"""DB-API implementation backed by HiveServer2 (Thrift API)
See http://www.python.org/dev/peps/pep-0249/
Many docstrings in this file are based on the PEP, which is in the public domain.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from urllib.parse import urlparse

import datetime
import json
import re
from decimal import Decimal
from ssl import CERT_NONE, CERT_OPTIONAL, CERT_REQUIRED
import http.client as httplib
from urllib.parse import *

from uniphi import common
from uniphi.common import DBAPITypeObject
# Make all exceptions visible in this uniphi per DB-API
import logging
import sys
import uniphi.typeId
import uniphi.constants
from uniphi.aesCipher import AESCipher
import socket
import gzip

apilevel = '2.0'
threadsafety = 2  # Threads may share the uniphi and connections.
paramstyle = 'pyformat'  # Python extended format codes, e.g. ...WHERE name=%(name)s
key = b"teamuniphi@cunninghamroadfrmbang"

_logger = logging.getLogger(__name__)

_TIMESTAMP_PATTERN = re.compile(r'(\d+-\d+-\d+ \d+:\d+:\d+(\.\d{,6})?)')

ssl_cert_parameter_map = {
    "none": CERT_NONE,
    "optional": CERT_OPTIONAL,
    "required": CERT_REQUIRED,
}


def _parse_timestamp(value):
    if value:
        match = _TIMESTAMP_PATTERN.match(value)
        if match:
            if match.group(2):
                format = '%Y-%m-%d %H:%M:%S.%f'
                # use the pattern to truncate the value
                value = match.group()
            else:
                format = '%Y-%m-%d %H:%M:%S'
            value = datetime.datetime.strptime(value, format)
        else:
            raise Exception(
                'Cannot convert "{}" into a datetime'.format(value))
    else:
        value = None
    return value


TYPES_CONVERTER = {"DECIMAL_TYPE": Decimal,
                   "TIMESTAMP_TYPE": _parse_timestamp}


class HiveParamEscaper(common.ParamEscaper):
    def escape_string(self, item):
        # backslashes and single quotes need to be escaped
        # TODO verify against parser
        # Need to decode UTF-8 because of old sqlalchemy.
        # Newer SQLAlchemy checks dialect.supports_unicode_binds before encoding Unicode strings
        # as byte strings. The old version always encodes Unicode as byte strings, which breaks
        # string formatting here.
        if isinstance(item, bytes):
            item = item.decode('utf-8')
        return "'{}'".format(
            item
                .replace('\\', '\\\\')
                .replace("'", "\\'")
                .replace('\r', '\\r')
                .replace('\n', '\\n')
                .replace('\t', '\\t')
        )


_escaper = HiveParamEscaper()


def connect(*args, **kwargs):
    """Constructor for creating a connection to the database. See class :py:class:`Connection` for
    arguments.
    :returns: a :py:class:`Connection` object.
    """
    return Connection(*args, **kwargs)


class Connection(object):
    """Wraps a http uniphi session"""

    def __init__(
            self,
            connectStr=None
    ):
        scheme = connectStr.drivername
        uri = "{host}:{port}".format(host=connectStr.host, port=connectStr.port)
        self._username = connectStr.username
        password = connectStr.password
        _auth_token = None

        if scheme in ("https", "http", "uniphi"):
            if scheme == "https" or scheme == "uniphi":
                if password is None:
                    raise ValueError("Password should be set")
                if self._username is None:
                    raise ValueError("Username should be set")
                # ssl_context = create_default_context()
                # ssl_context.check_hostname = "false"
                # ssl_cert = "none"
                # ssl_context.verify_mode = ssl_cert_parameter_map.get(ssl_cert, CERT_NONE)
                self.http_transport = httplib.HTTPConnection(uri, timeout=10000000)
                # Create a call to get a token here by first validating credentials
                self.signin(password)
                response = self.http_transport.getresponse()
                if response.status == 409:
                    response.read()
                    self.signoutAndSignin(password)
                    response = self.http_transport.getresponse()
                    if response.status != 200:
                        raise Exception("Unable to sign back into uniphi")
                elif response.status == 200:
                    pass
                else:
                    raise Exception("Unknown issue while logging in")
                resp = response.read()
                _logger.info("got response from server {resp}".format(resp = resp))
                responseDict = json.loads(resp)
                self._auth_token = responseDict['authtoken']
            else:
                raise ValueError(
                    "Use scheme HTTPS/UNIPHI"
                )
        # This is the part where other drivers point to a database. It is not necessary for Uniphi.

    def signoutAndSignin(self, password):
        body = {
            "username": self._username
        }
        headers = {"Content-Type": "text/plain", "Connection": "keep-alive", "Accept-Encoding": "gzip, deflate, br",
                   "Accept": "*/*"}
        # self._set_headers(http_transport, None)
        jsonbody = json.dumps(body)
        print("using json {jsonbody}".format(jsonbody=jsonbody))
        self.http_transport.request("POST", "/signout", json.dumps(body), headers)
        response = self.http_transport.getresponse()
        if response.status == 200:
            response.read()
            self.signin(password)
        else:
            raise Exception("User unable to logout")

    def signin(self, password):
        encodedtext = AESCipher().encrypt(password).hex()
        print(encodedtext)
        body = {
            "username": self._username,
            "password": encodedtext
        }
        headers = {"Content-Type": "application/json; charset=UTF-8", "Connection": "keep-alive", "Accept-Encoding": "gzip, deflate, br",
                   "Accept": "*/*"}
        # self._set_headers(http_transport, None)
        jsonbody = json.dumps(body)
        self.http_transport.request("POST", "/signin", json.dumps(body), headers)

    @staticmethod
    def _set_headers(http_transport, auth_token):
        http_transport.putheader('Connection', 'keep-alive')
        http_transport.putheader('Accept-Encoding', 'gzip, deflate, br')
        http_transport.putheader('Accept', '*/*')
        if auth_token is not None:
            http_transport.putheader('Authorization', 'Bearer {token}'.format(token=auth_token))

    def __enter__(self):
        """Transport should already be opened by __init__"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Call close"""
        self.close()

    def close(self):
        """Uniphi doesn't need to close client connections """
        pass

    def commit(self):
        """Hive does not support transactions, so this does nothing."""
        pass

    def cursor(self, *args, **kwargs):
        """Return a new :py:class:`Cursor` object using the connection."""
        return Cursor(self, *args, **kwargs)

    @property
    def client(self):
        return self.http_transport

    @property
    def clientAuth(self):
        return self._auth_token

    @property
    def user(self):
        return self._username

    @property
    def sessionHandle(self):
        return self._sessionHandle

    def rollback(self):
        raise Exception("Uniphi does not support transactions")  # pragma: no cover


class Cursor(common.DBAPICursor):
    """These objects represent a database cursor, which is used to manage the context of a fetch
    operation.
    Cursors are not isolated, i.e., any changes done to the database by a cursor are immediately
    visible by other cursors or connections.
    """

    def __init__(self, connection, arraysize=1000):
        super(Cursor, self).__init__()
        self._arraysize = arraysize
        self._connection = connection
        self._plan_uuid = None
        self._data = None
        self._query_columns_description = None
        self._description = None

    def _reset_state(self):
        """Reset state about the previous query in preparation for running another query"""
        pass

    @property
    def arraysize(self):
        return self._arraysize

    @arraysize.setter
    def arraysize(self, value):
        """Array size cannot be None, and should be an integer"""
        default_arraysize = 1000
        try:
            self._arraysize = int(value) or default_arraysize
        except TypeError:
            self._arraysize = default_arraysize

    @property
    def description(self):
        """This read-only attribute is a sequence of 7-item sequences.
        Each of these sequences contains information describing one result column:
        - name
        - type_code
        - display_size (None in current implementation)
        - internal_size (None in current implementation)
        - precision (None in current implementation)
        - scale (None in current implementation)
        - null_ok (always True in current implementation)
        This attribute will be ``None`` for operations that do not return rows or if the cursor has
        not had an operation invoked via the :py:meth:`execute` method yet.
        The ``type_code`` can be interpreted by comparing it to the Type Objects specified in the
        section below.
        """
        if self._description is None:
            self._description = []
            for col in self._query_columns_description:
                type_code = col.split(":")[1]
                column_name = col.split(":")[0]
                self._description.append((
                    column_name,
                    type_code,
                    None, None, None, None, True
                ))
        return self._description

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the operation handle"""
        pass

    def execute(self, operation, parameters=None, **kwargs):
        """Prepare and execute a database operation (query or command).
        Return values are not defined.
        """
        socket.setdefaulttimeout(6000)
        _logger.info("got command {op}".format(op=operation))

        if operation == "NOOP":
            return [{"test": "test"}]

        # Prepare statement
        if parameters is None:
            sql = operation
        else:
            sql = operation % _escaper.escape_args(parameters)

        is_describe_query = "DESCRIBE" in sql
        #if self._plan_uuid is None:
            # grep out the table name and set the context
        sql_json = None
        if not is_describe_query:
            _logger.info("Grepping pattern from query: {sql}".format(sql=sql))
            regexPattern = re.compile(
                r'[a-zA-Z0-9_\._-]+:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
            if regexPattern.search(sql) is not None:
                table_uuid_group = regexPattern.search(sql).group()
                self.set_context_for_query(table_uuid_group.split(":")[1])
                sql = sql.replace(table_uuid_group, "UNIPHI")
            sql_json = {"sqlQuery": sql, "isPivoted": True, "isPlain": True, "planUuid": self._plan_uuid}
        else:
            sql_json = {"sqlQuery": sql, "isPivoted": False, "isPlain": True, "planUuid": self._plan_uuid}

        transport = self._connection.client
        bearer = "Bearer " + self._connection.clientAuth
        headers = {"Content-Type": "application/json", "Connection": "keep-alive", "Accept-Encoding": "gzip, deflate, br",
                   "Accept": "*/*", "Authorization": bearer}
        # self._set_headers(http_transport, None)
        transport.request("POST", "/query", json.dumps(sql_json), headers)
        response = transport.getresponse()
        resp = None
        if response.getheader("Content-Encoding") == "gzip":
            resp = gzip.decompress(response.read())
        else:
            resp = response.read()
        responseDict = json.loads(resp)
        _logger.info("got response {op}".format(op=responseDict))
        if not is_describe_query:
            self._data = responseDict['data']
            self._query_columns_description = responseDict['description']
            return self._data
        else:
            return responseDict

    def get_view_names(self):
        user = self._connection.user
        transport = self._connection.client
        bearer = "Bearer " + self._connection.clientAuth
        headers = {"Content-Type": "text/plain", "Connection": "keep-alive", "Accept-Encoding": "gzip, deflate, br",
                   "Accept": "*/*", "Authorization": bearer}
        body = {"username": user}
        _logger.info("got auth object {conn} and user {user}".format(conn=bearer, user=user))
        transport.request("POST", "/extract/preferences/fetch", json.dumps(body), headers)
        response = transport.getresponse()
        resp = None
        if response.getheader("Content-Encoding") == "gzip":
            resp = gzip.decompress(response.read())
        else:
            resp = response.read()
        response_dict = json.loads(resp)
        list_of_views = []
        for item in response_dict:
            list_of_views.append(item['planName'] + ":" + item['planUUID'])
        return list_of_views

    def cancel(self):
        """Uniphi does not support cancelling of queries as yet"""
        pass

    def _fetch_more(self):
        """Send another TFetchResultsReq and update state"""
        pass

    def _fetch_all(self):
        return self._data

    def fetchall(self):
        return self._data

    def poll(self, get_progress_update=True):
        """Poll for and return the raw status data provided by the Hive Thrift REST API.
        :returns: ``ttypes.TGetOperationStatusResp``
        :raises: ``ProgrammingError`` when no query has been started
        .. note::
            This is not a part of DB-API.
        """
        pass

    def fetch_logs(self):
        """Retrieve the logs produced by the execution of the query.
        Can be called multiple times to fetch the logs produced after the previous call.
        :returns: list<str>
        :raises: ``ProgrammingError`` when no query has been started
        .. note::
            This is not a part of DB-API.
        """
        pass

    def set_context_for_query(self, plan_id):
        self._plan_uuid = plan_id


#
# Type Objects and Constructors
#


for type_id in uniphi.constants.PRIMITIVE_TYPES:
    name = uniphi.typeId.TypeId._VALUES_TO_NAMES[type_id]
    setattr(sys.modules[__name__], name, DBAPITypeObject([name]))

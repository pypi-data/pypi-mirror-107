"""Integration between SQLAlchemy and Hive.
Some code based on
https://github.com/zzzeek/sqlalchemy/blob/rel_0_5/lib/sqlalchemy/databases/sqlite.py
which is released under the MIT license.
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import decimal

import re
from sqlalchemy import exc
from sqlalchemy import processors
from sqlalchemy import types
from sqlalchemy import util
# TODO shouldn't use mysql type
from sqlalchemy.databases import mysql
from sqlalchemy.engine import default, Engine, Connection
from sqlalchemy.sql import compiler
from sqlalchemy.sql.compiler import SQLCompiler

from uniphi import uniphi
from uniphi.common import UniversalSet

from dateutil.parser import parse
from decimal import Decimal
from uniphi.exceptions import *
import logging

_logger = logging.getLogger(__name__)


class UniphiStringTypeBase(types.TypeDecorator):
    """Translates strings returned by Thrift into something else"""
    impl = types.String

    def process_bind_param(self, value, dialect):
        raise NotImplementedError("Writing to Hive not supported")


class UniphiDate(UniphiStringTypeBase):
    """Translates date strings to date objects"""
    impl = types.DATE

    def process_result_value(self, value, dialect):
        return processors.str_to_date(value)

    def result_processor(self, dialect, coltype):
        def process(value):
            if isinstance(value, datetime.datetime):
                return value.date()
            elif isinstance(value, datetime.date):
                return value
            elif value is not None:
                return parse(value).date()
            else:
                return None

        return process

    def adapt(self, impltype, **kwargs):
        return self.impl


class UniphiTimestamp(UniphiStringTypeBase):
    """Translates timestamp strings to datetime objects"""
    impl = types.TIMESTAMP

    def process_result_value(self, value, dialect):
        return processors.str_to_datetime(value)

    def result_processor(self, dialect, coltype):
        def process(value):
            if isinstance(value, datetime.datetime):
                return value
            elif value is not None:
                return parse(value)
            else:
                return None

        return process

    def adapt(self, impltype, **kwargs):
        return self.impl


class UniphiDecimal(UniphiStringTypeBase):
    """Translates strings to decimals"""
    impl = types.DECIMAL

    def process_result_value(self, value, dialect):
        if value is not None:
            return decimal.Decimal(value)
        else:
            return None

    def result_processor(self, dialect, coltype):
        def process(value):
            if isinstance(value, Decimal):
                return value
            elif value is not None:
                return Decimal(value)
            else:
                return None

        return process

    def adapt(self, impltype, **kwargs):
        return self.impl


class UniphiIdentifierPreparer(compiler.IdentifierPreparer):
    # Just quote everything to make things simpler / easier to upgrade
    reserved_words = UniversalSet()

    def __init__(self, dialect):
        super(UniphiIdentifierPreparer, self).__init__(
            dialect,
            initial_quote='`',
        )


_type_map = {
    'boolean': types.Boolean,
    'tinyint': mysql.MSTinyInteger,
    'smallint': types.SmallInteger,
    'int': types.Integer,
    'bigint': types.BigInteger,
    'float': types.Float,
    'double': types.Float,
    'string': types.String,
    'varchar': types.String,
    'char': types.String,
    'date': UniphiDate,
    'timestamp': UniphiTimestamp,
    'binary': types.String,
    'array': types.String,
    'map': types.String,
    'struct': types.String,
    'uniontype': types.String,
    'decimal': UniphiDecimal,
}


class UniphiCompiler(SQLCompiler):
    def visit_concat_op_binary(self, binary, operator, **kw):
        return "concat(%s, %s)" % (self.process(binary.left), self.process(binary.right))

    def visit_insert(self, *args, **kwargs):
        raise NotSupportedError()

    def visit_column(self, *args, **kwargs):
        result = super(UniphiCompiler, self).visit_column(*args, **kwargs)
        return result

    def visit_char_length_func(self, fn, **kw):
        return 'length{}'.format(self.function_argspec(fn, **kw))


class UniphiTypeCompiler(compiler.GenericTypeCompiler):
    def visit_INTEGER(self, type_):
        return 'INT'

    def visit_NUMERIC(self, type_):
        return 'DECIMAL'

    def visit_CHAR(self, type_):
        return 'STRING'

    def visit_VARCHAR(self, type_):
        return 'STRING'

    def visit_NCHAR(self, type_):
        return 'STRING'

    def visit_TEXT(self, type_):
        return 'STRING'

    def visit_CLOB(self, type_):
        return 'STRING'

    def visit_BLOB(self, type_):
        return 'BINARY'

    def visit_TIME(self, type_):
        return 'TIMESTAMP'

    def visit_DATE(self, type_):
        return 'DATE'

    def visit_DATETIME(self, type_):
        return 'TIMESTAMP'


# class HiveExecutionContext(default.DefaultExecutionContext):
#     """This is pretty much the same as SQLiteExecutionContext to work around the same issue.
#     http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#dotted-column-names
#     engine = create_engine('hive://...', execution_options={'hive_raw_colnames': True})
#     """
#
#     @util.memoized_property
#     def _preserve_raw_colnames(self):
#         # Ideally, this would also gate on hive.resultset.use.unique.column.names
#         return self.execution_options.get('hive_raw_colnames', False)
#
#     def _translate_colname(self, colname):
#         # Adjust for dotted column names.
#         # When hive.resultset.use.unique.column.names is true (the default), Hive returns column
#         # names as "tablename.colname" in cursor.description.
#         if not self._preserve_raw_colnames and '.' in colname:
#             return colname.split('.')[-1], colname
#         else:
#             return colname, None


class UniphiDialect(default.DefaultDialect):
    preparer = UniphiIdentifierPreparer
    statement_compiler = UniphiCompiler
    supports_views = True
    supports_alter = True
    supports_pk_autoincrement = False
    supports_default_values = False
    supports_empty_insert = False
    supports_native_decimal = True
    supports_native_boolean = True
    supports_unicode_statements = True
    supports_unicode_binds = True
    returns_unicode_strings = True
    description_encoding = None
    supports_multivalues_insert = True
    type_compiler = UniphiTypeCompiler
    supports_sane_rowcount = False
    driver = "uniphi"

    def _dialect_specific_select_one(self):
        return "NOOP"

    @classmethod
    def dbapi(cls):
        return uniphi

    def create_connect_args(self, url):
        kwargs = {
            'connectStr': url,
        }
        kwargs.update(url.query)
        return [], kwargs

    def get_schema_names(self, connection, **kw):
        # Equivalent to SHOW DATABASES
        # Rerouting to view names
        return self.get_view_names(connection)

    def get_view_names(self, connection, schema=None, **kw):
        # Hive does not provide functionality to query tableType
        # This allows reflection to not crash at the cost of being inaccurate
        engine = connection
        conn = engine.raw_connection()
        return conn.connection.cursor().get_view_names()

    def _get_table_columns(self, connection, uniphi_view_name):
        full_table = uniphi_view_name
        # TODO using TGetColumnsReq hangs after sending TFetchResultsReq.
        # Using DESCRIBE works but is uglier.
        try:
            # This needs the table name to be unescaped (no backticks).
            uuid = full_table.split(":")[1]
            full_table = "UNIPHI"
            cursor = None
            if isinstance(connection, Engine):
                cursor = connection.raw_connection().connection.cursor()
            elif isinstance(connection, Connection):
                cursor = connection.connection.cursor()
            else:
                raise Exception("Got type of object {typ}".format(type(connection)))

            cursor.set_context_for_query(uuid)
            rows = cursor.execute('DESCRIBE {}'.format(full_table))
        except exc.OperationalError as e:
            # Does the table exist?
            regex_fmt = r'Uniphi view not found {}'
            regex = regex_fmt.format(re.escape(full_table))
            if re.search(regex, e.args[0]):
                raise exc.NoSuchTableError(full_table)
            else:
                raise
        else:
            # Hive is stupid: this is what I get from DESCRIBE some_schema.does_not_exist
            regex = r'View .* does not exist'
            if len(rows) == 1 and re.match(regex, rows[0].col_name):
                raise exc.NoSuchTableError(full_table)
            return rows

    def has_table(self, connection, table_name, schema=None):
        try:
            self._get_table_columns(connection, table_name)
            return True
        except Exception:
            return False

    def get_columns(self, connection, table_name, schema=None, **kw):
        rows = self._get_table_columns(connection, table_name)
        # # Strip whitespace
        # rows = [[col.strip() if col else None for col in row] for row in rows]
        # Filter out empty rows and comment
        #rows = [row for row in rows if row[0] and row[0] != '# col_name']
        result = []
        for row in rows:
            col_name = row['col_name']
            col_type = row['data_type']
            if col_name == '# Partition Information':
                break
            # Take out the more detailed type information
            # e.g. 'map<int,int>' -> 'map'
            #      'decimal(10,1)' -> decimal
            col_type = re.search(r'^\w+', col_type).group(0)
            try:
                coltype = _type_map[col_type]
                _logger.info("Got column {column} with data type {dt}".format(column=col_name, dt= coltype))
            except KeyError:
                util.warn("Did not recognize type '%s' of column '%s'" % (col_type, col_name))
                coltype = types.NullType

            result.append({
                'name': col_name,
                'type': coltype,
                'nullable': True,
                'default': None,
            })
        return result

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        # Hive has no support for foreign keys.
        return []

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        # Hive has no support for primary keys.
        return []

    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []

    def get_table_names(self, connection, schema=None, **kw):
        return self.get_view_names(connection)

    def do_rollback(self, dbapi_connection):
        # No transactions for Hive
        pass

    def _check_unicode_returns(self, connection, additional_tests=None):
        # We decode everything as UTF-8
        return True

    def _check_unicode_description(self, connection):
        # We decode everything as UTF-8
        return True

    def do_ping(self, connection):
        # We do not need the ping api as we are using http
        return True


class UniphiHTTPDialect(UniphiDialect):
    name = "uniphi"
    scheme = "uniphi"
    driver = "uniphi"

    def create_connect_args(self, url):
        kwargs = {
            "connectStr": url
        }
        if url.query:
            kwargs.update(url.query)
            return [], kwargs
        return ([], kwargs)


class UniphiHTTPSDialect(UniphiHTTPDialect):
    name = "uniphi"
    scheme = "uniphi"

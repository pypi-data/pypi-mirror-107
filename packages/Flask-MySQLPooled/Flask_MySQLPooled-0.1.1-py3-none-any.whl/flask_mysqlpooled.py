# -*- coding: UTF-8 -*-
from __future__ import absolute_import

import pymysql
from dbutils.pooled_db import PooledDB

try:
    from flask import _app_ctx_stack as _ctx_stack
except ImportError:
    from flask import _request_ctx_stack as _ctx_stack


class MySQLPooled(object):
    def __init__(self, app=None, prefix="MySQLPooled", **pool_args):
        self.pool_args = pool_args
        self.pool_args.setdefault('creator', pymysql)
        self.prefix = prefix
        self.connect_pool = None
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        self.app = app
        self.app.config.setdefault('MySQLPooled_DATABASE_HOST', 'localhost')
        self.app.config.setdefault('MySQLPooled_DATABASE_PORT', 3306)
        self.app.config.setdefault('MySQLPooled_DATABASE_USER', None)
        self.app.config.setdefault('MySQLPooled_DATABASE_PASSWORD', None)
        self.app.config.setdefault('MySQLPooled_DATABASE_DB', None)
        self.app.config.setdefault('MySQLPooled_DATABASE_CHARSET', 'utf8')
        self.app.config.setdefault('MySQLPooled_USE_UNICODE', True)
        self.app.config.setdefault('MySQLPooled_DATABASE_SOCKET', None)
        self.app.config.setdefault('MySQLPooled_SQL_MODE', None)

        self.app.config.setdefault('MySQLPooled_MINCACHED', 0)
        self.app.config.setdefault('MySQLPooled_MAXCACHED', 1)
        self.app.config.setdefault('MySQLPooled_MAXCONNECTIONS', 1)
        self.app.config.setdefault('MySQLPooled_BLOCKING', False)
        self.app.config.setdefault('MySQLPooled_MAXUSAGE', None)
        self.app.config.setdefault('MySQLPooled_SETSESSION', None)
        self.app.config.setdefault('MySQLPooled_RESET', True)
        self.app.config.setdefault('MySQLPooled_FAILURES', None)
        self.app.config.setdefault('MySQLPooled_PING', 1)
        self._init_pool_args()

        self.connect_pool = PooledDB(**self.pool_args)

        # Flask 0.9 or later
        if hasattr(self.app, 'teardown_appcontext'):
            self.app.teardown_request(self.teardown_request)
        # Flask 0.7 to 0.8
        elif hasattr(self.app, 'teardown_request'):
            self.app.teardown_request(self.teardown_request)
        # Older versions
        else:
            self.app.after_request(self.teardown_request)

    def _init_pool_args(self):
        self.pool_args.setdefault('host', self.app.config['MySQLPooled_DATABASE_HOST'])
        self.pool_args.setdefault('port', self.app.config['MySQLPooled_DATABASE_PORT'])
        self.pool_args.setdefault('user', self.app.config['MySQLPooled_DATABASE_USER'])
        self.pool_args.setdefault('password', self.app.config['MySQLPooled_DATABASE_PASSWORD'])
        self.pool_args.setdefault('db', self.app.config['MySQLPooled_DATABASE_DB'])
        self.pool_args.setdefault('charset', self.app.config['MySQLPooled_DATABASE_CHARSET'])
        self.pool_args.setdefault('use_unicode', self.app.config['MySQLPooled_USE_UNICODE'])
        self.pool_args.setdefault('unix_socket', self.app.config['MySQLPooled_DATABASE_SOCKET'])
        self.pool_args.setdefault('sql_mode', self.app.config['MySQLPooled_SQL_MODE'])

        self.pool_args.setdefault('mincached', self.app.config['MySQLPooled_MINCACHED'])
        self.pool_args.setdefault('maxcached', self.app.config['MySQLPooled_MAXCACHED'])
        self.pool_args.setdefault('maxconnections', self.app.config['MySQLPooled_MAXCONNECTIONS'])
        self.pool_args.setdefault('blocking', self.app.config['MySQLPooled_BLOCKING'])
        self.pool_args.setdefault('maxusage', self.app.config['MySQLPooled_MAXUSAGE'])
        self.pool_args.setdefault('setsession', self.app.config['MySQLPooled_SETSESSION'])
        self.pool_args.setdefault('reset', self.app.config['MySQLPooled_RESET'])
        self.pool_args.setdefault('failures', self.app.config['MySQLPooled_FAILURES'])
        self.pool_args.setdefault('ping', self.app.config['MySQLPooled_PING'])

    def connect(self):
        return self.connect_pool.connection()

    def teardown_request(self, exception):
        ctx = _ctx_stack.top
        if hasattr(ctx, "mysql_dbs"):
            try:
                if self.prefix in ctx.mysql_dbs:
                    ctx.mysql_dbs[self.prefix].close()
            except Exception as e:
                pass

    def get_db(self):
        ctx = _ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "mysql_dbs"):
                ctx.mysql_dbs = dict()
            if self.prefix not in ctx.mysql_dbs:
                ctx.mysql_dbs[self.prefix] = self.connect()
            return ctx.mysql_dbs[self.prefix]

# -*- coding: utf-8 -*-

import web.coroweb as coroweb
from aiohttp import web
import web.orm as orm
import config

patched_config = {
    'debug': False,
    'web': {
        'host': 'localhost',
        'port': 35327
    },
    'db': {
        'host': 'localhost',
        'port': 3306,
        'user': 'monadoj_test',
        'password': 'MONADOJ TEST',
        'db': 'monadoj_test'
    },
    'session': {
        'max_age': 90000,
        'secret': 'SECRET KEY'
    }
}

runner = None


async def init_database_content():
    """Initialize MySql database data (create empty tables)
    """
    pass


async def init(loop):
    """Start web service for test
    """
    global runner
    await orm.create_connection(loop, **config.configs.db)
    await init_database_content()
    runner = web.AppRunner(coroweb.app, access_log_format='%a "%r" %s %bB %Dus')
    await runner.setup()
    site = web.TCPSite(runner, config.configs.web.host, config.configs.web.port)
    await site.start()


async def close_test():
    """Close web service
    """
    global runner
    if runner is not None:
        await runner.cleanup()
    orm.close()


def patch_config():
    """Mock default settings
    """
    config.configs = config.to_dict(patched_config)


async def init_test(loop):
    """Initialize test environment
    """
    patch_config()
    await init(loop)

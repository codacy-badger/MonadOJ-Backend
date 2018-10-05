#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(name)s %(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logging.info('=========== PRE-INITIALIZATION =========')

from aiohttp import web
import asyncio

from config import configs
import web.coroweb as coroweb
import web.orm as orm
import handlers


async def init(event_loop):
    """Start web service

    Args:
        event_loop: (asyncio event loop) The event loop

    Returns:
        aiohttp.web.AppRunner: The AppRunner instance
    """
    logging.info('============= INITIALIZING ============')
    await orm.create_connection(event_loop, **configs.db)
    runner = web.AppRunner(coroweb.app, access_log_format='%a "%r" %s %bB %Dus')
    logging.info('Setting up web app...')
    await runner.setup()
    site = web.TCPSite(runner, configs.web.host, configs.web.port)
    await site.start()
    logging.info('Starting judge server...')
    logging.info('============ SERVER RUNNING ===========')
    logging.info(f'Server started at http://{configs.web.host}:{configs.web.port}')
    return runner


async def server_close(runner):
    """Shutdown the server

    Args:
        runner: (aiohttp.web.AppRunner) The AppRunner instance
    """
    if runner is not None:
        await runner.cleanup()
    orm.close()


if __name__ == '__main__':
    app_runner = None
    loop = None
    try:
        loop = asyncio.get_event_loop()
        app_runner = loop.run_until_complete(init(loop))
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt')
    finally:
        logging.info('============= SERVER STOP =============')
        logging.info('Stopping web service...')
        loop.run_until_complete(server_close(app_runner))
        logging.info('Stopping asyncio loop...')
        loop.close()
        logging.info('Server stopped')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

# clean old log
with open('test.log', 'w') as f:
    pass

logging.basicConfig(level=logging.INFO,
                    format='[%(name)s %(levelname)s] %(message)s',
                    filename='test.log')

import asyncio
import unittest

from tests import *
from tests import init_test
import handlers
from tests import extra_handlers


if __name__ == '__main__':
    loop = None
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_test.init_test(loop))
        unittest.main(verbosity=2)
    finally:
        loop.run_until_complete(init_test.close_test())

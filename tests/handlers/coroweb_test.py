# -*- coding: utf-8 -*-

from unittest import TestCase

from tests.util import async_test, MonadSession


class TestCoroutineWeb(TestCase):
    @async_test
    async def setUp(self):
        self.client = MonadSession()

    @async_test
    async def tearDown(self):
        await self.client.close()
        self.client = None

    @async_test
    async def test_basic_get(self):
        req = await self.client.get('/test/get')
        resp = await req.json()

        self.assertEqual(req.status, 200)
        self.assertEqual(resp['msg'], 'Success')
        self.assertIsNone(resp['error'])

    @async_test
    async def test_get_param(self):
        params = dict(param='Get Param')
        req = await self.client.get('/test/get_params', params=params)
        resp = await req.json()

        self.assertIsNone(resp['error'])
        self.assertEqual(resp['msg'], 'Get Param')

    @async_test
    async def test_get_missing_param(self):
        req = await self.client.get('/test/get_params')
        resp = await req.json()

        self.assertEqual(req.status, 400)
        self.assertIsNotNone(resp['error'])
        self.assertEqual(resp['error'], 'request:missing_params')

    @async_test
    async def test_get_param_default(self):
        params = dict(param='Get Param')
        req = await self.client.get('/test/get_default_params', params=params)
        resp = await req.json()

        self.assertIsNone(resp['error'])
        self.assertEqual(resp['msg'], 'Get Param DEFAULT')

    @async_test
    async def test_post(self):
        payload = dict(data='Post Data')
        req = await self.client.post('/test/post', data=payload)
        resp = await req.json()

        self.assertEqual(req.status, 200)
        self.assertIsNone(resp['error'])
        self.assertEqual(resp['msg'], 'Post Data')

    @async_test
    async def test_api_error(self):
        req = await self.client.get('/test/api_error')
        resp = await req.json()

        self.assertEqual(req.status, 400)
        self.assertEqual(resp['error'], 'test:test_error')
        self.assertEqual(resp['msg'], 'Some Error')

    @async_test
    async def test_204(self):
        req = await self.client.get('/test/204')

        self.assertEqual(req.status, 204)

    @async_test
    async def test_return_str(self):
        req = await self.client.get('/test/return_str')
        resp = await req.text()

        self.assertEqual(resp, 'Hello')

    @async_test
    async def test_return_byte(self):
        req = await self.client.get('/test/return_byte')
        resp = await req.read()

        self.assertEqual(resp, b'Hello bytes')

    @async_test
    async def test_return_with_500(self):
        req = await self.client.get('/test/return_with_500')
        resp = await req.text()

        self.assertEqual(req.status, 500)
        self.assertEqual(resp, 'Server internal error (fake)')

    @async_test
    async def test_websocket(self):
        async with self.client.ws_connect('/test/websocket') as ws:
            await ws.send_json(dict(type='msg', msg='Hello from test client'))
            msg = (await ws.receive_json())['msg']
            self.assertEqual(msg, 'Hello from test client')

            await ws.send_json(dict(type='hello'))
            msg = (await ws.receive_json())['error']
            self.assertEqual(msg, 'Invalid message type: hello')

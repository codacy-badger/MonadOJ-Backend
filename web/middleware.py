# -*- coding: utf-8 -*-

from aiohttp import web
import logging
import json


@web.middleware
async def response(request, handler):
    """Processing the response from the handler

    Args:
        request: (aiohttp.web.Request) Request instance
        handler: (function) The handler function

    Returns:
        aiohttp.web.Response: The response generate from the return value of handler
    """
    logging.debug('Response handler...')
    r = await handler(request)

    # StreamResponse object
    if isinstance(r, web.StreamResponse):
        return r

    # binary response
    if isinstance(r, bytes):
        logging.debug("=========")
        resp = web.Response(body=r)
        resp.content_type = 'application/octet-stream'
        return resp

    # body only
    if isinstance(r, str):
        if r.startswith('redirect:'):
            # log_redirection(request.path, r[9:], request.__user__)
            return web.HTTPFound(r[9:])
        resp = web.Response(body=r.encode('utf-8'))
        resp.content_type = 'text/html;charset=utf-8'
        return resp

    # json data
    if isinstance(r, dict):
        if r.get('error', None) is None:
            r['error'] = None
        resp = web.Response(
            body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
        resp.content_type = 'application/json;charset=utf-8'
        return resp

    # status code only
    if isinstance(r, int) and r >= 100 and r < 600:
        return web.Response(status=r)

    # status code and json data
    if isinstance(r, tuple) and len(r) == 2:
        t, m = r
        if isinstance(t, int) and t >= 100 and t < 600:
            if isinstance(m, dict):
                if m.get('error', None) is None:
                    m['error'] = None
                resp = web.Response(status=t,
                                    body=json.dumps(m, ensure_ascii=False, default=lambda o: o.__dict__).encode(
                                        'utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            return web.Response(status=t, text=str(m))
    # default:
    resp = web.Response(body=str(r).encode('utf-8'))
    resp.content_type = 'text/plain;charset=utf-8'
    return resp


middlewares = [response]

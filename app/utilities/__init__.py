from aiohttp import web


def html_response(text):
    return web.Response(text=text, content_type='text/html')

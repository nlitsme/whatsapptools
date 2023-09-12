# proxy requests to web.whatsapp.com, inserting some code in app.js to make protocol tracing easier.
#
# note:  'web.whatsapp.com'  is only specified in index.html  and app.js

import asyncio
import logging
import aiohttp
from aiohttp import web, payload
import os.path
import ssl

class WhatsappProxy:
    """
    proxy requests to the whatsapp server
    """
    def __init__(self, args, basepath):
        self.args = args
        self.basepath = basepath
        self.client = None

        self.app = web.Application()
        self.app.router.add_get('/ws/chat', self.websocket)
        self.app.router.add_get('/', self.mainpage)
        self.app.router.add_get(r'/{path:.+}', self.get)
        self.app.router.add_options('/{path:.+}', self.handle_options)
        self.app.router.add_post('/{path:.+}', self.handle_post)

        self.app.on_shutdown.append(self.onshutdown)

    async def handle_post(self, request):
        """
        method is not used.
        """
        print("POST", request)
        return web.HTTPNotFound()

    async def handle_options(self, request):
        """
        method is not used.
        """
        print("OPTION", request)
        return web.Response(headers={
                "access-control-allow-origin": "*",
                "access-control-allow-headers": "*",
                "access-control-allow-methods": "GET, OPTIONS, POST",
                "access-control-max-age": "86400",
            })

    async def websocket(self, request):
        """
        dummy - not used.
        Whatsapp is fine with using the https://web.whatsapp.com/ws/chat directly.
        """
        print("ws", request)
        return web.HTTPNotFound()

    async def mainpage(self, request):
        """
        index.html is the main page.
        """
        return web.FileResponse(os.path.join(self.basepath, 'index.html'))

    def ensureclient(self):
        """
        Creates the ClientSession object when needed.
        """
        if self.client:
            return

        moreargs = {}
        if self.args.trace:
            """
            Add debugging output
            """
            async def on_request_start(session, trace_config_ctx, params):
                print("Starting request", params)
            async def on_request_end(session, trace_config_ctx, params):
                print("Ending request", params)
            async def on_response_chunk_received(session, trace_config_ctx, params):
                print("rx chunk", params)
            async def on_request_chunk_sent(session, trace_config_ctx, params):
                print("tx chunk", session, params)

            trace_config = aiohttp.TraceConfig()
            trace_config.on_request_start.append(on_request_start)
            trace_config.on_request_end.append(on_request_end)
            trace_config.on_response_chunk_received.append(on_response_chunk_received)
            trace_config.on_request_chunk_sent.append(on_request_chunk_sent)

            moreargs["trace_configs"] = [trace_config]

        loop = asyncio.get_running_loop()
        self.client = aiohttp.ClientSession(loop=loop, **moreargs)

    async def get(self, request):
        """
        handle GET requests, serving files from either the basepath,
        or from https://web.whatsapp.com
        """
        try:
            self.ensureclient()

            path = request.match_info['path']
            if path.startswith('/'):
                raise Exception("invalid request")
            if path.find('..') >= 0:
                raise Exception("invalid request")

            localpath = os.path.join(self.basepath, path)
            if os.path.exists(localpath):

                # retrieve from local storage
                print("local file", path)
                return web.FileResponse(localpath)

            print("remote file", path)
            # retrieve from whatsapp
            url = "https://web.whatsapp.com/" + path
            hdrs = {
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://web.whatsapp.com/",
            }
            remote = await self.client.get(url, headers=hdrs)
            return web.Response(body=payload.StreamReaderPayload(remote.content), content_type=remote.content_type)
        except Exception as e:
            print(e)
            return web.HTTPNotFound()

    async def onshutdown(self, app):
        if self.client:
            await self.client.close()

    def run(self):
        """
        run the whatsapp proxy server

        TODO: auto generate certs.
        """
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain('domain_srv.crt', 'domain_srv.key')

        web.run_app(self.app, port=8111, ssl_context=ssl_context)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='whatsapp debugging proxy',
                                     epilog='The proxy serve static files from either the specified path, or web.whatsapp.com')
    parser.add_argument('--trace', action='store_true', help="enable http client debug output")
    parser.add_argument('--debug', action='store_true', help="enable http server debug output")
    parser.add_argument('basepath', type=str, help="where to find modified whatsapp files")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    app = WhatsappProxy(args, args.basepath)
    app.run()

if __name__ == '__main__':
    main()


import asyncio
import json
import mako
import sqlalchemy
import tornado.web


class JsonHandler(tornado.web.RequestHandler):
    def prepare(self):
        if "json" in self.headers.get("Content-Type"):
            logger.info("Handling json")

class JSHandler(tornado.web.RequestHandler):
    def prepare(self):
        # set header content to application/javascript
        pass

class MainHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        print(args, kwargs)
        self.write("OK\n")

class ApiV1Handler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        print(args, kwargs)
        self.write("OK\n")

class PingHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write("pong\n")

class Server(tornado.web.Application):
    def __init__(self):
        super().__init__(
            [
                (r"/api/v1/ping", PingHandler),
                (r"/api/v1/(.*)", ApiV1Handler),
                (r"/(.*)\.js", JSHandler),
                (r"/(.*)", MainHandler),
            ]
        )

async def amain():
    server = Server()
    server.listen(8000)
    await asyncio.Event().wait()

def main():
    asyncio.run(amain())

if __name__ == "__main__":
    main()

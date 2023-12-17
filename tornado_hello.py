'''
Description: There is a description
Author: ShAn_3003
version: 1.0
Date: 2023-12-16 00:08:12
LastEditors: ShAn_3003
LastEditTime: 2023-12-16 00:08:17
'''
import asyncio
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!")
def make_app():
    return tornado.web.Application([
        (r"/",MainHandler),
    ])
async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()
if __name__ == "__main__":
    asyncio.run(main())
    
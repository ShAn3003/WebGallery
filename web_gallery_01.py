'''
Description: There is a description
Author: ShAn_3003
version: 1.0
Date: 2023-12-16 21:30:06
LastEditors: ShAn_3003
LastEditTime: 2023-12-16 21:30:15
'''
import tornado.web
import tornado.ioloop

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # 使用 self.render 渲染 HTML 页面
        self.render("index.html")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ], template_path="templates")  # 指定模板文件夹的路径

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

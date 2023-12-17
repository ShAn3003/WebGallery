import os 
import uuid
import datetime
import tornado.web
import atexit
import json

class Album(object):
    def __init__(self,id,name,created_at,description):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.description = description
    
    def get_id(self):
        return self.id
    
    def set_name(self,name):
        self.name = name
    
    def to_dict(self):
        return {"id": self.id,"name":self.name,"created_at":self.created_at,"description":self.description}

class Photo(object):
    def __init__(self,id,album_id,name,path,size,created_at,tags):
        self.id = id
        self.album_id = album_id
        self.name = name
        self.path = path
        self.size = size
        self.tags = tags
        self.created_at = created_at
    def to_dict(self):
        return {
            "id": self.id,
            "album_id": self.album_id,
            "name": self.name,
            "path": self.path,
            "size": self.size,
            "created_at": self.created_at,
            "tags": self.tags,
        }
    
class AlbumManager(object):
    # 初始化的时候还需要把albums读回来
    def __init__(self,album_dir="albums"):
        self.album_dir = album_dir
        self.albums = []
        if not os.path.exists(album_dir):
            os.makedirs(album_dir)
       
        self.load_albums()

    def load_albums(self):
        try:
            with open("albums/album_data.json", 'r', encoding="utf-8") as fr:
                album_data = json.load(fr)
                self.albums = [Album(**data) for data in album_data]
        except FileNotFoundError:
            pass
        

    def save_data_on_exit(self):
        album_data = [album.to_dict() for album in self.albums]
        with open("albums/album_data.json",'w',encoding="utf-8") as fw:
            json.dump(album_data,fw)
    
    # 创建album的时候直接创建album对象
    def create_album(self,album_name):
        print(f"创建{album_name}相册")
        album_id = str(uuid.uuid4())
        album_path = os.path.join(self.album_dir,album_id)
        os.makedirs(album_path)
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        album  = Album(album_id,album_name,created_at,"None")
        self.albums.append(album)

    # 删除album的时候还需要把对应的Album对象删除
    def del_album(self,album_id):
        album_path = os.path.join(self.album_dir,album_id)
        if os.path.exists(album_path):
            os.rmdir(album_path)
        for album in self.albums:
            if album_id ==album.get_id():
                print(f"删除{album.name}相册")
                self.albums.remove(album)
                break

    # 重命名album
    def rename_album(self,album_id,new_name):
        for album in self.albums:
            if album_id ==album.get_id():
                album.set_name(new_name)
                break

album_manager = AlbumManager()
atexit.register(album_manager.save_data_on_exit)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", albums=album_manager.albums)

class AddAlbumHandler(tornado.web.RequestHandler):
    def post(self):
        album_name = self.get_argument("album_name")
        album_manager.create_album(album_name)
        self.redirect("/")

class RenameAlbumHandler(tornado.web.RequestHandler):
    def post(self, album_id):
        new_album_name = self.get_argument("new_album_name")
        album_manager.rename_album(album_id, new_album_name)
        self.redirect("/")

class DeleteAlbumHandler(tornado.web.RequestHandler):
    def get(self,album_id):
        album_manager.del_album(album_id)
        self.redirect('/')

class AlbumHandler(tornado.web.RequestHandler):
    def get(self, album_id):
        print("处理打开相册请求")
        # 处理单个相册的请求
        album_name = ""
        for album in album_manager.albums:
            if album_id==album.id:
                album_name = album.name
                break
        album_path = os.path.join(album_manager.album_dir, album_id)
        photos = [f for f in os.listdir(album_path) if os.path.isfile(os.path.join(album_path, f))]
        self.render("album.html", album_id=album_id,album_name=album_name, photos=photos)
    def post(self, album_id):
        print("处理上传照片请求")
        upload_path = os.path.join(album_manager.album_dir, album_id)
        # 获取上传的文件
        file_data = self.request.files.get("photo")
        if file_data:
            # 保存上传的文件
            photo = file_data[0]
            file_name = photo["filename"]
            file_path = os.path.join(upload_path, file_name)
            with open(file_path, "wb") as f:
                f.write(photo["body"])
            
            photo_id = str(uuid.uuid4())
            created_at= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tags = ""
            new_photo = Photo(photo,album_id,file_name,file_path,len(photo["body"]),created_at, tags)

        self.redirect("/album/{}".format(album_id))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/album/([^/]+)", AlbumHandler),
    (r"/add_album",AddAlbumHandler),
    (r"/delete_album/([^/]+)", DeleteAlbumHandler),
    (r"/rename_album/([^/]+)", RenameAlbumHandler),
], template_path="templates",debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
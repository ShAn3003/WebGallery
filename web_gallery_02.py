import os 
import uuid
import datetime
import tornado.web
import json
import shutil

class Album(object):
    def __init__(self,id,name,created_at,description):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.description = description
        self.photos = []
        self.load_photos()

    def load_photos(self):
        print(f"读取{self.id}相册图片文件")
        if os.path.exists(f"albums/{self.id}/photo_data.json"):
            with open(f"albums/{self.id}/photo_data.json",'r',encoding = 'utf-8') as fr:
                photo_data = json.load(fr)
                self.photos = [Photo(**data) for data in photo_data]
        else:
            self.save_photos()
        
    def add_photo(self,album_id,file_data):
        upload_path = os.path.join(album_manager.album_dir, album_id)
        if file_data:
            # 保存上传的文件
            photo = file_data[0]
            file_name = photo["filename"]
            file_path = os.path.join(upload_path, file_name)
            with open(file_path, "wb") as f:
                f.write(photo["body"])
            
            photo_id = str(uuid.uuid4())
            created_at= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tags = []
            new_photo = Photo(photo_id,album_id,file_name,upload_path,len(photo["body"]),created_at, tags)
            self.photos.append(new_photo)
            self.save_photos()
    def filter_photos_by_tag(self, tag):
        # 根据标签过滤图片
        return [photo for photo in self.photos if photo.has_tag(tag)]
    def rename_photo(self, photo_id, new_name):
        # 找到对应的 Photo 对象
        target_photo = next((photo for photo in self.photos if photo.id == photo_id), None)
        if target_photo:
            # 重命名文件
            os.rename(os.path.join(target_photo.path,target_photo.name), os.path.join(target_photo.path,new_name))
            # 更新 Photo 对象的属性
            target_photo.name = new_name
            # 保存更新后的信息
            self.save_photos()
    def delete_photo(self, photo_id):
        # 找到对应的 Photo 对象
        target_photo = next((photo for photo in self.photos if photo.id == photo_id), None)
        if target_photo:
            # 删除照片文件
            os.remove(os.path.join(target_photo.path, target_photo.name))
            # 从相册中移除 Photo 对象
            self.photos.remove(target_photo)
            # 保存更新后的信息
            self.save_photos()
    def add_tag_to_photo(self, photo_id, tag):
        # 找到对应的 Photo 对象
        target_photo = next((photo for photo in self.photos if photo.id == photo_id), None)
        if target_photo:
            # 添加标签
            target_photo.tags.append(tag)
            # 保存更新后的信息
            self.save_photos()
    def save_photos(self):
        # 将 Photo 对象列表保存到文件
        photo_data = [photo.to_dict() for photo in self.photos]
        with open(f"albums/{self.id}/photo_data.json", 'w', encoding="utf-8") as fw:
            json.dump(photo_data, fw)

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
        self.tags = tags if tags else []
        self.created_at = created_at
    def has_tag(self, tag):
        # 检查是否包含指定标签
        return tag in self.tags
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
        

    def save_albums(self):
        album_data = [album.to_dict() for album in self.albums]
        with open("albums/album_data.json",'w',encoding="utf-8") as fw:
            json.dump(album_data,fw)
        
    def get_album_by_id(self, album_id):
        return next((album for album in self.albums if album.id == album_id), None)
    # 创建album的时候直接创建album对象
    def create_album(self,album_name):
        print(f"创建{album_name}相册")
        album_id = str(uuid.uuid4())
        album_path = os.path.join(self.album_dir,album_id)
        os.makedirs(album_path)
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        album  = Album(album_id,album_name,created_at,"None")
        self.albums.append(album)
        self.save_albums()

    # 删除album的时候还需要把对应的Album对象删除
    def del_album(self,album_id):
        album_path = os.path.join(self.album_dir, album_id)
        if os.path.exists(album_path):
            shutil.rmtree(album_path)
        album = self.get_album_by_id(album_id)
        if album:
            self.albums.remove(album)
            self.save_albums()
        

    # 重命名album
    def rename_album(self,album_id,new_name):
        album = self.get_album_by_id(album_id)
        if album:
            album.set_name(new_name)
            self.save_albums()


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
        album = album_manager.get_album_by_id(album_id)
        search_tag = self.get_argument("search_tag", None)
        if album:
            self.render("album.html", album= album,album_id=album.id, album_name=album.name, photos=album.photos, search_tag=search_tag)
    def post(self, album_id):
        print("处理上传照片请求")
        # 获取上传的文件
        file_data = self.request.files.get("photo")
        album = album_manager.get_album_by_id(album_id)
        if album:
            if file_data:
                album.add_photo(album_id, file_data)
            else:
                # 处理重命名照片或删除照片的逻辑
                action = self.get_argument("action", None)
                if action == "rename":
                    # 处理重命名照片的逻辑
                    photo_id_to_rename = self.get_argument("photo_id_to_rename", None)
                    new_photo_name = self.get_argument("new_photo_name", None)
                    
                    if photo_id_to_rename and new_photo_name:
                        album.rename_photo(photo_id_to_rename, new_photo_name)
                elif action == "delete":
                    # 处理删除照片的逻辑
                    photo_id_to_delete = self.get_argument("photo_id_to_delete", None)
                    if photo_id_to_delete:
                        album.delete_photo(photo_id_to_delete)
                elif action == "add_tag":
                # 获取新标签和要添加标签的照片的 ID
                    new_tag = self.get_argument("new_tag", None)
                    photo_id_to_tag = self.get_argument("photo_id_to_tag", None)
                    if new_tag and photo_id_to_tag:
                        # 调用相册对象的添加标签方法
                        album.add_tag_to_photo(photo_id_to_tag, new_tag)
        self.redirect("/album/{}".format(album_id))


album_manager = AlbumManager()

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "albums"),
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/album/([^/]+)", AlbumHandler),
    (r"/add_album", AddAlbumHandler),
    (r"/delete_album/([^/]+)", DeleteAlbumHandler),
    (r"/rename_album/([^/]+)", RenameAlbumHandler),
], template_path="templates", debug=True, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

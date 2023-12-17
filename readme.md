# Web_Gallery_ShAn_3003--Version0.0.1

## 介绍

本项目是一个功能丰富的相册管理系统，采用 Python 和 Tornado 框架开发，用于高效管理和组织您的数字图像收藏。

## 特点

* 轻松管理相册：创建、重命名、删除相册，并根据需要排序和过滤。
* 上传和浏览照片：无缝上传各种格式的照片，支持缩放预览和全屏查看。
* 灵活的元数据管理：为照片添加标题、描述、关键字和自定义标签，方便检索和分类。
* 强大的搜索功能：根据文件名、标签、元数据等多种条件快速准确地搜索照片。
* 安全可靠：文件系统存储确保数据安全，可选择部署方式灵活应用于个人或团队协作场景。
* 开放可扩展：模块化设计架构易于扩展，支持根据实际需求添加更多功能。

## 技术栈

* 后端：Python 3.x，Tornado 6.x
* 数据库：无（文件系统存储）
* 模板引擎：Mako
* 可选扩展：数据库集成（MySQL、PostgreSQL等），用户身份验证，图像处理库

## 安装和运行

* 系统要求：Python 3.x 环境，pip 包管理工具
* 安装依赖：
    ```bash
    pip install tornado uuid datetime os json shutil
    ```
* 克隆代码仓库：
    ```bash
    ```
* 运行应用： 
  ```bash
  python web_gallery.py
  ```
* 访问 http://localhost:8888/ 以打开主界面   
## 使用说明  
  1. 主界面：查看所有相册列表，可按名称、创建时间排序。
创建新相册，管理现有相册。  
  1. 相册详情页：
查看相册中所有照片，缩放预览，全屏查看。
上传新照片，编辑照片标题、描述和标签。
使用搜索功能快速查找特定照片。

## 贡献和反馈
我们欢迎任何形式的贡献，包括代码、文档和测试用例。
请将问题和建议提交到项目 GitHub 仓库的 Issues 页面，或发送邮件至 [1292210712@qq.com]。
## 许可证
本项目代码遵循 MIT 许可证。
## 致谢
感谢熬夜还在奋战的我。
## 寄语  
时间有点儿着急，这只是初版，后续我会跟进以及完善，包括但不限于美化+数据库链接
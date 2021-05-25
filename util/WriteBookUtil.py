# 使用前首先要引入os模块，一个程序文件引入一次就可以了，下面默认都已引入os模块
import os

dir_path = "Books/"


# 写入图书详情工具类
class WriteUtil(object):
    @staticmethod
    def write_info(img_url, book_name, source_name, author_name, near_chapter_name):
        if book_name is None or book_name == "":
            return "图书名字为空"
        elif source_name is None or source_name == "":
            return "来源为空"
        elif author_name is None or author_name == "":
            return "作者姓名为空"
        elif near_chapter_name is None or near_chapter_name == "":
            return "最新章节为空"
        else:
            # 读取相关文件夹，没有则创建，有则跳过
            path = dir_path+"/"+source_name+"/"+book_name
            folder = os.path.exists(path)
            if not folder:
                print("未找到相关文件或文件夹")
                os.makedirs(path)
                print("创建相关文件或文件夹")
            # 创建并写入图书详情文件
            file = open(path + "/info.json", 'w')
            file.writelines("book_name:"+book_name)
            file.writelines("author_name:"+author_name)
            file.writelines("source_name:"+source_name)
            file.writelines("near_chapter_name:"+near_chapter_name)
            file.close()
            return '写入图书详情成功'





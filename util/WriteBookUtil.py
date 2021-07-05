#!/usr/bin/python3
# 使用前首先要引入os模块，一个程序文件引入一次就可以了，下面默认都已引入os模块
import os
import re
import requests

dir_path = "/home/clonebook_application/books_save"


# 写入图书详情工具类
class WriteUtil(object):
    @staticmethod
    def write_info(img_url, book_name, source_name, author_name, near_chapter_name, book_about):
        global pic
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
            file = open(path + "/info.json", 'w', encoding="utf-8")
            str = '{"book_name":"'+book_name+'","author_name":"'+author_name+'","source_name":"'+source_name+'","near_chapter_name":"'+near_chapter_name+'","book_about":"'+book_about+'"}'
            file.writelines(str)
            file.close()
            if os.path.exists(path):
                try:
                    pic = requests.get(img_url)
                except requests.exceptions.ConnectionError:
                    print('图片无法下载')
                # 保存图片路径
                fp = open(path + "/book_info.jpg", 'wb')
                fp.write(pic.content)
                fp.close()
                print('图片下载 保存完成')

            return '写入图书详情成功'

    @staticmethod
    def write_chapter(path, chapter_name, index, content_list):
        save_path = dir_path+"/"+path
        if chapter_name == "" or len(content_list) == 0:
            return "章节名字/内容为空"
        elif os.path.exists(save_path):
            # 替换特殊字符防止写入失败
            chapter_name = re.sub("[<>/\\\|:\"*?]", "-", chapter_name)
            # 第几章正则表达式去除掉，然后在开头加上章节数字：
            chapter_name = re.sub("(第[\u4e00-\u9fa5\u767e\u5343\u96f6]{1,10}章)|(第[0-9]{1,10}章)", "", chapter_name)
            chapter_name = str(index)+"_"+chapter_name
            file_name = save_path + "/"+chapter_name+".txt"
            file = open(file_name, 'w', encoding="utf-8")
            for index in range(len(content_list)):
                file.writelines(content_list[index])
                file.writelines("\n")
            file.close()
            return chapter_name+"    写入成功"
        else:
            return "保存路径不正确 :" + save_path

    @staticmethod
    def get_chapter_sum(path):
        chapter_path = dir_path+"/"+path
        folder = os.path.exists(chapter_path)
        if not folder:
            print("未找到相关文件或文件夹")
            os.makedirs(chapter_path)
            print("创建相关文件或文件夹")
            return 0
        else:
            file_list = os.listdir(chapter_path)
            return len(file_list)

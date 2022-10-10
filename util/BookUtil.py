# coding=UTF-8
# !/usr/bin/python3
# 使用前首先要引入os模块，一个程序文件引入一次就可以了，下面默认都已引入os模块
import os
import re
import requests
from lxml import etree
import json


dir_path = "/home/ubuntu/clone_project/clone_source/books_save"


# 图书工具类
class BookUtil(object):
    @staticmethod
    def write_info(img_url, book_name, source_name, author_name, near_chapter_name, book_about):
        global pic
        if not all([book_name, source_name, author_name, book_about]):
            return "参数不完整"
        # 读取相关文件夹，没有则创建，有则跳过
        path = dir_path + "/" + source_name + "/" + book_name
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        json_info = {
            'book_name': book_name,
            'author_name': author_name,
            'source_name': source_name,
            'near_chapter_name': near_chapter_name,
            'book_about': book_about
        }
        # 创建并写入图书详情文件
        with open(path + "/info.json", 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_info, ensure_ascii=False))

        try:
            pic = requests.get(img_url)
        except requests.exceptions.ConnectionError:
            print('图片无法下载')
            return '图片无法下载'
        # 保存图片路径
        fp = open(path + "/book_info.jpg", 'wb')
        fp.write(pic.content)
        fp.close()
        print('图片下载 保存完成')

        return '写入图书详情成功'

    @staticmethod
    def write_chapter(path, chapter_name, index, content_list):
        save_path = dir_path + "/" + path
        if chapter_name == "" or len(content_list) == 0:
            return "章节名字/内容为空"
        elif os.path.exists(save_path):
            # 替换特殊字符防止写入失败
            chapter_name = re.sub("[<>/\\\|:\"*?]", "-", chapter_name)
            # 第几章正则表达式去除掉，然后在开头加上章节数字：
            chapter_name = re.sub("(第[\u4e00-\u9fa5\u767e\u5343\u96f6]{1,10}章)|(第[0-9]{1,10}章)", "", chapter_name)
            chapter_name = str(index) + "_" + chapter_name
            file_name = save_path + "/" + chapter_name + ".txt"
            file = open(file_name, 'w', encoding="utf-8")
            for index in range(len(content_list)):
                file.writelines(content_list[index])
                file.writelines("\n")
            file.close()
            return chapter_name + "    写入成功"
        else:
            return "保存路径不正确 :" + save_path

    @staticmethod
    def get_chapter_sum(path):
        chapter_path = dir_path + "/" + path
        folder = os.path.exists(chapter_path)
        if not folder:
            print("未找到相关文件或文件夹")
            os.makedirs(chapter_path)
            print("创建相关文件或文件夹")
            return 0
        else:
            file_list = os.listdir(chapter_path)
            return len(file_list)

    @staticmethod
    def get_hot_books():
        books = []
        # 从起点获取热门小说
        url = "https://www.qidian.com/rank/collect/"
        html = etree.HTML(requests.get(url).content.decode('utf-8'))
        # 获取所有页码
        urls = html.xpath('//*[@class="lbf-pagination-item"]/a/@href')
        # 查重去空
        pages = []
        for i in range(len(urls)):
            if urls[i] != "javascript:;":
                is_repeat = None
                for j in range(len(pages)):
                    if urls[i] == urls[j]:
                        is_repeat = 1
                        break
                if not bool(is_repeat):
                    pages.append(urls[i])
        for index in range(len(pages)):
            # 请求每页，获取每页图书名字
            url = "https:" + pages[index]
            html = etree.HTML(requests.get(url).content.decode('utf-8'))
            book_names = html.xpath('//*[@id="book-img-text"]/ul/li/div[2]/h2/a/text()')
            author_names = html.xpath('//*[@id="book-img-text"]/ul/li/div[2]/p[1]/a[1]/text()')
            length = 0
            if len(book_names) > len(author_names):
                length = len(book_names)
            else:
                length = len(author_names)
            for k in range(length):
                book_info = {'bookName': book_names[k], 'authorName': author_names[k]}
                book_json = json.dumps(book_info)
                books.append(book_json)
        return books

    @staticmethod
    def update_book_list(path,books_info):
        # 列表写入到文件内,先查重再写入
        with open(path, "r+") as lines:
            for line in lines:
                for index in range(len(books_info)):
                    if line == books_info[index]:
                        books_info.remove(books_info[index])
                        break
            for index in range(len(books_info)):
                lines.write("\n")
                lines.write(str(books_info[index]))



# coding=UTF-8
#!/usr/bin/python3
import re

from source.www_81zw_com import Source_81zw
from source.www_gebiqu_com import Source_gebiqu
from util.BookUtil import BookUtil

# 来源字典创建
source_web = {1: "http://www.gebiqu.com/",
              2: "https://www.81zw.com/"}
# 图书链接文件
bookUrl_path = "/home/ubuntu/clone_project/clone_source/book_update/bookUrl.txt"

def downloadBook(book_url):
    source = None
    for key in source_web.keys():
        m = re.search(source_web.get(key), book_url)
        if m:
            if key == 1:
                source = Source_gebiqu()
                break
            if key == 2:
                source = Source_81zw()
                break

    # 不为空直接开始调用爬取
    if source:
        source.clone_book(book_url)
    else:
        print("未找到源，爬取失败")


if __name__ == '__main__':
    # 获取起点最热门收藏书籍，更新到json内
    books = BookUtil.get_hot_books()
    books_info = []
    for index in range(len(books)):
        print(books[index])
        for key in source_web.keys():
            if key == 1:
                values = Source_gebiqu().search_book(books[index])
                if values is not None:
                    books_info.append(values)
                    break
            elif key == 2:
                values = Source_81zw().search_book(books[index])
                if values is not None:
                    books_info.append(values)
                    break

    BookUtil.update_book_list(bookUrl_path, books_info)

    # 根据列表爬取图书
    with open(bookUrl_path) as lines:
        for line in lines:
            downloadBook(line)



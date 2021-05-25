#!/usr/bin/python3
from source.www_gebiqu_com import Source
import re

# 来源字典创建
source_web = {1: "http://www.gebiqu.com/", 2: "www.baidu.com"}


# 读取文件流，匹配需要查找的图书链接，返回相应的网站源ID
def get_source_id(book_url):
    if book_url == "":
        return -1
    else:
        for key in source_web.keys():
            m = re.search(source_web.get(key), book_url)
            if m:
                return key
        return -1


if __name__ == '__main__':
    book_url = "http://www.gebiqu.com/biquge_127230/"
    source = None
    for key in source_web.keys():
        m = re.search(source_web.get(key), book_url)
        if m:
            if key == 1:
                source = Source()
                break

    # 不为空直接开始调用爬取
    if source:
        source.clone_book(book_url)
    else:
        print("未找到源，爬取失败")


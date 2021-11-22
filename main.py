# coding=UTF-8
#!/usr/bin/python3
from source.www_81zw_com import Source_81zw
from source.www_gebiqu_com import Source_gebiqu
import re

# 图书链接文件
bookUrl_path = "/home/clonebook_application/book_update/bookUrl.txt"

# 来源字典创建
source_web = {1: "http://www.gebiqu.com/",
              2: "https://www.81zw.com/"}


# 爬取图书
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
    with open(bookUrl_path) as lines:
        for line in lines:
            downloadBook(line)

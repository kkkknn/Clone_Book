from source.www_gebiqu_com import Source

# 来源字典创建
source_web = {1: "http://www.gebiqu.com/", 2: "www.baidu.com"}


# 读取文件流，匹配需要查找的图书链接，返回相应的网站源ID
def get_source_id(book_url):
    if book_url == "":
        return -1
    else:
        # todo 读取文件并进行比对
        return 1


if __name__ == '__main__':
    source = None
    source_id = get_source_id("www.xxxx.xxx/ssss")
    if source_id in source_web.keys():
        if source_web[source_id] == "http://www.gebiqu.com/":
            source = Source()
    # 不为空直接开始调用爬取
    if source:
        source.clone_book_info("http://www.gebiqu.com/biquge_127230/")
        source.get_chapter_urls()
        source.clone_chapter_content()
    print('PyCharm')


import requests
from util.CloneUtil import CloneUtil
from util.WriteBookUtil import WriteUtil
from lxml import etree


class Source(CloneUtil):
    def get_chapter_urls(self):
        print("获取到了")

    def clone_book_info(self, book_url):
        img_url = None
        book_name = None
        author_name = None
        source_name = None
        near_chapter_name = None
        html = etree.HTML(requests.get(book_url).content)

        content = html.xpath('//*[@id="info"]/h1/text()')
        if len(content) == 1:
            book_name = content[0]

        content = html.xpath('//*[@id="info"]/p/text()')
        if len(content) == 1:
            replace = content[0].split(':')
            author_name = replace[1]

    def clone_chapter_content(self):
        print("获取到了222")

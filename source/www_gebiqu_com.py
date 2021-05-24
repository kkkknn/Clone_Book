from util.CloneUtil import CloneUtil
from util.WriteBookUtil import WriteUtil
import requests
import re
from bs4 import BeautifulSoup


class Source(CloneUtil):
    def get_chapter_urls(self):
        print("获取到了")

    def clone_book_info(self, book_url):
        img_url = None
        book_name = None
        author_name = None
        source_name = None
        near_chapter_name = None
        html = requests.get(book_url).content
        html.find()
        print(".text")

    def clone_chapter_content(self):
        print("获取到了222")

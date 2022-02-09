# coding=UTF-8
#!/usr/bin/python3
import requests
from lxml import etree
from requests.adapters import HTTPAdapter

from util.CloneUtil import CloneUtil
from util.BookUtil import BookUtil

source_url = "www.81zw.com"
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))
connectTimeOut = 5
readTimeOut = 10


class Source_81zw(CloneUtil):


    def search_book(self, json_str):
        value = eval(json_str)
        name = value['bookName']
        author = value['authorName']
        url = "https://www.81zw.com/search.php?q="+value['bookName']
        try:
            html = etree.HTML(s.get(url, timeout=(connectTimeOut,readTimeOut)).content.decode('utf-8'))
        except requests.exceptions.RequestException as e:
            print(e)
            return
        # 解析请求对比返回是否一致
        req_authors = html.xpath('/html/body/div[3]/div/div[2]/div/p[1]/span[2]/text()')
        req_urls = html.xpath('/html/body/div[3]/div/div[2]/h3/a/@href')

        ret_url = None
        for index in range(len(req_authors)):
            if author == req_authors[index]:
                ret_url = 'https://'+source_url+req_urls[index]
                break
        # 最终返回图书链接
        return ret_url

    @staticmethod
    def clone_book(book_url):
        # 来源网址
        source_name = source_url
        try:
            html = etree.HTML(s.get(book_url, timeout=(connectTimeOut,readTimeOut)).content.decode('utf-8'))
        except requests.exceptions.RequestException as e:
            print(e)
            return
        # 写入图书名字
        content = html.xpath('//*[@id="info"]/h1/text()')
        book_name = content[0]
        # 写入作者名字
        content = html.xpath('//*[@id="info"]/p[1]/text()')
        replace = content[0].split('：')
        author_name = replace[1]
        # 最新章节名字
        content = html.xpath('//*[@id="info"]/p[4]/a/text()')
        near_chapter_name = content[0]
        # 图书封面图片
        content = html.xpath('//*[@id="fmimg"]/img/@src')
        img_url = content[0]
        # 图书简介
        content = html.xpath('//*[@id="intro"]/text()')
        book_about = content[0]

        value = BookUtil.write_info(img_url, book_name, source_name, author_name, near_chapter_name, book_about)
        print(value)

        # 获取章节列表
        chapter_list = []
        name_list = html.xpath('//*[@id="list"]/dl/dt[1]//following-sibling::*/a/text()')
        url_list = html.xpath('//*[@id="list"]/dl/dt[1]//following-sibling::*/a/@href')

        for index in range(len(name_list)):
            info_list = [name_list[index], url_list[index]]
            chapter_list.append(info_list)
        print(len(chapter_list))

        # 获取目录内最新章节
        root_path = source_url+"/"+book_name+"/chapters"
        chapter_sum = BookUtil.get_chapter_sum(root_path)
        start_index = (chapter_sum-1) if chapter_sum > 0 else 0
        for index in range(len(chapter_list)):
            if index >= start_index:
                # 获取章节内容 延迟卡在这里
                url = "https://" + source_url + chapter_list[index][1]
                try:
                    chapter_html = etree.HTML(s.get(url, timeout=(connectTimeOut,readTimeOut)).content.decode('utf-8'))
                except requests.exceptions.RequestException as e:
                    print(e)
                    break
                content_str_list = chapter_html.xpath('//div[@id="content"]/text()')
                for content_str in content_str_list:
                    content_str.replace(u'\x20', u'\n').replace(u'\u3000', ' ')
                str2 = BookUtil.write_chapter(root_path, chapter_list[index][0],index, content_str_list)
                print(str2)


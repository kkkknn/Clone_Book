# coding=UTF-8
#!/usr/bin/python3
import abc


# 爬取小说网站工具抽象类
class CloneUtil(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def clone_book(self, book_url):
        raise AttributeError('子类必须实现get_book_info')

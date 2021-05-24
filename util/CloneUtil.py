import abc


# 爬取小说网站工具抽象类
class CloneUtil(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_chapter_urls(self):
        raise AttributeError('子类必须实现get_chapter_urls')

    @abc.abstractmethod
    def clone_book_info(self, book_url):
        raise AttributeError('子类必须实现get_book_info')

    @abc.abstractmethod
    def clone_chapter_content(self):
        raise AttributeError('子类必须实现get_chapter_content')

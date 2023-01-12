from model.crud import Article as A
from collections import namedtuple
from datetime import datetime
from markupsafe import Markup
from ads.adcash import *


Article = namedtuple("Article", 
        ["id", "title", "author", "date", "desc", "text"])


class Articles:


    def __init__(self):
        self.banners   = [BANNER_1, BANNER_2, BANNER_3]
        self.delimiter = "</p><p>"
        self.articles  = A()


    def read(self, id = None):
        articles = []
        for article in self.articles.read(id = id):

            text, title, desc = self.decode(article)
            text              = self.inject(text)

            id      = article[0]
            title   = Markup(title)
            author  = article[2]
            date    = datetime.strftime(article[3], "%B %d, %Y")
            desc    = Markup(desc)
            text    = Markup(text)

            article = Article(id, title, author, date, desc, text)
            articles.append(article)

        return sorted(articles, reverse = True, key = lambda a: a.id)



    def decode(self, article):
        text, title, desc = article[-1], article[1], article[-2]
        text, title, desc = text.replace("$$$", "\'"), title.replace("$$$", "\'"), desc.replace("$$$", "\'")
        text, title, desc = text.replace("Xxx", "\'"), title.replace("Xxx", "\'"), desc.replace("Xxx", "\'")
        text, title, desc = text.replace("xxx", "\'"), title.replace("xxx", "\'"), desc.replace("xxx", "\'")
        text, title, desc = text.replace("###", "\""), title.replace("###",   ""), desc.replace("###", "\"")
        text, title, desc = text.replace("Qqq", "\""), title.split(" "),           desc.replace("Qqq", "\"")
        text        = text.replace("qqq", "\"")
        for e, word in enumerate(title):
            if ("Qqq" in word):
                word = word.replace("Qqq", "")
                word = word.replace("qqq", "")
                if 4 <= len(word):
                    word = word.title()
                title[e] = word
        title = " ".join(title)
        return text, title, desc


    def inject(self, text):
        text  = text.split(self.delimiter)
        array = [str()] * ((len(text) - 1) + len(text))
        banner_index, text_index = 0, 0
        for i in range(len(array)):
            if not (i % 2):
                array[i] = text[text_index]
                text_index += 1
            elif (banner_index < len(self.banners)):
                array[i] = self.banners[banner_index]
                banner_index += 1
            else:
                array[i] = str()
        text = self.delimiter.join(array)
        return text

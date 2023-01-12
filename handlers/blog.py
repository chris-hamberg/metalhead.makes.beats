from handlers.articles import Articles
from flask import render_template
from flask import request
from flask import abort
from math import ceil


class Article:


    def __init__(self, id):
        self._validate(id)


    def get(self):
        return render_template("article.html", article = self._article)


    def _validate(self, id):
        try:
            articles = Articles()
            self._article = articles.read(id = int(id))[0]
        except (IndexError, ValueError):
            abort(404)


class Page:


    NUMBER = 5


    def __init__(self, page):
        self._validate(page)
        self._get_articles()
        self._set_bounds()
        self._get_pages()


    def get(self):
        html = render_template("blog.html", 
                posts = self._articles[self._lower:self._upper], 
                base_url = request.root_url, 
                prev = self._prev, _next = self._next)
        return html


    def _get_pages(self):
        number_of_pages = ceil(len(self._articles) / __class__.NUMBER) + 1
        array = list(range(number_of_pages))
        self._page %= number_of_pages
        next_page = self._page + 1
        try:
            array[next_page]
        except IndexError:
            next_page = 0
        prev_page = array[self._page - 1]
        next_page %= number_of_pages
        prev_page %= number_of_pages
        self._prev = f"blog?page={prev_page + 1}"
        self._next = f"blog?page={next_page + 1}"       


    def _validate(self, page):
        try:
            self._page = int(page)
            1 / self._page
            self._page -= 1
        except ValueError:
            abort(404)
        except ZeroDivisionError:
            self._page = 0


    def _get_articles(self):
        articles = Articles()
        self._articles = articles.read()


    def _set_bounds(self):
        page = self._page
        if (len(self._articles) < (self._page * __class__.NUMBER)):
            page = self._page %  __class__.NUMBER
        self._lower = page * __class__.NUMBER
        self._upper = self._lower + __class__.NUMBER

import sys
config = "model.config"
try:
    if (sys.argv[1:][0] == "test"):
        import model.test_config
        config = "model.conf"
except IndexError as production:
    pass
from api.analytics import AnalyticsReadInterface
from api.article import BlogCreateUpdateInterface
from api.article import BlogReadDeleteInterface

from handlers.mailing_list import MailingList
from handlers.articles import Articles
from handlers.visitor import get_data
from handlers.blog import Article
from handlers.blog import Page

from model.crud import MailingList as Email
from model.crud import FreeBeat

from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import Flask
from flask import abort

from feedwerk.atom import AtomFeed
from flask_restful import Api

from collections import namedtuple
from urllib.parse import urljoin
from datetime import datetime


app = Flask(__name__)
app.config.from_object(config)

app.config["RECAPTCHA_PUBLIC_KEY"] = "6Lc2KLoiAAAAAPO4kOMst4yjw3RC__7AypNUTm8k"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6Lc2KLoiAAAAALxo_lFU52Ry5sV9_jSZ0qdecZmF"
api = Api(app)


api.add_resource(BlogReadDeleteInterface, "/api/article/<int:id>")
api.add_resource(BlogCreateUpdateInterface, "/api/article/")
api.add_resource(AnalyticsReadInterface, "/api/analytics/")


articles = Articles()
beats    = FreeBeat()
beats    = beats.read()


Record = namedtuple("Record", ["first", "last", "email"])
Beat   = namedtuple("Beat", ["id", "link", "next", "locker_id", "locker_hash"])

beats  = [Beat(b[0], b[1], b[3], b[2], b[4]) for b in beats]


@app.before_request
def get_visitor_data(): get_data()


@app.errorhandler(404)
def http404(e): return render_template("404.html", error=str(e))


@app.errorhandler(503)
def http503(e): return render_template("503.html", error=str(e))


@app.route("/robots.txt")
def robots(): return render_template("robots.txt")


@app.route("/sitemap.xml")
def sitemap():
    a, b = list(reversed(articles.read())), [b[0] for b in beats]
    e = len(a) - 1
    return render_template("sitemap.xml", articles = a, free_beats = b,
            base_url = request.root_url, pages = int(e / 10) + 1)


@app.route("/feeds/")
def feeds():
    feed = AtomFeed(title = "MΞTALHEΔD MΛKΞS BΞΔTS RSS", feed_url = request.url,
            url = request.url_root)
    for article in articles.read()[:20]:
        ts = datetime.strptime(article.date, "%B %d, %Y")
        feed.add(article.title, content_type = "html", id = article.id,
                author = article.author, 
                url = urljoin(request.url_root, 
                        "/blog?article=" + str(article.id)),
                updated = ts, summary = article.desc, summary_type = "text",
                title_type = "text")
    return feed.get_response()


@app.route("/")
@app.route("/home")
def index():
    try:
        article = articles.read()[0]
        return render_template("home.html", article = article)
    except IndexError: abort(404)


@app.route("/blog")
def blog():
    number = request.args.get("page")
    id     = request.args.get("article")
    if id: html = Article(id).get()
    elif not number: html = Page(1).get()
    else: html = Page(number).get()
    return html


@app.route("/free-beat")
def free_beats():
    try:
        idx  = int(request.args.get("id", False)) or 1
        idx -= 1
        beat = beats[idx]
        next = f"/free-beat?id={beat.id}" if idx < len(beats) else "/home"
    except (ValueError, IndexError):
        abort(404)
    else:
        return render_template(f"free_beats.html", beat = beat, next = next)


@app.route("/mailing-list", methods=["GET", "POST"])
def mailing_list():
    
    html_form    = MailingList(request.form)
    mailing_list = Email()
    try:

        assert html_form.submit.data

        email   = html_form.email.data
        confirm = html_form.confirm.data
        first   = html_form.first.data.title()
        last    = html_form.last.data.title()

        message = " cannot exceed 255 characters."

        is_valid = (html_form.validate(), first.isalpha(), last.isalpha())
        is_valid += (len(email) <= 255, len(first) <= 255, len(last) <= 255)

        if not first.isalpha():
            html_form.first.errors.append("First name must be real.")

        if not last.isalpha():
            html_form.last.errors.append("Last name must be real.")

        if not len(email) <= 255 or not len(confirm) <= 255:
            html_form.email.errors.append("Email" + message)
            html_form.confirm.errors.append("Email" + message)

        if not len(first) <= 255:
            html_form.first.errors.append("First name" + message)

        if not len(last) <= 255:
            html_form.last.errors.append("Last name" + message)

        assert all(is_valid)

        record = Record(first, last, html_form.email.data)

        created = mailing_list.create(record)

        if not created:
            html_form.email.errors.append(f"{email} is already subscribed.")
            html_form.confirm.errors.append(f"{email} is already subscribed.")
            assert created
        else:
            return redirect("/success")

    except (AssertionError, AttributeError):
        return render_template("mailing_list.html", html_form = html_form)


@app.route("/success")
def success():
    base_url = request.root_url
    return render_template("success.html", base_url = base_url)


if __name__ == "__main__":
    app.run(host = app.config["HOST"],
            port = app.config["PORT"],
            debug = app.config["DEBUG"])

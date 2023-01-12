from flask_restful import abort, Api, fields, marshal_with
from flask_restful import reqparse, Resource
from types import SimpleNamespace
from model.crud import Article
from datetime import datetime
import hashlib


HASH = ("8464737df688ea263cc34eef8be130a6af9c0d3aa8fa16501a87a404a3f"
        "26e7d468ea4dae4ccd58263556f0c47bc64632ca42a457f2cadf245cd87"
        "f1240e653d")


blog_post = {"id"     : fields.Integer,
             "title"  : fields.String,
             "author" : fields.String,
             "date"   : fields.DateTime,
             "desc"   : fields.String,
             "article": fields.String}


articles = Article()


def authenticated(password):
    password = password.encode()
    auth = hashlib.sha512(password).hexdigest() == HASH
    if auth:
        return True
    else:
        message = f"You are not authorized to access this resource."
        abort(401, message = message)


class BlogReadDeleteInterface(Resource):


    @marshal_with(blog_post)
    def get(self, id):
        data, code = self._fetch(id)
        parser = BlogCreateUpdateInterface()
        json = parser._mutable(data)
        return json, code


    @marshal_with(blog_post)
    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("password", type = str, required = True,
                help = "Password is required.")
        args = parser.parse_args()
        password = args.get("password")

        if authenticated(password):
            articles.delete(id)
            return "", 204


    def _fetch(self, id):
        try:
            results = articles.read()
            article = list(filter(lambda a: a[0] == id, results))[0]
            return article, 200
        except IndexError as not_found:
            message = f"Blog post {id} does not exist."
            abort(404, message = message)



class BlogCreateUpdateInterface(Resource):


    @marshal_with(blog_post)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title",    type = str, required = True, 
                help = "A title is required.")
        parser.add_argument("author",   type = str, required = True,
                help = "The author's name is required.")
        parser.add_argument("desc",     type = str, required = True,
                help = "The article description is required.")
        parser.add_argument("article",  type = str, required = True,
                help = "The article is required.")
        parser.add_argument("password", type = str, required = True,
                help = "Password is required")
        article = parser.parse_args()

        password = article.get("password")
        if authenticated(password):

            title, author = article.get("title"), article.get("author")
            desc, article = article.get("desc"), article.get("article")
            article = (title, author, desc, article)

            json = articles.create(article)

            if json:
                return json, 201
            else:
                abort(409, message = f"Article '{title}' failed to be created.")


    @marshal_with(blog_post)
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument("password", type = str, required = True,
                help = "Password is required.")
        parser.add_argument("id",       type = int, required = True,
                help = "The article id is required.")
        parser.add_argument("title",    type = str)
        parser.add_argument("author",   type = str)
        parser.add_argument("desc",     type = str)
        parser.add_argument("article",  type = str)
        args = parser.parse_args()

        password = args.get("password")
        if authenticated(password):

            try:
                id = args["id"]
                article = articles.read(id=id)[0]
                article = self._mutable(article)
            except (KeyError, AssertionError) as expectation_failed:
                message = "Blog post id is required to update a post."
                abort(417 , message = message)

            article.update({"title"   : args.title   or article.get("title"  )})
            article.update({"author"  : args.author  or article.get("author" )})
            article.update({"desc"    : args.desc    or article.get("desc"   )})
            article.update({"article" : args.article or article.get("article")})

            articles.update(article)
        
            article = articles.read(id=id)[0]
            json = self._mutable(article)
        
            return json, 200


    def _mutable(self, article):
        return {"id"     : article[0],
                "title"  : article[1],
                "author" : article[2],
                "date"   : article[3],
                "desc"   : article[4],
                "article": article[5]}

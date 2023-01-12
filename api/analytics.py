from flask_restful import abort, Api, fields, marshal_with
from flask_restful import reqparse, Resource
from types import SimpleNamespace
from model.crud import Analytics
from datetime import datetime
import hashlib


HASH = ("8464737df688ea263cc34eef8be130a6af9c0d3aa8fa16501a87a404a3f"
        "26e7d468ea4dae4ccd58263556f0c47bc64632ca42a457f2cadf245cd87"
        "f1240e653d")


analytic = {"ip"        : fields.String,
            "platform"  : fields.String,
            "browser"   : fields.String,
            "city"      : fields.String,
            "country"   : fields.String,
            "continent" : fields.String,
            "bot"       : fields.Boolean,
            "visits"    : fields.Integer,
            "created"   : fields.DateTime,
            "last_visit": fields.DateTime}


analytics = Analytics()


def authenticated(password):
    password = password.encode()
    auth = hashlib.sha512(password).hexdigest() == HASH
    if auth:
        return True
    else:
        message = f"You are not authorized to access this resource."
        abort(401, message = message)


class AnalyticsReadInterface(Resource):


    @marshal_with(analytic)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("password", type = str, required = True,
                help = "Password is required")
        args = parser.parse_args()
        password = args.get("password")
        if authenticated(password):
            data = analytics.read()
            json = [{
                "ip"        : dat[0],
                "platform"  : dat[1],
                "browser"   : dat[2],
                "city"      : dat[3],
                "country"   : dat[4],
                "continent" : dat[5],
                "bot"       : dat[6],
                "visits"    : dat[7],
                "created"   : dat[8],
                "last_visit": dat[9]
                } for dat in data]
            return json, 200

from model.crud import Analytics
from flask import request
import httpagentparser
import requests


analytics = Analytics()


def valid(request):
    prohibited = ["static", "api", "feeds", "sitemap", "robots"]
    for term in prohibited:
        if term in request.url:
            return False
    return True


def get_data():
    if not valid(request):
        return False
    data = httpagentparser.detect(request.headers.get("User-Agent"))
    if (request.access_route): ip = request.access_route[0]
    else: ip = request.remote_addr
    ip  = "71.91.98.154" if ip == "127.0.0.1" else ip
    url = "https://www.iplocate.io/api/lookup/" + ip
    r   = requests.get(url)
    try:
        platform = data.get("platform").get("name")
        browser  = data.get("browser").get("name")
    except AttributeError:
        platform = "Unknown"
        browser  = "Unknown"
    try:
        city      = r.json().get("city")
        country   = r.json().get("country")
        continent = r.json().get("continent")
    except AttributeError:
        city      = "Unknown"
        country   = "Unknown"
        continent = "Unknown"
    bot = data.get("bot")
    data = (ip, platform, browser, city, country, continent, bot)
    analytics.create(data)

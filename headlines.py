import json
import urllib
import urllib2
import feedparser
from flask import Flask, render_template, request

app = Flask(__name__)
RSS_FEEDS = {'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'iol': 'http://www.iol.co.za/cmlink/1.640', 
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'bbc': 'http://feeds.bbci.co.uk/news/rss.xml'}
DEFAULTS = {'publication': 'cnn', 'city': 'Babol, IR'}


@app.route("/")
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html", articles=articles, weather=weather)


def get_news(query):
    if query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/" \
                  "weather?q={}&units=metric&appid=530cbf9555e6349e36c8d93ac3274ef6"
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'], 'country': parsed['sys']['country']}
    return weather


if __name__ == "__main__":
    app.run(port=80, debug=True)

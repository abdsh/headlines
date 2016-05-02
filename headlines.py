import feedparser
from flask import Flask, render_template, request

app = Flask(__name__)
RSS_FEEDS = {'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "cnn"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    articles = feed['entries']
    return render_template("home.html", articles=articles)

if __name__ == "__main__":
    app.run(port=80, debug=True)
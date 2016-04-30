import feedparser
from flask import Flask, render_template
app = Flask(__name__)
RSS_FEEDS = {'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}


@app.route("/")
@app.route("/<publication>")
def get_news(publication="cnn"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    articles = feed['entries']
    return render_template('home.html', articles=articles)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
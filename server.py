import crochet
crochet.setup() 

from flask import Flask
from scrapy.crawler import CrawlerRunner

from estate_browser import EstateSpider
from database import DB
import os

app = Flask("Estate list")
output_data = []
crawl_runner = CrawlerRunner()


def html_prefix():
    return """<html><head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Estates</title>
    </head><body>"""


def style():
    style = ""
    with open("style.css", "r") as f:
        style = f.read()
        f.close
    return "<style>"+style+"</style>"


def read_results_from_db(db_name = "estates.db"):
    db = DB(db_name)
    db.create_table()
    table = "<table><tr><th>Id</th><th>Title</th><th>Image</th></tr>"
    for row in db.cur.execute("SELECT * FROM estates"):
        table = table + "<tr><td>%s</td><td>%s</td><td><img src ='%s' width=50px></td></tr>" % row
    table = table + "</table>"
    return html_prefix() + table + style() + "</body></html>"


@app.route("/")
def scrape():
    scrape_with_crochet()
    return read_results_from_db()


@crochet.wait_for(timeout=60.0)
def scrape_with_crochet():
    eventual = crawl_runner.crawl(EstateSpider)
    return eventual


if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
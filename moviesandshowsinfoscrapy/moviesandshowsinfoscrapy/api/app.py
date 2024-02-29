from flask import Flask, request
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy import signals
import time
from moviesandshowsinfoscrapy.service.tasteio import get_tasteio
from moviesandshowsinfoscrapy.service.imdb import get_top_ten_this_week
from moviesandshowsinfoscrapy.spiders.cleganespider import CleganeSpider
import crochet

crochet.setup()
app = Flask(__name__)
crawl_runner = CrawlerRunner()
scraped_data = []


@app.route('/v1/tasteio', methods=['GET'])
def tasteio_all():
    """ Fetches Taste.io data for all categories """
    try:
        limit = request.args.get('limit', default=5, type=int)
        return get_tasteio(limit=limit)

    except Exception as e:
        return f'Error fetching Taste.io data: {str(e)}'


@app.route('/v1/tasteio/<category>', methods=['GET'])
def tasteio_category(category):
    """ Fetches Taste.io data for a specific category """
    try:
        limit = request.args.get('limit', default=5, type=int)
        return get_tasteio(category, limit)

    except Exception as e:
        return f'Error fetching Taste.io data for category "{category}": {str(e)}'


@app.route('/v1/imdb', methods=['GET'])
def imdb():
    """ Fetches IMDb's top ten movies/shows for the current week """
    try:
        return get_top_ten_this_week()

    except Exception as e:
        return f'Error fetching IMDb data: {str(e)}'


@app.route('/v1/tasteio/<category>/info', methods=['GET'])
def tasteio_info(category):
    """ Scrapes additional information from Taste.io for a specific category """
    global scraped_data
    scraped_data = []
    try:
        scrape_with_crochet(category)
        time.sleep(2)
        return f'{scraped_data}'

    except Exception as e:
        return f'Error scraping data for category "{category}": {str(e)}'


@crochet.run_in_reactor
def scrape_with_crochet(category):
    """ Initiates web scraping using Scrapy with Crochet """
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    return crawl_runner.crawl(CleganeSpider, scraped_data=scraped_data, category=category)


def _crawler_result(item):
    """ Callback function to handle scraped items """
    scraped_data.append(item)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

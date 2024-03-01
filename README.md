## Movies and Shows Info Scrapy
This Python project, created for non-commercial educational purposes, aims to build a Flask API that scrapes movie and TV show information from popular 
websites using various scraping approaches.

## Requirements
* Python
* Scrapy
* Flask
* Crochet
* Requests
* Uncurl

## Getting Started:
* Install all dependencies
* Start the flask application: run `app.py` on `moviesandshowsinfoscrapy/api`
* Open a Browser
* Open a web browser and visit http://localhost:5000/v1/imdb or any other available API endpoint (described below) to interact with the API.

## APIs

### /v1/imdb
Fetches information about the top 10 movies and TV shows on IMDb for the current week.

``` json
[
    {
    "category": "TV Series",
    "genre": "Crime, Drama, Mystery",
    "id": "tt2356777",
    "img_url": "https://m.media-amazon.com/images/M/MV5BNTEzMzBiNGYtYThiZS00MzBjLTk5ZWItM2FmMzU3Y2RjYTVlXkEyXkFqcGdeQXVyMjkwOTAyMDU@._V1_.jpg",
    "name": "True Detective",
    "ranking": 1,
    "rating": 8.9
  },
  {
    "category": "Movie",
    "genre": "Biography, Drama, History",
    "id": "tt15398776",
    "img_url": "https://m.media-amazon.com/images/M/MV5BMDBmYTZjNjUtN2M1MS00MTQ2LTk2ODgtNzc2M2QyZGE5NTVjXkEyXkFqcGdeQXVyNzAwMjU2MTY@._V1_.jpg",
    "name": "Oppenheimer",
    "ranking": 2,
    "rating": 8.4
  },
    // ... (up to 10 items)
]
```

### /v1/tasteio
Retrieves  movies and TV shows from Taste.io website for the following categories:
coming-soon, new-releases, comedy, romance, science-fiction and war.

``` json
{
  "comedy": [
    {
      "category": "tv",
      "description": "It's 1993 and Ted the bear's moment of fame has passed, leaving him living with his best friend[...]",
      "genre": [
        "Comedy"
      ],
      "name": "ted",
      "poster_image": "/cPn71YFDENH0JkWUezlsLyWmLfN.jpg",
      "title_image": "/2ZAeXAV3aQyi2VQksRAfMChjeFD.jpg",
      "trailer_key": "aq2Vt7OvQG0",
      "trailer_site": "YouTube"
    }
  ],
  "science-fiction": [
    {
      "category": "movies",
      "description": "Brought back to life by an unorthodox scientist, a young woman runs off [...]",
      "genre": [
        "Science Fiction",
        "Romance",
        "Comedy",
        "Drama",
        "Fantasy"
      ],
      "name": "Poor Things",
      "poster_image": "/kCGlIMHnOm8JPXq3rXM6c5wMxcT.jpg",
      "title_image": "/8LnjpwfZOSGOZUIE1uX54RXGlfR.jpg",
      "trailer_key": "-EfYJWRw2FM",
      "trailer_site": "YouTube"
    }
  ],
  //... (every category)
}
```

### /v1/tasteio/{category}
Filters the `/v1/tasteio` response based on a specific category provided as a URL path parameter.

For both tasteio APIs, you can specify the quantity of items that will be returned by adding the query parameter `?limit=N`, 
if no limit is specified, the default value of 5 is used.

``` json
{
  "romance": [
    {
      "category": "tv",
      "description": "After spending graduation night together, Emma and Dexter go their separate ways \u2014 but their lives remain intertwined.",
      "genre": [
        "Drama",
        "Romance"
      ],
      "name": "One Day",
      "poster_image": "/smBWt8rHCCavV88C5gQVjh0NUFa.jpg",
      "title_image": null,
      "trailer_key": "WlopfWYGBh4",
      "trailer_site": "YouTube"
    }
  ]
}
```

### /v1/tasteio/{category}/info
Starts a Scrapy Crawler to extract detailed information from individual movie/TV show pages listed in a specified 
category page on Tasteio's website.

``` json
[
{"name": "Through My Window 3: Looking at You", 
"description": ""After the events of the summer [...]",
"cast": "Clara Galle, Julio Peña, Natalia Azahara,[...]"},
//... (other movies and shows)
] 
```

## Curl convertion to Request object
The  `curl_manager.py` file provides functions to handle `curl` operations:

- `clean_curl_cmd` prepares a `curl` command for conversion by the `uncurl` library.
- `convert_to_request` utilizes `uncurl` to transform the `curl` command into a Python `Request` object.


## Flask x Scrapy integration
Integrating Flask and Scrapy can be challenging due to their different execution models: 

Flask follows a synchronous model, when a request comes in, Flask processes it sequentially. Scrapy, on the other hand, is asynchronous. 
It can send multiple requests concurrently and process them as responses arrive.

Combining these two models can be tricky because Flask expects synchronous behavior, while Scrapy operates asynchronously.

`Crochet` is a library that simplifies Flask-Scrapy integration by enabling you to run Scrapy spiders from within a Flask application.

Code snippet showing the integration using crochet:
``` python
from flask import Flask, request
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy import signals
from moviesandshowsinfoscrapy.spiders.cleganespider import CleganeSpider
import crochet

crochet.setup()
app = Flask(__name__)
crawl_runner = CrawlerRunner()
scraped_data = []

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
```
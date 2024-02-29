import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class CleganeSpider(scrapy.Spider):
    name = "cleganespider"
    allowed_domains = ["taste.io"]
    start_urls = ["https://www.taste.io/browse/new-releases"]

    def start_requests(self):
        """ Yields the new-releases page from taste.io """
        try:
            yield scrapy.Request(url="https://www.taste.io/browse/"+f'{self.category}', callback=self.crawler_parse)

        except Exception as e:
            return {
                "message": "An exception was caught during the execution of the program",
                "error": f'{e}'
            }

    def crawler_parse(self, response):
        """ A crawler that gets all the movies/tv shows urls from taste.io page and follows then """
        links = response.css('a::attr(href)')
        for link in links:
            link = link.get()
            if link is not None and (link.startswith('/movie') or link.startswith('/tv')):
                url = "".join(['https://www.taste.io', link])
                yield response.follow(url=url, callback=self.tasteio_movie_tv_parse)

    def tasteio_movie_tv_parse(self, response):
        """ Receives the web pages from the crawler and gets the name, description and cast from it """
        name = response.css('h1.styles_title__wdD7h::text').get()
        description = response.css('p.m-0.text-muted::text').get()
        cast = ', '.join(response.css('.styles_people__XIO53 h4 + p span a::text').getall())

        self.scraped_data.append({
            "name": name,
            "description": description,
            "cast": cast
        })

if __name__ == '__main__':
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(CleganeSpider)
    process.start()
import scrapy
from scrapy_project.items import BookScraperItem


class BooksScraperSpider(scrapy.Spider):
    name = "books_scraper"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        self.logger.info(f"Scraping URL: {response.url}")
        books = response.css("article.product_pod")
        for book in books:
            item = BookScraperItem()
            item['title'] = book.css("h3 a::attr(title)").get()
            item['price'] = book.css("p.price_color::text").get()
            item['rating'] = book.css("p.star-rating::attr(class)").get()
            yield item
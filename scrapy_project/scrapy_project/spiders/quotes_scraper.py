import scrapy


class QuotesScraperSpider(scrapy.Spider):
    name = "quotes_scraper"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output/quotes.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_DELAY': 2,
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 1,
    }

    def parse(self, response):
        self.logger.info(f"Scraping URL: {response.url}")
        quotes = response.css("div.quote")
        for quote in quotes:
            yield {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            }
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)


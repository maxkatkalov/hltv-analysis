import scrapy


class MatchResultsSpider(scrapy.Spider):
    name = "match_results"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results"]

    def parse(self, response):
        pass

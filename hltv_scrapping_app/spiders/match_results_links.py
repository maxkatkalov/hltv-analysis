import scrapy
from scrapy.http import Response, Request


class MatchResultsLinksSpider(scrapy.Spider):
    name = "match_results_links"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results"]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response: Response, **kwargs):
        all_matches = response.css('div.result-con>a.a-reset::attr(href)').getall()
        for url in all_matches:
            yield {
                "Match link": url,
            }

        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

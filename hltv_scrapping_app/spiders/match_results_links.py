import sys

from db_app.models import HltvMatchLinks

import scrapy
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.http import Response, Request
from tortoise import Tortoise

from db_app.models import config


class MatchResultsLinksSpider(scrapy.Spider):
    name = "match_results_links"
    allowed_domains = ["www.hltv.org"]
    start_urls = ["https://www.hltv.org/results"]

    links_objects = []

    @staticmethod
    def count_stars(match_link: str, response: Response) -> tuple[str, int]:
        stars_html = response.css(
            f'a.a-reset[href="{match_link}"] div.map-and-stars>div'
        ).get()
        if stars_html is not None:
            splitted_stars_html = stars_html.split()
        else:
            splitted_stars_html = []
        if "fa-star" not in splitted_stars_html:
            return match_link, 0
        return match_link, splitted_stars_html.count("fa-star")

    @staticmethod
    async def links_bulk_create(links_objects: list[HltvMatchLinks]):
        await Tortoise.init(config)

        await HltvMatchLinks.bulk_create(links_objects, batch_size=10000)

    async def spider_closed(self, spider):
        print(
            f"Get size of links_objects: {sys.getsizeof(self.links_objects)}"
        )
        await self.links_bulk_create(self.links_objects)

    def start_requests(self):
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response: Response, **kwargs):
        all_matches_links = response.css(
            "div.result-con>a.a-reset::attr(href)"
        ).getall()
        rated_matches = [
            self.count_stars(match_rating, response)
            for match_rating in all_matches_links
        ]
        self.links_objects.extend(
            [
                HltvMatchLinks.create_new_links_instances(match_rating)
                for match_rating in rated_matches
            ]
        )

        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os
import hashlib
from urllib.parse import urljoin


class BerlinHousesSpider(scrapy.Spider):
    name = "berlin_houses"
    start_urls = ["https://home-in-berlin.de/immobilien/"]

    def parse(self, response):
        listings = response.css("div.estate-card")

        for house in listings:
            title = house.css(".news-item-title::text").get(default="").strip()
            location = house.css(".news-item-info::text").get(default="").strip()
            details = house.css(".estate-item-button-inner p strong::text").get(default="").strip()
            price = house.css(".price strong::text").get(default="").strip()
            link = urljoin("https://home-in-berlin.de", house.css("a::attr(href)").get(default="").strip())
            image = house.css(".news-item-image-slide::attr(style)").re_first(r'url\((.*?)\)')

            yield {
                "title": title,
                "location": location,
                "details": details,
                "price": price,
                "link": link,
                "image": image,
            }


def run_spider():
    collected_items = []

    process = CrawlerProcess(settings={"LOG_ENABLED": False})

    def collect_results(item, response, spider):
        collected_items.append(item)

    process.crawl(BerlinHousesSpider)
    for crawler in list(process.crawlers):
        crawler.signals.connect(collect_results, signal=scrapy.signals.item_scraped)
    process.start()

    return collected_items


if __name__ == "__main__":
    # Always output all current listings (not just new ones)
    current_items = run_spider()
    print(json.dumps(current_items, ensure_ascii=False))

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
            # Extract location from various possible elements
            location_candidates = house.css("*::text").getall()
            location = ""
            for text in location_candidates:
                if "|" in text and ("Berlin" in text or "Straße" in text):
                    location = text.strip()
                    break
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


def hash_listing(item):
    return hashlib.md5(
        (item.get("title", "") + item.get("link", "")).encode("utf-8")
    ).hexdigest()


def load_previous():
    if os.path.exists("output.json"):
        with open("output.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return {hash_listing(d): d for d in data}
            except json.JSONDecodeError:
                return {}
    return {}


def save_current(data):
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


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
    # Get current and previous listings
    current_items = run_spider()
    previous = load_previous()
    current = {hash_listing(d): d for d in current_items}
    
    # Find NEW listings only
    new_hashes = set(current.keys()) - set(previous.keys())
    new_listings = [current[h] for h in new_hashes]
    
    # Save all current listings for next time
    save_current(list(current.values()))
    
    # Output only NEW listings (for email notifications)
    for item in new_listings:
        print(json.dumps(item, ensure_ascii=False))

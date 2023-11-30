from typing import Any, List, Dict, Iterable

from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scraper.items import SrealityPropertyItem
from scrapy_playwright.page import PageMethod


class SrealityParser(Spider):
    name: str = "sreality"
    allowed_domains: List[str] = ["www.sreality.cz"]
    start_urls: List[str] = [f"https://www.sreality.cz/hledani/prodej/byty?strana={i}" for i in range(1, 26)][:2]

    def start_requests(self) -> Iterable[Request]:
        """A generator function to return next URL for scraping. 
        It uses scrapy-playwright engine to scrape dynamic websites
        and waits for the rendering of "div.dir-property-list" element
        before yielding the result.

        Returns:
            Iterable[Request]: The downloaded request.

        Yields:
            Iterator[Iterable[Request]]: asdasd
        """
        meta: Dict[str, Any] = {
            "playwright": True, 
            "playwright_page_methods": [
                PageMethod(
                    "wait_for_selector", 
                    "div.dir-property-list", 
                    timeout=10000
                )
            ]
        }

        for start_url in self.start_urls:
            yield Request(start_url, meta=meta)

    def parse(self, response):
        """Function to trigger on every URL and perform scraping.

        Args:
            response (Any): The response from download handler.

        Yields:
            scrapy.Item: Returns an key-value pair object with scraper data.
        """
        for div in response.css(".property"):
            item = ItemLoader(item=SrealityPropertyItem(), response=response)
            item.add_value("name", div.css("span.name::text").get())
            item.add_value("image_url", div.css("a:first-child").css("img::attr(src)").get())
            yield item.load_item()

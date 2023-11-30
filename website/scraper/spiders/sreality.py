from typing import Any, List, Dict, Iterable

from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scraper.items import SrealityPropertyItem
from scrapy_playwright.page import PageMethod


class SrealityParser(Spider):
    name: str = "sreality"
    allowed_domains: List[str] = ["www.sreality.cz"]
    start_urls: List[str] = [
        f"https://www.sreality.cz/hledani/prodej/byty?strana={i}" for i in range(1, 26)
    ][:2]

    def start_requests(self) -> Iterable[Request]:
        """Generator function to return the next URL for scraping.

        Uses the scrapy-playwright engine to scrape dynamic websites
        and waits for the rendering of the "div.dir-property-list" element
        before yielding the result.

        Returns:
            Iterable[Request]: The downloaded request.

        Yields:
            Any: The URL to be scraped
        """
        meta: Dict[str, Any] = {
            "playwright": True,
            "playwright_page_methods": [
                PageMethod(
                    "wait_for_selector", "div.dir-property-list", timeout=10000
                )
            ],
        }

        for start_url in self.start_urls:
            yield Request(start_url, meta=meta)

    def parse(self, response: Any) -> Iterable[SrealityPropertyItem]:
        """Function triggered on every URL to perform scraping.

        Args:
            response (scrapy.Response): The response from the download handler.

        Yields:
            SrealityPropertyItem: The scraped data as an Item object
        """
        for div in response.css(".property"):
            item = ItemLoader(item=SrealityPropertyItem(), response=response)

            try:
                name: str = div.css("span.name::text").get()
                # image_url: str = div.css("a:first-child").css("img::attr(src)").get()
                image_url: str = div.css("a:first-child img::attr(src)").get()
                item.add_value("name", name)
                item.add_value("image_url", image_url)

            except Exception as e:
                print(f"Error scraping property data: {e}")
                continue

            yield item.load_item()

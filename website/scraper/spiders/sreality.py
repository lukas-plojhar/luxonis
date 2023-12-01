"""A custom Sreality.cz scraper."""
from typing import Any, List, Dict

from scrapy import Spider
from scrapy.exceptions import DropItem
from scrapy.http import Request, Response
from scrapy.item import Item
from scrapy.loader import ItemLoader
from scraper.items import SrealityPropertyItem
from scrapy_playwright.page import PageMethod


class SrealityParser(Spider):
    """Scrapes flats from the Sreality.cz website.

    It usees the Scrapy-playwright engine for scraping
    dynamic websites.

    Attributes:
        Spider (scrapy.Spider): The Spider base class.
    """

    # Spider name for identifying the spider in Scrapy
    name: str = "sreality"

    # Allowed domains to restrict scraping to Sreality.cz
    allowed_domains: List[str] = ["www.sreality.cz"]

    # List of starting URLs for scraping
    start_urls: List[str] = [
        f"https://www.sreality.cz/hledani/prodej/byty?strana={i}" for i in range(1, 26)
    ]

    def start_requests(self) -> Request:
        """Generate URLs for scraping.

        This function uses the scrapy-playwright engine to scrape dynamic
        websites and waits for the rendering of the "div.dir-property-list"
        element before yielding the result.

        Yields:
            Iterable[Request]: The downloaded request.
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

    def parse(self, response: Response) -> Item:
        """Scrapes an item from the URL.

        Args:
            response (scrapy.Response): The response from the download handler.

        Raises:
            DropItem: If the data cannot be scraped from the response.

        Yields:
            SrealityPropertyItem: The scraped data as an Item object.
        """
        for div in response.css(".property"):
            item = ItemLoader(item=SrealityPropertyItem(), response=response)

            try:
                name: str = div.css("span.name::text").get()
                image_url: str = div.css("a:first-child img::attr(src)").get()
                item.add_value("name", name)
                item.add_value("image_url", image_url)

            except Exception as e:
                print(f"Failed to scrape property data: {e}")
                raise DropItem(f"Failed to scrape property data: {e}") from e

            yield item.load_item()

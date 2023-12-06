"""Defines pipelines for processing items after scraping by Spider."""
from connector import DatabaseConnector
from scrapy.spiders import Spider
from scrapy.exceptions import DropItem
from scraper.items import SrealityPropertyItem


class SrealityPropertyPipeline:
    """Pipeline to handle scraped property item."""

    def process_item(self, item: SrealityPropertyItem, _: Spider) -> SrealityPropertyItem:
        """Process data from the scraped item.

        Args:
            item (SrealityPropertyItem): A dictionary-like object holding
            the scraped data.
            _ (Spider): A reference to the Spider object (unused here).

        Raises:
            DropItem: If the data are not found in the item argument.

        Returns:
            SrealityPropertyItem: The original item if the property was
            successfully inserted into the database, or skips the Item if
            the property information is missing.
        """
        name: str = item.get("name")[0]
        image_url: str = item.get("image_url")[0]

        if not name or not image_url:
            raise DropItem("Missing property information.")

        DatabaseConnector().create_property(name=name, image_url=image_url)
        return item

from connector import DatabaseConnector
from psycopg2.extensions import connection, cursor
from scrapy import Item
from scrapy.exceptions import DropItem


class SrealityPropertyPipeline:
    """Pipeline to handle scraped property data and insert it into a PostgreSQL database."""

    def __init__(self) -> None:
        """Constructor for the class."""
        self._connection: connection = None
        self._cursor: cursor = None

    def process_item(self, item, _) -> Item:
        """Extracts the property name and image URL from the item, validates the data,
        and inserts it into the database.

        Args:
            item (scrapy.Item): A dictionary-like object holding the scraped
            data.
            _ (scrapy.Spider): A reference to the Spider object (unused here).

        Returns:
            scrapy.Item: The original item if the property was successfully
            inserted into the database, or skips the Item if the property 
            information is missing.
        """
        name: str = item.get("name")[0]
        image_url: str = item.get("image_url")[0]

        if not name or not image_url:
            raise DropItem("Missing property information")

        DatabaseConnector().create_property(name=name, image_url=image_url)
        return item
    
from connector import connect_to_database
from scrapy import Item

from psycopg2.extensions import connection, cursor



class SrealityPropertyPipeline:
    def __init__(self) -> None:
        """Constructor for the class.
        """
        self._connection: connection = None
        self._cursor: cursor = None

    def _create_property_command(self, name: str, image_url: str) -> None:
        self._cursor.execute(f"INSERT INTO results (name, image_url) VALUES ('{name}', '{image_url}');")
        self._connection.commit()

    def process_item(self, item, _) -> Item:
        """Function that is triggered for every yielded object§
        from the Spider object.

        Args:
            item (scrapy.Item): A dictionary-like object holding the scraped data.
            _ (scrapy.Spider): A reference to the Spider object.

        Returns:
            scrapy.Item: A dictionary-like object holding the scraped data.
        """
        name: str = item.get("name")[0]
        image_url: str = item.get("image_url")[0]
        self._create_property_command(name=name, image_url=image_url)
        return item

    def open_spider(self, _) -> None:
        """Function triggered before spider is opened.
        Opens up connection to PostgreSQL database and 
        creates a cursor.

        Args:
            _ (scrapy.Spider): A reference to the Spider object.
        """
        self._connection = connect_to_database()
        self._cursor = self._connection.cursor()

    def close_spider(self, _) -> None:
        """A function that is triggered once the spider is closed.
        Closes the database connection and the cursor. 

        Args:
            _ (scrapy.Spider): A reference to the Spider object.
        """
        self._cursor.close()
        self._connection.close()

import os
import psycopg2

from typing import List
from psycopg2.extensions import connection, cursor
from scrapy.exceptions import DropItem


class DatabaseConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def __init__(self):
        try:
            self._connection: connection = psycopg2.connect(
                host=os.environ.get("POSTGRES_HOST"),
                port=os.environ.get("POSTGRES_PORT"),
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASS"),
            )
            self._cursor: cursor = self._connection.cursor()

        except psycopg2.OperationalError as e:
            print(f"Failed to connect to database: {e}")

    def retrieve_all_properties(self) -> List[List[str]]:
        with self._connection.cursor() as cursor:
            try:
                cursor.execute("SELECT * FROM results;")
                return cursor.fetchall()
            
            except Exception as e:
                print("Error fetiching database: ", e)
                return []

    def create_property(self, name: str, image_url: str) -> None:
        """Inserts a property record into the database.

        Args:
            name (str): Name of the property
            image_url (str): URL of the property image
        """
        with self._connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"INSERT INTO results (name, image_url) VALUES (\"{name}\", \"{image_url}\");"
                )
                self._connection.commit()
            
            except Exception as e:
                raise DropItem(f"Error inserting property: {e}")

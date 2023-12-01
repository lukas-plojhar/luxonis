"""Database connector for PostgreSQL."""
import os

from typing import List
from typing_extensions import Self

import psycopg2

from psycopg2.extensions import connection, cursor


class DatabaseConnector:
    """Singleton for accessing the PostgreSQL dataase."""

    _instance: Self = None

    def __new__(cls) -> None:
        """Singleton constructor method."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the database connection and cursor."""
        try:
            self._connection: connection = psycopg2.connect(
                host=os.environ.get("POSTGRES_HOST"),
                port=os.environ.get("POSTGRES_PORT"),
                database=os.environ.get("POSTGRES_DATABASE"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
            )
            self._cursor: cursor = self._connection.cursor()

        except psycopg2.Error as e:
            print(f"Failed to connect to database: {e}")

    def __del__(self) -> None:
        """Close the database connection when the object is deleted."""
        self._cursor.close()
        self._connection.close()

    def retrieve_all_properties(self) -> List[List[str]]:
        """Fetch all property records from the database.

        Returns:
            List[List[str]]: A list of property records, where each record
            is a list of values.
        """
        try:
            self._cursor.execute("SELECT * FROM results;")
            return self._cursor.fetchall()

        except psycopg2.Error as e:
            print("Error fetching database: ", e)
            return []

    def create_property(self, name: str, image_url: str) -> None:
        """Insert a property record into the database.

        Args:
            name (str): The name of the property.
            image_url (str): The URL of the property image.
        """
        try:
            self._cursor.execute(
                f"INSERT INTO results (name, image_url) VALUES('{name}', '{image_url}');"
            )
            self._connection.commit()

        except psycopg2.Error as e:
            print(f"Error inserting property to the database: {e}")

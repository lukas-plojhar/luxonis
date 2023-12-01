"""Defines Scrapy models for spiders."""
from scrapy import Field, Item


class SrealityPropertyItem(Item):
    """A class to represent the scraped object from Sreality.cz."""

    name = Field()
    image_url = Field()

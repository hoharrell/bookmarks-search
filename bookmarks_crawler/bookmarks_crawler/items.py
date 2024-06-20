# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Book(scrapy.Item):
    # define the fields for your item here like:
    # title = scrapy.Field()
    # url = scrapy.Field()
    # lastUpdated = scrapy.Field()
    title = scrapy.Field()
    publisher = scrapy.Field()
    pub_date = scrapy.Field()
    aggregate_rating = scrapy.Field()
    total_scores = scrapy.Field()
    cover = scrapy.Field()
    f_nf = scrapy.Field()
    authors = scrapy.Field()
    genres = scrapy.Field()

from scrapy.item import Item, Field


class Data(Item):
    artist = Field()
    album = Field()
    picture_url = Field()
    review_url = Field()
    tags = Field()
    genres = Field()
    year = Field()
    custom = Field()

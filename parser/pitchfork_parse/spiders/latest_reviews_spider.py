import scrapy
from pitchfork_parse.db_connector import DBconnector
from pitchfork_parse.items import Data


class LatestReviewsSpider(scrapy.Spider):
    name = 'latest'
    allowed_domains = ['pitchfork.com']
    start_urls = ['https://pitchfork.com/reviews/albums/?page=1']
    base_url = "https://pitchfork.com/reviews/albums/?page="
    page_number = 1

    def parse(self, response):
        db = DBconnector(config=self.settings.get("DB_CONFIG"))
        reviews: list = response.xpath('//div[@class="review"]')
        found_records = False

        for part in reviews:
            image_link = part.xpath('.//div[@class="review__artwork artwork"]/div/img/@src').get()
            if self.page_number == 1:
                if db.select_record_by_picture(image_link):
                    found_records = True
                    continue

            artist = part.xpath('.//ul[@class="artist-list review__title-artist"]/li/text()').get()
            album = part.xpath('.//h2[@class="review__title-album"]/text()').get()
            review_link = "https://" + self.allowed_domains[0] + part.xpath('.//a[@class="review__link"]/@href').get()
            date = part.xpath('.//time/@datetime').get()
            genres = part.xpath('.//a[@class="genre-list__link"]/text()').get()

            yield Data(artist=artist, album=album, review_url=review_link, picture_url=image_link,
                       tags=["latest"], custom={
                    "date": date,
                    "genres": genres
                })
        else:
            if found_records:
                raise scrapy.exceptions.CloseSpider(reason="All scraped")

        self.page_number += 1

        if self.page_number < 5:
            yield scrapy.Request(self.base_url + str(self.page_number), callback=self.parse)

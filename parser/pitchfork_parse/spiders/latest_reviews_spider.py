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
        reviews = response.xpath('//div[@class="review"]')
        if_reviews_modified = False

        if self.page_number == 1:
            found_record_id = len(reviews)
            records_pictures = response.xpath('//div[@class="review__artwork artwork"]/div/img/@src').getall()
            db = DBconnector(config=self.settings.get("DB_CONFIG"))
            for i, pic in enumerate(records_pictures, 1):
                if db.select_record_by_picture(pic):
                    found_record_id = -i
                    if_reviews_modified = True
            reviews = reviews[:found_record_id]

        for part in reviews:
            image_link = part.xpath('.//div[@class="review__artwork artwork"]/div/img/@src').get()
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
            if if_reviews_modified:
                raise scrapy.exceptions.CloseSpider(reason="No new records")

        self.page_number += 1
        # if response.status != 404:
        if self.page_number < 100:
            yield scrapy.Request(self.base_url + str(self.page_number), callback=self.parse)

import scrapy

from pitchfork_parse.items import Data


class BestAlbums2018(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://pitchfork.com/features/lists-and-guides/the-50-best-albums-of-2018',
    ]

    def parse(self, response):
        for part in response.xpath('//div[@class="list-blurb blurb-container container-fluid"]'):
            image_link = part.xpath('.//img/@src').get()
            artist = part.xpath('.//ul[@class="artist-links artist-list list-blurb__artists"]/*/*/text()').get()
            album = part.xpath('.//h2[@class="list-blurb__work-title"]/text()').get()
            review_link = response.request.url

            if not artist:
                artist = part.xpath('.//ul[@class="artist-list list-blurb__artists"]/*/text()').get()

            yield Data(artist=artist, album=album, review_url=review_link, picture_url=image_link,
                       custom={
                           "date": "2018-02-09T06:00:00"}, tags=["50_2018"])

        links = response.xpath('//a[@class="fts-pagination__list-item__link"]/@href').getall()[1:]

        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse)

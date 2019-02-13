from datetime import datetime

from scrapy import log
from twisted.enterprise import adbapi


class ItemProcessPipeline:

    def process_item(self, item, spider):
        # parse year
        item["year"] = datetime.strptime(item["custom"]["date"], "%Y-%m-%dT%H:%M:%S").year

        # parse genres
        if item.get("custom").get("genres"):
            genres = [a.lower() for a in item["custom"]["genres"].split('/')]
            item["genres"] = self._prepare_list_to_string(genres)
        else:
            item["genres"] = '[]'

        item["tags"] = self._prepare_list_to_string(item["tags"])
        return item

    def _prepare_list_to_string(self, arr):
        return str(arr).replace("'", '"')


class MySQLStorePipeline:

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            dbpool=adbapi.ConnectionPool('MySQLdb', **crawler.settings.get("DB_CONFIG"))
        )

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item):
        conn.execute(
            "insert into data (artist, album, picture_url, review_url, genres, year, tags) values (%s, %s, %s, %s, %s, %s, %s)",
            (item["artist"], item["album"], item["picture_url"], item["review_url"], item["genres"], item["year"],
             item["tags"]))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

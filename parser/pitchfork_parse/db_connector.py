from collections import namedtuple
from contextlib import contextmanager

import MySQLdb


class DBconnector:

    def __init__(self, config):
        self.model = namedtuple("AlbumItem", "artist, album, picture_url, review_url, genres, year")
        self.db_config = config

    @contextmanager
    def _open_close_connection(self):
        connection = MySQLdb.connect(**self.db_config)  # name of the data base
        cursor = connection.cursor()
        try:
            yield cursor
        finally:
            connection.close()

    def get_random_album(self, chosen_tag):
        return self._select_and_return_model(
            f"select * from (select * from `data` order by id desc limit 50) as lim where JSON_CONTAINS(lim.tags, '[\"{chosen_tag}\"]') = 1 order by rand() limit 1;")

    def select_record_by_picture(self, picture_url):
        return self._select_and_return_model("select * from data where picture_url=%s", picture_url)

    def select_pure_random(self):
        return self._select_and_return_model("select * from data order by rand() limit 1;")

    def _select_and_return_model(self, query, *params):
        with self._open_close_connection() as cursor:
            cursor.execute(query) if not params else cursor.execute(query, params)
            resulset = cursor.fetchone()
        return self.model(*resulset[1:7]) if resulset else resulset

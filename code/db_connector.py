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
        with self._open_close_connection() as cursor:
            cursor.execute(
                f" select * from data where JSON_CONTAINS(tags, '[\"{chosen_tag}\"]') = 1 order by rand() limit 1;")
            resulset = cursor.fetchone()
            return self.model(resulset[1], resulset[2], resulset[3], resulset[4], resulset[5], resulset[6])

    def select_record_by_picture(self, picture_url):
        with self._open_close_connection() as cursor:
            cursor.execute("select * from data where picture_url = %s", (picture_url,))
            if cursor.fetchone():
                return True

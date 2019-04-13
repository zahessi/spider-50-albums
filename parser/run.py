from pitchfork_parse.db_connector import DBconnector as connector
from pitchfork_parse.settings import DB_CONFIG as conf
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def crawl(runner, spider):
    return runner.crawl(spider)


configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerProcess(get_project_settings())

if not connector(conf).get_random_album(chosen_tag="50_2018"):
    crawl(runner, "50albums")
crawl(runner, "latest")
runner.start()


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
import datetime
import os


def _get_file_path(query_type, suffix="csv"):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = f"{query_type}_{datetime.date.today()}.{suffix}"

    data_path = os.path.join(dir_path, "..", "DATA", query_type)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return os.path.join(data_path, filename)

def main(*, query_type, url):
    
    file_path = _get_file_path(query_type)
    process = CrawlerProcess({**get_project_settings(), "FEED_URI" : file_path, "FEED_FORMAT": "csv"})
    process.crawl('immoscout', url=url)
    process.start()
    process.join()

if __name__ == "__main__":
    main(query_type="apartment_buy", url='https://www.immobilienscout24.de/Suche/de/bayern/muenchen-kreis/wohnung-kaufen?numberofrooms=2.0-&price=-1000000.0&livingspace=60.0-')



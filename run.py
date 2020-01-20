
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
import datetime
import os
import pandas as pd
import glob


def _get_data_path(query_type, create=True):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(dir_path, "DATA", query_type)
    if create and not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path

def _get_file_path(query_type, suffix="csv"):    
    data_path = _get_data_path(query_type)
    filename = f"{query_type}_{datetime.date.today()}.{suffix}"
    return os.path.join(data_path, filename)

def _post_process(query_type, suffix="csv"):
    files = glob.glob(f"*.{suffix}")
    data_path = _get_data_path(query_type)
    files = glob.glob(os.path.join(data_path, f"*.{suffix}"))    
    df_files = [pd.read_csv(f) for f in files if "dataset.csv" not in f]
    final_df = pd.concat(df_files, axis=0)
    final_df = final_df.drop_duplicates(subset=['immo_id'])
    final_df.to_csv(os.path.join(_get_data_path(query_type), "dataset.csv"))


def main(*, query_type, url):
    
    file_path = _get_file_path(query_type)
    process = CrawlerProcess({**get_project_settings(), "FEED_URI" : file_path, "FEED_FORMAT": "csv"})
    process.crawl('immoscout', url=url)
    process.start()
    process.join()
    _post_process(query_type, suffix="csv")

if __name__ == "__main__":
    main(query_type="apartment_buy", url='https://www.immobilienscout24.de/Suche/radius/wohnung-kaufen?centerofsearchaddress=M%C3%BCnchen;;;;;&numberofrooms=2.0-&price=-1000000.0&livingspace=60.0-&geocoordinates=48.15437;11.54199;20.0')



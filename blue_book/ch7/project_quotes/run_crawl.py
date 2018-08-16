from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_crawl():
    process = CrawlerProcess(get_project_settings())
    process.crawl('quotes')
    process.start()


if __name__ == "__main__":
    run_crawl()


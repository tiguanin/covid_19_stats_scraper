from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from crawler.spiders.scrap_statistic_table import CovidGeoInfoSpider


def main():
    configure_logging()
    runner = CrawlerRunner()
    task = LoopingCall(lambda: runner.crawl(CovidGeoInfoSpider))
    task.start(60 * 15, now=True)
    reactor.run()


if __name__ == "__main__":
    main()

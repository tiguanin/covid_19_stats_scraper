import scrapy

from crawler import parse_helper
from crawler.country_dao import parse_scrapped_countries_data
from dto.countryDTO import CountryDTO


class CovidGeoInfoSpider(scrapy.Spider):
    name = 'crawler'
    start_urls = ['https://www.worldometers.info/coronavirus/']

    def parse(self, response):
        stats_table = response.css('#main_table_countries_today tbody tr')
        stats_by_countries = []
        for row in stats_table:
            country_dto = CountryDTO(None, None, None, None, None, None, None, None, None)
            index = 0
            for td in row.css('td::text, a::text'):
                parse_helper.get_data_from_cells(index=index, text=td.get(), country=country_dto)
                index = index + 1
            stats_by_countries.append(country_dto)
        parse_scrapped_countries_data(stats_by_countries)

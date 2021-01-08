import scrapy
from scrapy.http import HtmlResponse
from jobparser7.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//a[contains(@class,'icMQ_ _6AfZ9')]/@href").extract()

        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

        next_page = response.xpath("//a[contains(@data-qa,'pager-next')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//span[@class='_1OuF_ ZON4b']//span[contains(@class,'_2Wp8I')]/text()").extract()
        link = response.url
        yield JobparserItem(name=name, salary=salary, link=link)
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from isbullshit.items import IsBullshitItem

class IsBullshitSpider(CrawlSpider):
    name = 'isbullshit'
    start_urls = ['http://isbullsh.it']
    rules = (
            Rule(LinkExtractor(allow=(r'page/\d+')), follow=True),
            Rule(LinkExtractor(allow=(r'\d{4}/\d{2}/\w+')), callback='parse_blogpost'),
            )
    def parse_blogpost(self, response):
        item = IsBullshitItem()
        item['title'] = response.xpath('//header/h1/text()').extract() 
        item['tag'] = response.xpath(
                "//header/div[@class='post-data']/p/a/text()").extract()
        return item


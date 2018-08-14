# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider

from project_quotes.items import Quote


class QuotesSpider(CrawlSpider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        items = []
        for quote_html in response.css('div.quote'):
            item = Quote()
            item['author'] = quote_html.css('small.author::text').extract_first()
            item['text'] = quote_html.css('span.text::text').extract_first()
            item['tags'] = quote_html.css('div.tags a.tag::text').extract()
            items.append(item)
            yield item

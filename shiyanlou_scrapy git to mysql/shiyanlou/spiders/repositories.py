# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import ShiyanlougithubItem

class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,5))
    
    def parse(self, response):
        for repository in response.css('li.public'):
            item = ShiyanlougithubItem({
                'name': repository.css('div.mb-1 a::text').extract_first().strip(),
                'update_time':repository.xpath('.//div[contains(@class, "mt-2")]/relative-time/@datetime').extract_first()
                })
            yield item

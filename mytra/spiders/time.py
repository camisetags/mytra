# -*- coding: utf-8 -*-
import scrapy


class TimeSpider(scrapy.Spider):
    name = 'time'
    allowed_domains = ['climatempo.com.br']
    start_urls = ['http://climatempo.com.br/']

    def parse(self, response):
        pass

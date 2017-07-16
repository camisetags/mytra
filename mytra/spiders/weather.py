# -*- coding: utf-8 -*-
import scrapy
import json
import os
import re

class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['climatempo.com.br']
    start_urls = [
        'https://www.climatempo.com.br/previsao-do-tempo/15-dias/cidade/321/riodejaneiro-rj'
    ]

    def parse(self, response):
        max_temps = response.css('p[arial-label="temperatura máxima"]::text').extract()
        min_temps = response.css('p[arial-label="temperatura mínima"]::text').extract()
        days = response \
            .css('h1.left.top10.bold.font12.txt-darkgray.medium-8.show-for-medium-up::text') \
            .extract()

        obj = self.build_temps_obj(
            max_temps=max_temps,
            min_temps=min_temps,
            days=days
        )

        is_saved = self.create_file(obj)

        print(obj)

    def build_temps_obj(self, min_temps, max_temps, days):
        obj = { 'temperatures': [] }
        for i in range(len(days)):
            day_split_pattern = 'RIO DE JANEIRO - '
            obj['temperatures'].append({
                'day': days[i].split(day_split_pattern)[-1],
                'min_temp': min_temps[i].replace('\u00b0', ''),
                'max_temp': max_temps[i].replace('\u00b0', '')
            })
        obj['temperatures'] = self.extract_repeated_days(obj['temperatures'])

        return obj

    def extract_repeated_days(self, temps):
        clean_temps = [dict(t) for t in set([tuple(d.items()) for d in temps])]
        return sorted(clean_temps, key=lambda k: k['day'])

    def create_file(self, obj):
        try:
            with open('temperatures.json', 'w') as json_file:
                print('================ SALVANDO ARQUIVO ================')
                json.dump(obj, json_file)
            return True
        except Exception as e:
            return False
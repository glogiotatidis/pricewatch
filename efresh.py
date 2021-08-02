#!/usr/bin/env python3

import scrapy
ROOT_URL = 'https://www.e-fresh.gr'
START_URL = ROOT_URL + '/api/list?page={page}'


class Efresh(scrapy.Spider):
    name = 'efresh'
    page = 1
    start_urls = [START_URL.format(page=1)]

    def parse(self, response):
        for product in response.json()['data']['products']['data']:
            data = {
                'url': product['links']['app_web'],
                'name': product['title'],
                'id': product['kodikos'],
                # Looks like some products feature the barcode at the end of the
                # image URL.
                'barcode': None,
                'image_url': product['image']['url'],
                'price': product['price'] ,
                'original_price': product['price_old'],
                'tax_rate': product['tax_rate'],
            }
            yield data

        if response.json()['data']['products']['next_page_url']:
            self.page += 1
            yield response.follow(START_URL.format(page=self.page), callback=self.parse)

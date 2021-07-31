#!/usr/bin/env python3

import scrapy
ROOT_URL = 'https://pitsias.gr'
START_URL = ROOT_URL + '/search?p={page}&q='

class Pitsias(scrapy.Spider):
    name = 'pitsias'
    page = 1
    products = 1
    start_urls = [START_URL.format(page=1)]

    def parse_product(self, response):
        data = {
            'url': response.url,
            'name': response.css('#prdinfo h1')[0].root.text,
            'id': response.css('#prdinfo .skman label')[0].root.text,
            'barcode': response.css('#prdinfo .skman label')[1].root.text,
            'image_url': ROOT_URL + response.css('#prdimgs img')[0].attrib['src'],
            'price': response.css('#prdinfo .prices strong')[0].root.text[:-1].replace(',', '.'),

        }
        yield data

    def parse(self, response):
        products = response.css('.prdgrd .image a')
        for product in products:
            product_url = ROOT_URL + product.attrib['href']
            yield response.follow(product_url, callback=self.parse_product)

        if response.css('#pagination .pagination a')[-1].root.text.strip() == '»':
            self.page += 1
            yield response.follow(START_URL.format(page=self.page), callback=self.parse)

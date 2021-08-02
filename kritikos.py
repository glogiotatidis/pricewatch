#!/usr/bin/env python3

import scrapy
START_URL = 'https://kritikos-cxm-production.herokuapp.com/api/v2/products?collection_eq=900&eligible=true'

class Kritikos(scrapy.Spider):
    name = 'kritikos'
    page = 1
    start_urls = [START_URL]

    def parse(self, response):
        for product in response.json()['payload']['products']:
            data = {
                'url': 'https://www.kritikos-sm.gr/products/x/x/' + product['sku'],
                'name': product['name'],
                'id': product['sku'],
                # Looks like some products feature the barcode at the end of the
                # image URL.
                'barcode': None,
                'image_url': 'https://s3.eu-central-1.amazonaws.com/w4ve/kritikos/products/' + product['images']['primary'],
                'price': (1.0 * product['finalPrice']) / 100,
                'original_price': (1.0 * product['beginPrice']) / 100,
                'tax_rate': product['vat'],
            }
            yield data


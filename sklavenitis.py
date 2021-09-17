#!/usr/bin/env python3

import scrapy
ROOT_URL = 'https://sklavenitis.gr'


class Sklavenitis(scrapy.Spider):
    name = 'sklavenitis'
    page = 1
    start_urls = [
        'https://www.sklavenitis.gr/katigories/'
    ]

    def parse(self, response):
        # Fetch categories
        if response.url.endswith('/katigories/'):
            for cat in response.css('.categories_item .categories_subs a'):
                yield response.follow(ROOT_URL + cat.root.attrib['href'])


        else:

            for product in response.css('#productList .product'):
                data = {
                    'url': ROOT_URL + product.css('.absLink')[0].attrib['href'],
                    'name': product.css('.product__title a')[0].root.text,
                    'price': float(product.css('.main-price .price')[0].root.text.strip().split(' ')[0].replace(',', '.')),
                    'image_url': product.css('img')[0].root.attrib['src'],
                    'id': product.css('img')[0].root.attrib['src'].rsplit('/', 2)[1],
                }
                try:
                    data['original_price'] = float(product.css('.main-price .deleted__price')[0].root.text.strip().split(' ')[0].replace(',', '.'))
                except IndexError:
                    data['original_price'] = data['price']

                yield data

            try:
                next_page_id = int(response.css('.pagination')[0].root.attrib['data-pg'])
            except (IndexError, ValueError):
                pass
            else:
                yield response.follow(response.url.rsplit('/',1 )[0] + f"/?$component=Atcom.Sites.Yoda.Components.ProductList.Index&sortby=ByPopularity&pg={next_page_id}")

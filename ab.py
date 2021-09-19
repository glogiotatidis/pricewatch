#!/usr/bin/env python3

import scrapy
ROOT_URL = 'https://www.AB.gr'
START_URL = ROOT_URL + '/api/list?page={page}'


class AB(scrapy.Spider):
    name = 'ab'
    page = 1
    url = "https://api.ab.gr"
    start_urls = [START_URL.format(page=1)]


    def _data(self):
        data ='{"operationName":"GetProductSearch","variables":{"lang":"gr","searchQuery":"","pageNumber":PAGENUMBER,"pageSize":500,"filterFlag":true,"useSpellingSuggestion":true},"query":"query GetProductSearch($lang: String, $searchQuery: String, $pageSize: Int, $pageNumber: Int, $category: String, $sort: String, $filterFlag: Boolean, $useSpellingSuggestion: Boolean) {\\n  productSearch: productSearchV2(lang: $lang, searchQuery: $searchQuery, pageSize: $pageSize, pageNumber: $pageNumber, category: $category, sort: $sort, filterFlag: $filterFlag, useSpellingSuggestion: $useSpellingSuggestion) {\\n    products {\\n      ...ProductBlockDetails\\n      __typename\\n    }\\n    breadcrumbs {\\n      ...Breadcrumbs\\n      __typename\\n    }\\n    facets {\\n      ...Facets\\n      __typename\\n    }\\n    sorts {\\n      name\\n      selected\\n      code\\n      __typename\\n    }\\n    pagination {\\n      ...Pagination\\n      __typename\\n    }\\n    freeTextSearch\\n    spellingSuggestionUsed\\n    currentQuery {\\n      query {\\n        value\\n        __typename\\n      }\\n      __typename\\n    }\\n    productsCountByCategory {\\n      categoryCode\\n      count\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment ProductBlockDetails on Product {\\n  available\\n  averageRating\\n  numberOfReviews\\n  manufacturerName\\n  manufacturerSubBrandName\\n  code\\n  eanCodes\\n freshnessDuration\\n  freshnessDurationTipFormatted\\n  frozen\\n  recyclable\\n  images {\\n    format\\n    imageType\\n    url\\n    __typename\\n  }\\n  maxOrderQuantity\\n  limitedAssortment\\n  name\\n  onlineExclusive\\n  potentialPromotions {\\n    alternativePromotionMessage\\n    code\\n    priceToBurn\\n    promotionType\\n    range\\n    redemptionLevel\\n    toDisplay\\n    description\\n    title\\n    promoBooster\\n    simplePromotionMessage\\n    __typename\\n  }\\n  price {\\n    approximatePriceSymbol\\n    currencySymbol\\n    formattedValue\\n    priceType\\n    supplementaryPriceLabel1\\n    supplementaryPriceLabel2\\n    showStrikethroughPrice\\n    discountedPriceFormatted\\n    discountedUnitPriceFormatted\\n    unit\\n    unitPriceFormatted\\n    unitCode\\n    unitPrice\\n    value\\n    __typename\\n  }\\n  purchasable\\n  productProposedPackaging\\n  productProposedPackaging2\\n  stock {\\n    inStock\\n    inStockBeforeMaxAdvanceOrderingDate\\n    partiallyInStock\\n    availableFromDate\\n    __typename\\n  }\\n  url\\n  previouslyBought\\n  nutriScoreLetter\\n  isLowPriceGuarantee\\n  __typename\\n}\\n\\nfragment Breadcrumbs on SearchBreadcrumb {\\n  facetCode\\n  facetName\\n  facetValueName\\n  facetValueCode\\n  removeQuery {\\n    query {\\n      value\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment Facets on Facet {\\n  code\\n  name\\n  category\\n  facetUiType\\n  values {\\n    code\\n    count\\n    name\\n    query {\\n      query {\\n        value\\n        __typename\\n      }\\n      __typename\\n    }\\n    selected\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment Pagination on Pagination {\\n  currentPage\\n  totalResults\\n  totalPages\\n  sort\\n  __typename\\n}\\n"}'
        data = data.replace('PAGENUMBER', str(self.page))

        return data


    def start_requests(self):
        data = self._data()
        yield scrapy.http.Request(self.url, method='POST', body=data, headers={'Content-Type': 'application/json'})

    def parse(self, response):
        for product in response.json()['data']['productSearch']['products']:
            data = {
                'url': f"https://www.ab.gr/{product['url']}",
                'name': f"{product['manufacturerName']} {product['name']}",
                'id': product['code'],
                'barcode': product['eanCodes'],
                'image_url': f"https://www.ab.gr/{product['images'][0]['url']}" if product['images'] else None,
                'price': float(product['price']['discountedPriceFormatted'][1:].replace(',', '.')),
                'original_price': float(product['price']['formattedValue'][1:].replace(',', '.')),
            }
            yield data

        if self.page < response.json()['data']['productSearch']['pagination']['totalPages']:
            self.page += 1
            data = self._data()
            yield scrapy.http.Request(self.url, method='POST', body=data, headers={'Content-Type': 'application/json'})

# -*- coding: utf-8 -*-
import scrapy


class FlipkartMobileSpider(scrapy.Spider):
    name = 'flipkart_mobile'
    allowed_domains = ['https://www.flipkart.com']
    start_urls = ['https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.serviceability%5B%5D%3Dfalse']

    def parse(self, response):
        name = response.xpath('//div[@class = "_3wU53n"]/text()').extract()
        rating = response.xpath('//div[@class = "hGSR34"]/text()').extract()
        price = response.xpath('//div[@class = "_1vC4OE _2rQ-NK"]/text()').extract()
        x = response.xpath('//ul[@class = "vFw0gD"]')
        mobile_info = zip(name, rating, price, x)
        for mobile in mobile_info:
            g = []
            for s in mobile[3].css('li'):
                g.append(s.css('li ::text').extract())
            scraped_info = {
                'name' : mobile[0],
                'rating' : mobile[1],
                'price' : mobile[2],
                'spec' : g
            }

            yield scraped_info

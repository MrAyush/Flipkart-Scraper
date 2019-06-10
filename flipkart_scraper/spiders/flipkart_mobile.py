# -*- coding: utf-8 -*-
import scrapy


class FlipkartMobileSpider(scrapy.Spider):
    name = 'flipkart_mobile'
    start_urls = ['https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.serviceability%5B%5D%3Dfalse']

    custom_settings = {
        'FEED_URI' : "flipkart-mobile_%(time)s.json",
        'FEED_FORMATE' : 'json'
    }

    def parse(self, response):
        name = response.xpath('//div[@class = "_3wU53n"]/text()').extract()
        rating = response.xpath('//div[@class = "hGSR34"]/text()').extract()
        price = response.xpath('//div[@class = "_1vC4OE _2rQ-NK"]/text()').extract()
        spec = response.xpath('//ul[@class = "vFw0gD"]')
        price = response.xpath('//div[@class = "VGWI6T"]/span/text()').extract()

        mobile_info = zip(name, rating, price, spec, price)
        for mobile in mobile_info:
            spec_list = []
            for s in mobile[3].css('li'):
                spec_list.append(s.css('li ::text').extract())
            scraped_info = {
                'name' : mobile[0],
                'rating' : mobile[1],
                'price' : mobile[2],
                'spec' : spec_list,
                'off' : mobile[4]
            }

            yield scraped_info

            NEXT_PAGE_SELECTOR = '//a[@class = "_3fVaIS"][span/text() = "Next"]'
            next_page = response.xpath(NEXT_PAGE_SELECTOR)
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page.css('._3fVaIS ::attr(href)').extract_first()),
                    callback=self.parse
                )

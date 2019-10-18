# -*- coding: utf-8 -*-
#import scrapy


#class PulsaPaketdataSpider(scrapy.Spider):
#    name = 'pulsa_paketdata'
#
#    def start_requests(self):
#        url = "https://portalpulsa.com/pulsa-reguler-murah/"
#        yield scrapy.Request(url=url, callback=self.parse)
#
#    def parse(self, response):
#        for row in response.css("tbody tr"):
#            yield {
#                "pulsa": row.css("td[0]::text").get(),
#                "kode": row.css("td[1]::text").get(),
#                "harga": row.css("td[2]::text").get(),
#                "status": row.css("td.text-center span::text").get()
#            }

import scrapy


class PulsaSpider(scrapy.Spider):
    name = 'pulsa'

    def start_requests(self):
        url = "https://portalpulsa.com/pulsa-reguler-murah/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.xpath("//table//tr")
        for row in data[1:]:
            yield {
                "produk": row.xpath("td[1]//text()").get(),
                "jenis": "pulsa",
                "kode": row.xpath("td[2]//text()").get(),
                "harga": row.xpath("td[3]//text()").get(),
                "status": row.xpath("td[4]//text()").get()
            }



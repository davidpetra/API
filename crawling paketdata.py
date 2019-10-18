import scrapy


class PaketDataSpider(scrapy.Spider):
    name = 'paketdata'

    def start_requests(self):
        url = "https://portalpulsa.com/paket-data-internet-murah/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.xpath("//table//tr")
        for row in data[1:]:
            yield {
                "produk": row.xpath("td[1]//text()").get(),
                "jenis": "paketdata",
                "kode": row.xpath("td[2]//text()").get(),
                "harga": row.xpath("td[3]//text()").get(),
                "status": row.xpath("td[4]//text()").get()
            }



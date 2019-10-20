import http.server
from http.server import HTTPServer, SimpleHTTPRequestHandler
import base64

import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher

import json
from urllib.parse import urlparse



class PulsaSpider(scrapy.Spider):
    name = "pulsa"

    def start_requests(self):
        url = "https://portalpulsa.com/pulsa-reguler-murah/"
        yield scrapy.Request(url=url, callback=self.parse)


    custom_settings = {
        "FEED_URI": "datapulsa.json",
        "FEED_FORMAT": "json"
    }

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


class PaketDataSpider(scrapy.Spider):
    name = "paketdata"

    def start_requests(self):
        url = "https://portalpulsa.com/paket-data-internet-murah/"
        yield scrapy.Request(url=url, callback=self.parse)

    custom_settings = {
        "FEED_URI": "datapaketdata.json",
        "FEED_FORMAT": "json"
    }

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


def hasilspider():
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)

    process = CrawlerProcess(get_project_settings())
    process.crawl(PulsaSpider)
    process.crawl(PaketDataSpider)
    process.start()
    return results


crawled_data = hasilspider()

with open("datapulsa.json","r") as a:
    crawled_pulsa = json.load(a)

with open("datapaketdata.json","r") as b:
    crawled_paket_data = json.load(b)


class Requests(http.server.SimpleHTTPRequestHandler):
    def _html(self, message):
        
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")
    
    def do_GET(self):
        parse = urlparse(self.path)
        path = parse.path
        query = parse.query

        if path == "/pulsa":
            if query == "":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(crawled_pulsa).encode())
            else:
                parameter = query.split("=")[0]
                if parameter == "kode":
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    kodepulsa = query.split("=")[1]
                    kodepulsa_parameter = next(item for item in crawled_pulsa if item["kode"] == kodepulsa)
                    self.wfile.write(json.dumps(kodepulsa_parameter).encode())
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(self._html("Error 404 Not Found"))
        elif path == "/paketdata":
            if query == "":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(crawled_paket_data).encode())
            else:
                parameter = query.split("=")[0]
                if parameter == "kode":
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    kodepaketdata = query.split("=")[1]
                    kodepaketdata_parameter = next(item for item in crawled_paket_data if item["kode"] == kodepaketdata)
                    self.wfile.write(json.dumps(kodepaketdata_parameter).encode())
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(self._html("Error 404 Not Found"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self._html("Error 404 Not Found"))

port = 8000
try:
    with HTTPServer(("",port), Requests) as httpd:
        print("Serving at port ", port, "...")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("tutup")
    httpd.socket.close()
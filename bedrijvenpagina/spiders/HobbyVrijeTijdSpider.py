# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import time, re, random, base64
from bedrijvenpagina.items import BedrijvenpaginaItem
# from fake_useragent import UserAgent


class HobbyvrijetijdspiderSpider(scrapy.Spider):
    name = "HobbyVrijeTijdSpider"
    allowed_domains = ["bedrijvenpagina.nl"]
    start_urls = (
        'https://www.bedrijvenpagina.nl/',
    )

    keywords = ['hobby-vrije-tijd']
    counts = [15030] #699659
    # counts = [3] #699659

    def set_proxies(self, url, callback):
        req = Request(url=url, callback=callback)
        # user_agent = self.ua.random
        # req.headers['User-Agent'] = user_agent
        return req

    def start_requests(self):
        # self.ua = UserAgent()

        for idx in range(0, len(self.keywords)):

            keyword = self.keywords[idx]
            count = self.counts[idx]

            for ind in range(1, count):
                pg_no = ""
                if ind > 1:
                    pg_no = "?p=" + str(ind)

                url = self.start_urls[0] + keyword + "/" + pg_no
                req = self.set_proxies(url , self.parse_item)
                yield req

    def parse_item(self, response):
        # print("_________________________________")
        # print response.url
        item = BedrijvenpaginaItem()
        card_div = response.xpath("//div[@class='card']")

        url = response.url

        for row in card_div:
            name = row.xpath("h3/a/span/text()").extract_first()
            address = row.xpath('span/span[@class="street-address"]/text()').extract_first()
            postal_code = row.xpath('span/span[@class="postal-code"]/text()').extract_first()
            city = row.xpath('span/span[@class="locality"]/text()').extract_first()

            item["name"] = name
            item["address"] = address
            item["postal_code"] = postal_code
            item["city"] = city
            item["url"] = url

            note_div = row.xpath(".//div[@class='note']/p/a/@href").extract()
            if len(note_div) > 0:
                req = self.set_proxies(response.urljoin(note_div[0]) , self.parse_item_detail)
                req.meta["item"] = item
                yield req
            else:
                print("_________________________________")
                print response.url
                if item["name"] != "":
                    yield item

    def parse_item_detail(self, response):

        item = response.meta["item"]

        item["phoneno"] = response.xpath("//div[@class='tel mobile']/a/span/text()").extract()
        item["email"] = response.xpath("//div[@class='mail']/a/text()").extract()
        item["website"] = response.xpath("//div[@class='url']/a/text()").extract()
        item["kvk"] = response.xpath("//div[@class='kvk']/a/text()").extract()
        item["sub_url"] = response.url

        if item["name"] != "":
            print("_________________________________")
            print response.url
            yield item

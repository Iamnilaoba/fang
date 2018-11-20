# -*- coding: utf-8 -*-
import scrapy
from fang.items import FangItem
from scrapy_redis import spiders
import re

class FfSpider(spiders.RedisSpider):
    name = 'ff'
    allowed_domains = ['fang.com']
    #start_urls = ['http://www.fang.com/SoufunFamily.htm']
    redis_key = "fang"

    def parse(self, response):
        # 先获取整个table和tr区域
        # 获取省，获取市，获取市url
        table = response.xpath("//div[@class='outCont']/table")
        trs = table.xpath(".//tr")
        province = None
        for tr in trs:
            first_td = tr.xpath(".//td[2]//text()").get().strip()
            if first_td:
                province = first_td
            td_city_herf = tr.xpath(".//td[3]/a/@href").getall()
            td_city = tr.xpath(".//td[3]/a/text()").getall()
            for index, city in enumerate(td_city):
                newUrl = None
                esUrl = None
                if city == "北京":
                    newUrl = 'http://newhouse.fang.com/house/s/'
                    esUrl = 'http://esf.fang.com/'
                else:
                    lst = td_city_herf[index].split('fang')
                    newUrl = 'newhouse.fang'.join(lst)
                    esUrl = 'esf.fang'.join(lst)
                yield scrapy.Request(newUrl, callback=self.newHome, meta={"province": province, "city": city})
                yield scrapy.Request(esUrl, callback=self.esHome, meta={"province": province, "city": city})

    def newHome(self, response):
        meta = dict(response.meta)
        lis = response.xpath("//div[@id='newhouse_loupai_list']/ul/li[not(@class)]")
        for li in lis:
            names = li.xpath(".//div[@class='nlcd_name']/a/text()").get()
            if not names:
                continue
            else:
                name = re.sub("\t", '', names, 0).strip()
            sizes = li.xpath(".//div[@class='house_type clearfix']/a/text()").getall()
            sizes = "/".join(sizes)
            size = re.sub("\s", '', sizes, 0).strip()
            address = li.xpath(".//div[@class='address']/a/@title").get()
            price = li.xpath(".//div[@class='nhouse_price']/span/text()").get()
            phone = li.xpath(".//div[@class='tel']/p/text()").get()
            yield FangItem(name=name, size=size, address=address, price=price,
                           phone=phone, province=meta['province'], city=meta['city'])
        nextUrl = response.xpath("//div[@class='page']/ul/li/a[@class='next']/@href").get()
        if nextUrl:
            nextUrl = response.url.join(nextUrl)
            scrapy.Request(nextUrl, callback=self.newHome, meta=meta)

    def esHome(self, response):
        meta=dict(response.meta)
        lis=response.xpath("//div[@class='shop_list shop_list_4']")
        for li in lis:
            name=li.xpath(".//dd[1]/h4/a/span/text()").get()
            size=li.xpath(".//dd[1]/p/text()").get().strip()
            address=li.xpath(".//dd[1]/p[2]/span/text()").get()
            price=li.xpath(".//dd[2]/span[2]/text()").get()
            yield FangItem(name=name,size=size,address=address,price=price,province=meta['province'],city=meta['city'])
        nextUrl=response.xpath("//div[@class='page_al']/p[1]/a/@href").get()
        if nextUrl:
            nextUrl=response.url.join(nextUrl)
            scrapy.Request(nextUrl,callback=self.esHome,meta=meta)

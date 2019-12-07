# -*- coding: utf-8 -*-
import scrapy
import time,random

from Meinv_img.items import MeinvImgItem
class ImgDownSpider(scrapy.Spider):
    name = 'img_down'
    allowed_domains = ['quantuwang.co']
    start_urls = ['http://www.quantuwang.co/meinv/']
    start_url='http://www.quantuwang.co'
    def parse(self, response):
        tag_href=response.xpath('//div[@class="index_top_tag"]/ul/li/a/@href').getall()
        for i in tag_href:
            tag_url=self.start_url+i
            yield scrapy.Request(tag_url,callback=self.index)
    def index(self,response):
        one_url=response.xpath('//div[@class="index_left"]/ul/li/a/@href').getall()
        for i in one_url:
            now_url=self.start_url+i
            yield scrapy.Request(now_url,callback=self.img_down)
        next_page=response.xpath('//div[@class="c_page"]/a/text()').getall()
        now_page=response.xpath('//div[@class="c_page"]/span/text()').get()
        list(next_page)
        if next_page==[]:
            pass
        elif next_page[-1]!=now_page:
            next_url=response.xpath('//div[@class="c_page"]/a[{}]/@href'.format(str(now_page))).get()
            urls=self.start_url+next_url
            yield scrapy.Request(urls,callback=self.index)
        else:
            pass
    def img_down(self,response):
        img_url=response.xpath('//div[@class="c_img"]/a/img/@src').get()
        img_title=response.xpath('//div[@class="c_title"]/h1/text()').get()
        item=MeinvImgItem()
        item['title']=img_title
        item['img_url']=img_url
        yield item
        time.sleep(random.randint(1,3))
        next_url=response.xpath('//div[@class="c_page"]/a/text()').getall()
        list(next_url)
        now_page=response.xpath('//div[@class="c_page"]/span/text()').get()
        if now_page!=next_url[-1]:
            nexts=response.xpath('//div[@class="c_page"]/a[{}]/@href'.format(now_page)).get()
            ne=self.start_url+nexts
            yield scrapy.Request(ne,callback=self.img_down)
# -*- coding: utf-8 -*-
import scrapy,time
from Meinvtu.items import MeinvtuItem
from lxml import etree
# from items import MeinvtuItem

class MeizituImgSpider(scrapy.Spider):
    name = 'Meizitu_img'
    allowed_domains = ['meitulu.com']
    start_urls = ['http://www.meitulu.com/']

    def parse(self, response):
        tag_url=response.xpath('//li[@id="tag"]/ul/li/a/@href').getall()
        tag_name=response.xpath('//li[@id="tag"]/ul/li/a/text()').getall()
        for i in zip(tag_url,tag_name):
            self.tag = i[1]
            yield scrapy.Request(i[0],callback=self.Get_ime_url)
            break

    def Get_ime_url(self,response):
        xml=etree.HTML(response.text)
        img=xml.xpath('//ul[@class="img"]/li')
        for i in img:
            img_href=i.xpath('.//a/@href')[0]
            yield scrapy.Request(img_href,callback=self.get_img_url)
        if_url=xml.apth('//center/div/a[@class="a1"][last()]/@href')[0]
        if if_url==response.url:
            print('>'*10,'本大类已经爬取完毕')
            pass
        else:
            print('>'*10,'正在爬取下一页面')
            yield scrapy.Request(if_url,callback=self.Get_ime_url)

    def get_img_url(self,response):
        xml=etree.HTML(response.text)
        data=xml.xpath('//center/img')
        file_title=xml.xpath('//h1/text()')[0]
        ifs=file_title[-5:-1]
        if '/' in ifs:
            file_title=file_title[0:-5]
        else:
            pass
        for i in data:
            img_url=i.xpath('.//@src')[0]
            img_title=i.xpath('.//@alt')[0]
            # print(img_url)
            item=MeinvtuItem()
            item['file_tag']=self.tag
            item['file_title']=file_title
            item['img_title']=img_title
            item['img_url']=img_url
            yield item
        if_url=xml.xpath('//div[@id="pages"]/a[last()]/@href')[0]
        next_url='https://www.meitulu.com/'+if_url
        if next_url==response.url:
            print('>'*10,'本url已经爬取完毕')
            pass
        else:
            print('>'*10,'正在爬取下一页面')
            yield scrapy.Request(next_url,callback=self.get_img_url)






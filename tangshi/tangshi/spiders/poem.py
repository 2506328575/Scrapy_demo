# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time
from lxml import etree
from tangshi.items import TangshiItem
class PoemSpider(CrawlSpider):
    name = 'poem'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['https://so.gushiwen.org/shiwen/']

    rules = (
        Rule(LinkExtractor(allow=r'/shiwen/default_.+.aspx')),
        Rule(LinkExtractor(allow=r'/shiwen/default_.+.aspx'),follow=True),
        Rule(LinkExtractor(allow=r'https://so.gushiwen.org/shiwenv_.+.aspx'),follow=False,callback='parse_item')
    )

    def parse_item(self, response):
        response_url=response.url
        html=response.text
        xml=etree.HTML(html)
        response=xml
        id=response_url.split('_')[-1].split('.')[0]
        title=response.xpath('//h1/text()')
        cont_list= response.xpath('//div[@id="contson{}"]/p/text()'.format(id))
        cont_list2= response.xpath('//div[@id="contson{}"]/text()'.format(id))
        cont=','.join(cont_list) if cont_list!=[] else ','.join(cont_list2)
        author=response.xpath('//div[@class="sons"][1]/div[@class="cont"]/p/a[2]/text()') # 作者
        dynasty=response.xpath('//div[@class="sons"][1]/div[@class="cont"]/p/a[1]/text()') # 朝代
        about_the_author=response.xpath('//div[@class="sonspic"]/div[@class="cont"]/p[2]/text()') # 作者简介
        annotation=response.xpath('//div[@class="sons"][2]/div[@class="contyishang"]/p[2]/text()') # 注释
        translation=response.xpath('//div[@class="sons"][2]/div[@class="contyishang"]/p[1]/text()')
        # backdrop=response.xpath('//div[@class="sons"][5]/div[@class="contyishang"]/p/a/text()')
        item = TangshiItem()
        item['title']=title[0].replace(u'\u3000',u'').replace(u'\n',u'')  if title!=[] else 'None'
        item['dynasty']=dynasty[0] .replace(u'\u3000',u'').replace(u'\n',u'') if dynasty!= [] else 'None'
        item['author']=author[0].replace(u'\u3000',u'').replace(u'\n',u'')  if author!=[] else 'None'
        item['cont']=cont.strip().replace(u'\u3000',u'').replace(u'\n',u'')
        item['id']=id
        item['about_the_author']=about_the_author[0].replace(u'\u3000',u'').replace(u'\n',u'') if about_the_author!=[] else 'None'
        item['annotation']=' '.join(annotation).replace(u'\u3000',u'').replace(u'\n',u'')  if annotation != [] else 'None'
        item['translation']=' '.join(translation).replace(u'\u3000',u'').replace(u'\n',u'')  if translation!=[] else 'None'
        print('*'*100000)
        return item

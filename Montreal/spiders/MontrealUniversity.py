import scrapy
import logging,re,traceback
# import requests
from lxml import html
from Montreal.items import MontrealItem
from googletrans import Translator


class MontrealSpider(scrapy.Spider):
    name = 'Montreal'
    # allowed_domains = ['www.admission.umontreal.ca']
    page_number=2
    # start_urls = ['https://admission.umontreal.ca/en/graduate-programs']
    start_urls=['https://admission.umontreal.ca/en/graduate-programs?type=888&tx_solr[page]=1&_=1600315011529']
    link=[]
    def parse(self, response):
        # program_link=response.xpath('//div[@class="programme"]/table[@class="listingTable programmesListing"]/tbody/tr/td/div[@class="programmeEtude"]/p/a/@href').extract()
        program_link=response.xpath('/html/body/tr/td/div[@class="programmeEtude"]/p/a/@href').extract()
        self.link.extend(program_link)
        # print(len(program_link))
        next_page='https://admission.umontreal.ca/en/graduate-programs?type=888&tx_solr[page]='+str(MontrealSpider.page_number)+'&_=1600315011529'
        if MontrealSpider.page_number <=8:
            MontrealSpider.page_number=MontrealSpider.page_number+1
            yield response.follow(next_page,callback=self.parse)
        else:
            course_url=[]
            for link in self.link:
                base='https://admission.umontreal.ca'+str(link)
                course_url.append(base)
            print(len(course_url))
            for url in course_url:
                yield scrapy.Request(url,callback=self.parse_course)

    def parse_course(self,response):
        item=MontrealItem()
        translator=Translator()
        logging.info('Montreal Unisversity:Scrapping course page started:url {}'.format(response.url))
        # 1 course name
        course_name=response.xpath('//*[@id="c9"]/div[1]/div[1]/div/div/h1/text()').extract()
        # print(len(course_name))
        s_course_name=" ".join([str(e) for e in course_name])
        t_course_name=translator.translate(s_course_name,des='en').text
        item["course_name"]=t_course_name
        # 2 Category
        category=response.xpath('//*[@id="c9"]/div[1]/div[1]/div/div/div/a[1]/text()').extract_first()
        t_category=translator.translate(category,des='en').text
        item["category"]=t_category
        # 3 Sub category
        # 4 Course website
      
        # result=translator.translate(program_link, src='fr', dest='en')
        # program_en=[]
        # for trans in result:
        #     tran=trans.text
        #     text=tran.strip()
        #     program_en.append(text)
        # print(program_en)

       
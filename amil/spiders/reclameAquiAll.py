# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

class ReclameAquiAllSpider(scrapy.Spider):
    name = 'reclameAquiAll'
    start_urls = ['https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id=14205&page=1&size=10&status=ALL']
    count = 2 #991

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1.0})

    def parse(self, response):
        links = response.xpath('/html/body/ui-view/div[2]/div[3]/div/div[2]/div/div/div/div/a/@href').extract()
        feelings = response.xpath('/html/body/ui-view/div[2]/div[3]/div/div[2]/div/div/div/div/span/img/@src').extract()
        #npag = response.xpath('/html/body/ui-view/div[2]/div[3]/div/div[2]/div/div/ul[2]/li[contains(@class, "pagination-next") and not(contains(@class, "disabled"))]/a').extract_first()

        for i in range(len(feelings)):
            feelings[i] = feelings[i].split('/')[-1].split('.')[0].replace('-', " ").replace('nao', 'não')
            feelings[i] = feelings[i][0].upper() + feelings[i][1:]
        for i  in range(len(links)):
            yield SplashRequest('https://www.reclameaqui.com.br%s?feeling=%s' %(links[i], feelings[i]), self.parse_detail, args={'wait': 1.0})

        yield SplashRequest('https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id=14205&page=%s&size=10&status=ALL' % self.count, self.parse, args={'wait': 1.0})
        self.count+=1
            
        
    
    def parse_detail(self, response):
        try:
            title = response.xpath('/html/body/ui-view/div[3]/div/div[1]/div[1]/div/div[1]/div[2]/div[1]/h1/text()').extract_first()
            desc = response.xpath('/html/body/ui-view/div[3]/div/div[1]/div[1]/div/div[2]/p/text()').extract_first()
            local = response.xpath('/html/body/ui-view/div[3]/div/div[1]/div[1]/div/div[1]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first()
            index = response.xpath('/html/body/ui-view/div[3]/div/div[1]/div[1]/div/div[1]/div[2]/div[1]/ul[1]/li[2]/b/text()').extract_first().split(': ')[-1]
            date = response.xpath('/html/body/ui-view/div[3]/div/div[1]/div[1]/div/div[1]/div[2]/div[1]/ul[1]/li[3]/text()').extract_first().replace(' às ', " ").replace('h', ":")
            status = response.xpath('/html/body/ui-view/div[3]/div/div[1]/div[1]/div/div[1]/div[2]/div[2]/div/span/img/@src').extract_first().split('/')[-1].split('.')[0].replace('-', " ").replace('nao', 'não')
            status = status[0].upper() + status[1:]
            feeling = response.url.split('=')[-1]
            
            yield{
                'titulo': title,
                'descricao': desc,
                'id_reclame_aqui': index,
                'local': local,
                'data': date,
                'status': status,
                'sentimento': feeling
            }
        except:
            print ("Exception")
            yield SplashRequest(response.url, self.parse_detail, args={'wait': 1.0})
        
        '''
    # SELENIUM
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.ndriver = webdriver.PhantomJS()
    
    def parse(self, response):
        recs = self.driver.find_elements_by_class_name('complaint-item')
        npag = self.driver.find_element_by_class_name('pagination-next')
        for rec in recs:
            self.links.append(rec.find_element_by_tag_name('a').get_attribute('href'))
            feeling = self.driver.find_element_by_class_name('complain-status-title').find_element_by_tag_name('img').get_attribute('src').split('/')[-1].split('.')[0].replace('-', " ").replace('nao', 'não')
            self.feelings.append(feeling[0].upper() + feeling[1:])
        #self.driver.close()
        #self.print_list(self.votes)

        for link in self.links:
            yield scrapy.Request(
                url = link,
                callback = self.parse_detail
            )
    
        if 'disabled' not in npag.get_attribute('class'): #and self.count < 1:
            #self.count += 1
            npag.find_element_by_tag_name('a').click()
            yield scrapy.Request(
                url = self.driver.current_url,
                callback = self.parse
            )

    def parse_detail(self, response):
        self.ndriver.get(response.url)

        WebDriverWait(self.ndriver, 50).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

        title = self.ndriver.find_element_by_tag_name('h1').get_attribute('innerHTML')
        desc = self.ndriver.find_element_by_class_name('complain-body').find_element_by_tag_name('p').get_attribute('innerHTML').replace('<br>', ' ')
        local_date = self.ndriver.find_element_by_class_name('local-date').find_elements_by_tag_name('li')
        local = local_date[0].text
        index = local_date[1].text.split(': ')[-1]
        date = local_date[2].text.replace(' às ', " ").replace('h', ":")
        status = self.ndriver.find_element_by_class_name('upshot-seal').find_element_by_tag_name('img').get_attribute('src').split('/')[-1].split('.')[0].replace('-', " ").replace('nao', 'não')
        status = status[0].upper() + status[1:]
        feelingIndex = self.links.index(response.url)

        #self.log('\n'+vote+'\n')
        yield{
            'titulo': title,
            'descricao': desc,
            'id_reclame_aqui': index,
            'local': local,
            'data': date,
            'status': status,
            'sentimento': self.feelings[feelingIndex]
        }
        '''
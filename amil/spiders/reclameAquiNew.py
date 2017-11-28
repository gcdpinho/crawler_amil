# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ReclameAquiNewSpider(scrapy.Spider):
    name = 'reclameAquiNew'
    start_urls = ['https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id=14205&page=1&size=10&status=ALL']
    feelings = []
    links = []
    flag = True

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.ndriver = webdriver.PhantomJS()

    def parse(self, response):
        self.driver.get(response.url)

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'pagination-next')))

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
    
        if 'disabled' not in npag.get_attribute('class') and self.flag:
            npag.find_element_by_tag_name('a').click()
            yield scrapy.Request(
                url = self.driver.current_url,
                callback = self.parse
            )

    def parse_detail(self, response):
        self.ndriver.get(response.url)

        WebDriverWait(self.ndriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

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
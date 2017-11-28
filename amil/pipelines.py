# -*- coding: utf-8 -*-
import cx_Oracle
from datetime import datetime


class AmilPipeline(object):
    lastDate = None

    def open_spider(self, spider):
        self.connection = cx_Oracle.connect('voiza_crawler', 'voiza_crawler', cx_Oracle.makedsn('192.168.0.4', '1521', service_name='oracle11g'), encoding = 'UTF-8', nencoding = 'UTF-8')
        self.db = self.connection.cursor()
        if "New" in spider.name:
            query = """SELECT TO_DATE(MAX(DATA)) FROM RECLAME_AQUI_TESTE"""
            self.db.execute(query)
            self.lastDate = self.db.fetchall()[0][0]
    
    def close_spider(self, spider):
        self.db.close()
        self.connection.commit()
        self.connection.close()
        spider.driver.close()
        spider.ndriver.close()
        #print(spider.count)

    def process_item(self, item, spider):
        if self.lastDate != None:
            if datetime.strptime(item['data'], "%d/%m/%y %H:%M").date() >= self.lastDate.date():
                query = """SELECT * FROM RECLAME_AQUI_TESTE WHERE ID_RECLAME_AQUI = :id_reclame_aqui"""
                self.db.execute(query, {
                    ':id_reclame_aqui': item['id_reclame_aqui']
                })
                if not self.db.fetchall():
                    query = """INSERT INTO reclame_aqui_teste (id, pesquisa, titulo, descricao, local, data, status, sentimento, id_reclame_aqui) VALUES (seq_reclame_aqui.NEXTVAL, 'Amil', :titulo, :descricao, :local, to_date(:data, 'dd/mm/yyyy hh24:mi'), :status, :sentimento, :id_reclame_aqui)"""
                    self.db.execute(query, {
                        ':titulo': item['titulo'],
                        ':descricao': item['descricao'],
                        ':local': item['local'],
                        ':data': item['data'],
                        ':status': item['status'],
                        ':sentimento': item['sentimento'],
                        ':id_reclame_aqui': item['id_reclame_aqui']
                    })
            else:
                spider.flag = False
        else:
            query = """INSERT INTO reclame_aqui_teste (id, pesquisa, titulo, descricao, local, data, status, sentimento, id_reclame_aqui) VALUES (seq_reclame_aqui.NEXTVAL, 'Amil', :titulo, :descricao, :local, to_date(:data, 'dd/mm/yyyy hh24:mi'), :status, :sentimento, :id_reclame_aqui)"""
            self.db.execute(query, {
                ':titulo': item['titulo'],
                ':descricao': item['descricao'],
                ':local': item['local'],
                ':data': item['data'],
                ':status': item['status'],
                ':sentimento': item['sentimento'],
                ':id_reclame_aqui': item['id_reclame_aqui']
            })

        return item
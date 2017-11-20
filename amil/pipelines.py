# -*- coding: utf-8 -*-
import cx_Oracle


class AmilPipeline(object):

    def open_spider(self, spider):
        self.connection = cx_Oracle.connect('voiza_crawler', 'voiza_crawler', cx_Oracle.makedsn('192.168.0.4', '1521', service_name='oracle11g'), encoding = 'UTF-8', nencoding = 'UTF-8')
        self.db = self.connection.cursor()
        
    def close_spider(self, spider):
        self.db.close()
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        
        self.db.execute('INSERT INTO reclame_aqui (id, pesquisa, titulo, descricao, local, data, status, sentimento, id_reclame_aqui) VALUES (seq_reclame_aqui.NEXTVAL, \'Amil\', \''+item['titulo']+'\', \''+item['descricao']+'\', \''+item['local']+'\', to_date(\''+item['data']+'\', \'dd-mm-yyyy hh24:mi\'), \''+item['status']+'\', \''+item['sentimento']+'\', \''+item['id']+'\')')

        return item

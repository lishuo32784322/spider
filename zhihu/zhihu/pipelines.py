# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class ZhihuPipeline(object):
    def process_item(self, item, spider):
        key, user_pic_url, user_name, gender, address, job, education, description =item['key'], item['user_pic_url'], item['user_name'], item[
            'gender'], item['address'], item['job'], item['education'], item['description']
        sql = 'insert into zhihu_alluser values(%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql, [key, user_pic_url, user_name, gender, address or 0, job or 0, education or 0, description or 0])
            print('新增加一个数据')
        except:
            pass
        # print(user_pic_url , user_name , gender , address , job , education)

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            # host='120.92.77.36',  # 数据库地址
            host='localhost',  # 数据库地址
            # port=48368,  # 数据库端口
            port=3306,  # 数据库端口
            db='spider_resource',  # 数据库名
            # user='bd_ceshi',  # 数据库用户名
            user='root',  # 数据库用户名
            # passwd='BDqilingzhengfan1',  # 数据库密码
            passwd='123456',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)
        print('爬虫已开启')

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
        print('爬虫已关闭')

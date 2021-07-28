# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

#连接数据库
def dbHandle():
    conn = pymysql.connect(
        host = "localhost",
        user = "webprocess",
        passwd = "p1aaiihZ>ir2e_OG",
        charset = "utf8",
        use_unicode = False
    )
    return conn

class Project1Pipeline:
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE web_project_1")
        sql = """INSERT INTO teacher(name,position,phone,email,fax,research) VALUES(%s,%s,%s,%s,%s,%s)"""
        if len(item['position'])==0:
            item['position'] = ''
        if len(item['phone'])==0:
            item['phone'] = ''  
        if len(item['email'])==0:
            item['email'] = ''
        if len(item['fax'])==0:
            item['fax'] = ''  
        if len(item['research'])==0:
            item['research'] = ''                          
        try:
            cursor.execute(sql,
                           ( item['name'], item['position'], item['phone'], item['email'], item['fax'], item['research']))
            cursor.connection.commit()
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
            dbObject.rollback()
        
        return item

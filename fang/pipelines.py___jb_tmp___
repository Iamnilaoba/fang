# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os,json
from scrapy.exporters import JsonLinesItemExporter
BASE_URL=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class FangPipeline(object):
    def process_item(self, item, spider):
        province=item["province"]
        city=item["city"]
        province_path=os.path.join(BASE_URL,province)
        if not os.path.exists(province_path):
            os.mkdir(province_path)
        city_path=os.path.join(province_path,city)
        if not os.path.exists(city_path):
            os.mkdir(city_path)
        newHomePath=os.path.join(city_path,"home.json")
        with open(newHomePath,"a+") as f:
            f.write(json.dumps(item.__dict__,ensure_ascii=False) + '\n')
        return item

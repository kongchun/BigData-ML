# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: 曹茂国
"""
#数据库中读取数据
import pymongo as mongo;
class MongoClass:
    #获取数据库连接
    def __init__(self, ip, port,sheep,table):
      conn = mongo.MongoClient(ip,port);
      print conn
      if conn:
          db = conn[sheep];
          self.collect = db[table];
      else:
          return None;
          
    #mongo数据库查询操作    
    def find_mongo(self,filter):
        all_data = self.collect.find(filter).sort('id',mongo.ASCENDING);
        re_data = self.tran_mongo_array(all_data);
        return re_data;
        
    #mongo数据库更新操作     
    def updata_mongo(self,old,new):
        self.collect.update(old,{'$set':new}, multi=True)
        
        
    #mongo数据库更新操作     
    def insert_mongo(self,data):
        self.collect.save(data)
        
    #查询mongo数据库得到数据转换成对象数组
    def tran_mongo_array(self,data):
        list_data = [];
        for i in data:
            list_data.append(i);
        return list_data;
        

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: Administrator
"""
#数据库中读取数据
import pymongo_class as mongdb_class
import pandas as pd       
    
dataunion = mongdb_class.MongoClass('10.82.0.1',27017,'bigdata','dataunion');
artlist = dataunion.find_mongo({});
datayuan = mongdb_class.MongoClass('10.82.0.1',27017,'bigdata','datayuan');
artlist1 = datayuan.find_mongo({});
#数据模型转换
docs1 = pd.DataFrame(artlist);
docs1['mongoname'] = 'dataunion'
docs2 = pd.DataFrame(artlist1);
docs2['mongoname'] = 'datayuan'
docs = docs1.append(docs2,True)
import MLaction
MLaction.action(docs);
dataunion.updataMore_mongo({"isNew" : True},{"isNew" :False })
datayuan.updataMore_mongo({"isNew" : True},{"isNew" :False })
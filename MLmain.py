# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: Administrator
"""
#数据库中读取数据
import pymongo_class as mongdb_class
import pandas as pd       
    
dataunion = mongdb_class.MongoClass('10.82.0.1',27017,'bigdata','dataunions');
artlist = dataunion.find_mongo({});
datayuan = mongdb_class.MongoClass('10.82.0.1',27017,'bigdata','datayuans');
artlist1 = datayuan.find_mongo({});
#jiqizhixin = mongdb_class.MongoClass('10.82.0.1',27017,'bigdata','jiqizhixins');
#artlist2 = jiqizhixin.find_mongo({});
leiphone = mongdb_class.MongoClass('10.82.0.1',27017,'bigdata','leiphones');
artlist3 = leiphone.find_mongo({});
#数据模型转换
doc  = pd.DataFrame(artlist);
docs1 = pd.DataFrame(artlist1);
#docs2 = pd.DataFrame(artlist2);
docs3 = pd.DataFrame(artlist3);
docs = doc.append(docs1,True).append(docs3,True)
docs = docs.sort(column='createDate', ascending=False)


import MLaction
MLaction.action(docs); 
dataunion.updata_mongo({"isnew" : True},{"isnew" :False })
datayuan.updata_mongo({"isnew" : True},{"isnew" :False })
#jiqizhixin.updata_mongo({"isnew" : True},{"isnew" :False })
leiphone.updata_mongo({"isnew" : True},{"isnew" :False })
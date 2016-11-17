# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: 曹茂国
"""
#获取相似文章
import pandas as pd
from sklearn.neighbors import NearestNeighbors
class NeighborsClass:
    def __init__(self, docs,tfidf):
      self.model = self.get_train_model(tfidf);
    #获取训练模型
    def get_train_model(self,data): 
        model = NearestNeighbors(metric='euclidean', algorithm='brute')
        model.fit(data)
        return model
    #获取相似文章id  
    def get_neighbors(self,tfidf,index):
        distances, indices = self.model.kneighbors(tfidf[index], n_neighbors=6) # 1st
        neighbors = pd.DataFrame({'distance':distances.flatten(), 'id':indices.flatten()}) 
        return neighbors['id'];   
    #相似文章数据库id以逗号分隔组成字符串    
    def get_id_str(self,similar,docs):
        str_id = "";
        for j in range(1,len(similar)):
            index = similar[j];
            similar_id = docs.loc[index,'id'];
            str_id = str_id + str(similar_id) + ",";
        return str_id[0:len(str_id)-1];   
    
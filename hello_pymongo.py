# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: Administrator
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
    def find_mongo(self):
        all_data = self.collect.find();
        re_data = self.tran_mongo_array(all_data);
        return re_data;
        
    #mongo数据库更新操作     
    def updata_mongo(self,old,new):
        self.collect.update_one(old,{'$set':new})
        
    #查询mongo数据库得到数据转换成对象数组
    def tran_mongo_array(self,data):
        list_data = [];
        for i in data:
            list_data.append(i);
        return list_data;
        

    
get_mongo = MongoClass('10.82.0.1',27017,'dataunion','articles');
artlist = get_mongo.find_mongo();

#   
import pandas as pd

docs = pd.DataFrame(artlist);
docs['all_content'] = docs['title'] + docs['content'];


import jieba
import jieba.analyse
#分词
def sentence_to_split_word(str):
    jieba.load_userdict("./dict.txt") # file_name为自定义词典的路径
    str_to_word = jieba.cut(str, cut_all=False)
    #str_to_word = jieba.analyse.extract_tags(str, topK=40, withWeight=False)
    return ' '.join(str_to_word)

# 增加一列，把文本进行分词
docs['text_split_word']=docs['all_content'].apply(sentence_to_split_word)

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

#获取分词的tf-idf权重
def get_tf_idf(data):
    vectorizer = CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(vectorizer.fit_transform(data))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()#获取词袋模型中的所有词语
    return tfidf,word
#weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重   
#数据库中更新abstract字段
def dump_weigh_with_word(word,get_mongo):
    for i in range(len(docs)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        listAbstract = dict();
        listAbstract['word'] = word;
        weight = tfidf[i].toarray();
        listAbstract['value'] = weight[0];
        frameAbstract = pd.DataFrame(listAbstract); 
        frame_sort = frameAbstract.sort(['value'], ascending=0)
        abstract = ",".join(frame_sort['word'][0:10])
        id = docs['id'][i]
        get_mongo.updata_mongo({'id':int(id)},{'abstract':abstract})
        
corpus = docs['text_split_word']        
(tfidf,word) = get_tf_idf(corpus)
docs['tfidf'] = tfidf
dump_weigh_with_word(word,get_mongo);   

str_title = docs['title'][4]
doc = docs[docs['title']==str_title]
doc.index

#获取相似文章
from sklearn.neighbors import NearestNeighbors
#获取训练模型
def get_train_model(data): 
    model = NearestNeighbors(metric='euclidean', algorithm='brute')
    model.fit(data)
    return model
#获取相似文章id  
def get_neighbors(model,tfidf,index):
    distances, indices = model.kneighbors(tfidf[index], n_neighbors=6) # 1st
    neighbors = pd.DataFrame({'distance':distances.flatten(), 'id':indices.flatten()}) 
    return neighbors['id'];   
#相似文章数据库id以逗号分隔组成字符串    
def get_id_str(similar,docs):
    str_id = "";
    for j in range(1,len(similar)):
        index = similar[j];
        similar_id = docs.loc[index,'id'];
        str_id = str_id + str(similar_id) + ",";
    return str_id[0:len(str_id)-1];   
#mongo数据库更新similar字段    
def updata_similar(docs,tfidf,model,get_mongo):
    for i in range(len(docs)):
       similar_index = get_neighbors(model,tfidf,i); 
       str_id = get_id_str(similar_index,docs);
       self_id = docs.loc[i,'id'];
       get_mongo.updata_mongo({'id':int(self_id)},{'similar':str_id})
   
model = get_train_model(tfidf)
updata_similar(docs,tfidf,model,get_mongo)
del get_mongo;

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: Administrator
"""
#数据库中读取数据
import pymongo_class as mongdb_class       
    
get_mongo = mongdb_class.MongoClass('10.82.0.1',27017,'bigdata','dataunion');
artlist = get_mongo.find_mongo({});
#数据模型转换
import pandas as pd
docs = pd.DataFrame(artlist);
docs['all_content'] = docs['title'] + docs['content'];

#结巴分词
import td_idf_jieba as  word_weight
getWeight = word_weight.WordWeight();
# 增加一列，把文本进行分词
docs['text_split_word']=docs['all_content'].apply(getWeight.sentence_to_split_word)

#weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重   
#数据库中更新abstract、重点语句字段
import MLget_keyword
corpus = docs['text_split_word']        
(tfidf,word_freq,word) = getWeight.get_tf_idf(corpus)
docs['tfidf'] = tfidf
ml = MLget_keyword.GetKeyWord(docs, word, tfidf, word_freq, getWeight, 'dataunion');   


import find_neighbors as neighbor
#mongo数据库更新similar字段    
sklearn_model = neighbor.NeighborsClass(docs,tfidf);
ml.updata_similar(sklearn_model, get_mongo)

#关键字排序
ml.insert_keyword()
ml.del_mongodb();

del get_mongo;
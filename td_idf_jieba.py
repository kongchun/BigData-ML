# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: 曹茂国
"""
#数据库中读取数据
import jieba
import jieba.analyse
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
class WordWeight:
    #分词
    def sentence_to_split_word(self,str):
        #jieba.load_userdict("./dict.txt") # file_name为自定义词典的路径
        str_to_word = jieba.cut(str, cut_all=False);
        #str_to_word = jieba.analyse.extract_tags(str, topK=40, withWeight=False)
        return  ' '.join(str_to_word)
        
        #获取分词的tf-idf权重
    def get_tf_idf(self,data):
        vectorizer = CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        transformer = TfidfTransformer()#该类会统计每个词语的tf-idf权值
        tfidf = transformer.fit_transform(vectorizer.fit_transform(data))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
        word = vectorizer.get_feature_names()#获取词袋模型中的所有词语
        return tfidf,word
        
    def delete_stop_word(self,word,num):
        stopwords = {}.fromkeys([ line.rstrip().decode('utf-8') for line in open('stop_word.txt').readlines() ])
        str = [];
        for i in word:
            if i not in stopwords:
                str.append(i); 
        return str[0:num];
        

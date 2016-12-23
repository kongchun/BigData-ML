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
import MLbaidu as baidu
import math
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
        word_freq = vectorizer.fit_transform(data)#fit_transform是将文本转为词频矩阵
        tfidf = transformer.fit_transform(word_freq)#第一个fit_transform是计算tf-idf
        word = vectorizer.get_feature_names()#获取词袋模型中的所有词语      
        return tfidf,word_freq,word
        
    def delete_stop_word(self,word,num):
        stopwords = {}.fromkeys([ line.rstrip().decode('utf-8') for line in open('stop_word.txt').readlines() ])
        str = [];
        for i in word:
            if i not in stopwords:
                str.append(i); 
        return str[0:num];

    def docs_tdidf(self, word, i, word_freq, tfidf):
        listAbstract = dict();
        listAbstract['word'] = word;
        weight = tfidf[i].toarray();               #权重
        word_freq_weight = word_freq[i].toarray()  #词频
        listAbstract['value'] = weight[0];
        listAbstract['word_freq'] = word_freq_weight[0]/max(word_freq_weight[0]) #归一化
        return listAbstract;
        
    def reget_tdidf(self, frame_sort, total_docs, search_baidu):
        alreadyContent = search_baidu.get_word();
        new_tdidf = []
        baidu_df = {}
        for i in range(len(frame_sort)):
            word_arry = frame_sort['word'][i:i+1].values;
            value_arry = frame_sort['value'][i:i+1].values
            df = 0;
            word = word_arry[0]
            value = value_arry[0]
            if word not in alreadyContent:
                df = search_baidu.get_df(word)
                baidu_df[word] = df
                search_baidu.set_df(word,df)
            else:
                df = alreadyContent[word]
                            
            if df <= 50:
                new_tdidf.append(0)
            else:
                new_tdidf.append(value*math.log(total_docs/(1+df)))                  
        frame_sort['new_tdidf'] =  new_tdidf;     
        return frame_sort.sort(['new_tdidf'], ascending=0),baidu_df; 
        

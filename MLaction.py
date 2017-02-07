# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: Administrator
"""
import td_idf_jieba as  word_weight
import MLget_keyword
import find_neighbors as neighbor
class action:
    #初始化
    def __init__(self, docs):
        
        docs['all_content'] = docs['title'] + docs['content'];
        #结巴分词    
        getWeight = word_weight.WordWeight();
        # 增加一列，把文本进行分词
        docs['text_split_word']=docs['all_content'].apply(getWeight.sentence_to_split_word);
        
        #weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重   
        #数据库中更新abstract、重点语句字段
        corpus = docs['text_split_word']        
        (tfidf,word_freq,word) = getWeight.get_tf_idf(corpus);
        docs['tfidf'] = tfidf;
        ml = MLget_keyword.GetKeyWord(docs, word, tfidf, word_freq, getWeight);   
        
        #mongo数据库更新similar字段
        article = ml.get_articles();
        article['all_content'] = article['title'] + article['content'];
        article['text_split_word']=article['all_content'].apply(getWeight.sentence_to_split_word);
        article_corpus = article['text_split_word']        
        (article_tfidf,article_word_freq,article_word) = getWeight.get_tf_idf(article_corpus);
        article['tfidf'] = article_tfidf;
        sklearn_model = neighbor.NeighborsClass(article,article_tfidf);
        ml.updata_similar(article,sklearn_model,article_tfidf);
        
        #关键字排序
        ml.insert_keyword();
        ml.del_mongodb();

        
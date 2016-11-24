# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: Administrator
"""
#数据库中读取数据
import pymongo_class as mongdb_class       
    
get_mongo = mongdb_class.MongoClass('10.82.0.1',27017,'dataunion','articles');
artlist = get_mongo.find_mongo();

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
#数据库中更新abstract字段
def dump_weigh_with_word(word,get_mongo):
    for i in range(len(docs)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        listAbstract = dict();
        listAbstract['word'] = word;
        weight = tfidf[i].toarray();
        listAbstract['value'] = weight[0];
        frameAbstract = pd.DataFrame(listAbstract); 
        frame_sort = frameAbstract.sort(['value'], ascending=0)
        key_word = getWeight.delete_stop_word(frame_sort['word'][0:30],10)
        abstract = ",".join(key_word)
        id = docs['id'][i]
        get_mongo.updata_mongo({'id':int(id)},{'abstract':abstract})
        
        paragraph_obj = dict();
        html_art = docs['html'][i]
        paragraph = html_art.split("<p>")
        for temp in paragraph:
            paragraph_temp = temp.split("</p>")[0]
            paragraph_obj[paragraph_temp] = 0
            for key_i in key_word:
                if key_i in  paragraph_temp:
                    paragraph_obj[paragraph_temp] += 1
        paragraph_obj_list = sorted(paragraph_obj.iteritems(),key=lambda d:d[1],reverse=True)
        main_p = paragraph_obj_list[0][0]
        new_html = html_art.replace("<p>" + main_p +"</p>", "<p style='color:red;font-weight:bold;'>" + main_p +"</p>",  1)
        get_mongo.updata_mongo({'id':int(id)},{'brief':main_p,'html':new_html})
        
        
corpus = docs['text_split_word']        
(tfidf,word) = getWeight.get_tf_idf(corpus)
docs['tfidf'] = tfidf
dump_weigh_with_word(word,get_mongo);   



import find_neighbors as neighbor
#mongo数据库更新similar字段    
def updata_similar(docs,tfidf,get_mongo):
    for i in range(len(docs)):
       similar_index = sklearn_model.get_neighbors(tfidf,i); 
       str_id = sklearn_model.get_id_str(similar_index,docs);
       self_id = docs.loc[i,'id'];
       get_mongo.updata_mongo({'id':int(self_id)},{'similar':str_id})
sklearn_model = neighbor.NeighborsClass(docs,tfidf);
updata_similar(docs,tfidf,get_mongo)


del get_mongo;
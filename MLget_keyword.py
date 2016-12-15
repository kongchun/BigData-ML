# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: Administrator
"""
import pandas as pd
import time
import pymongo_class as mongdb_class  
class GetKeyWord:
    #初始化
    def __init__(self, docs, word, tfidf, getWeight, mongo_name):
        self.articles = mongdb_class.MongoClass('10.82.0.1',27017,'bigdata','articles');
        self.word_relation = mongdb_class.MongoClass('10.82.0.1',27017,'bigdata','word_relation');
        self.mongo_name = mongo_name;
        self.docs = docs;
        self.insert_data = dict();
        self.tfidf = tfidf
        self.getkeyword(word, getWeight)
        
    #查找关键字
    def getkeyword(self, word, getWeight):
        docs = self.docs
        tfidf = self.tfidf
        for i in range(len(docs)):
            if docs['isNew'][i]:
                listAbstract = dict();
                listAbstract['word'] = word;
                weight = tfidf[i].toarray();
                listAbstract['value'] = weight[0];
                frameAbstract = pd.DataFrame(listAbstract); 
                frame_sort = frameAbstract.sort(['value'], ascending=0);
                key_word = getWeight.delete_stop_word(frame_sort['word'][0:30],10);
                abstract = ",".join(key_word);
                (new_html,keyword_list) = self.find_mainparagraph(i,key_word);
                self.createNewData(i, abstract, new_html, keyword_list)
        
    #查找重点语句    
    def find_mainparagraph(self, i, key_word):
        docs = self.docs
        keyword_list = dict();
        paragraph_obj = dict();
        html_art = docs['html'][i]
        paragraph = html_art.split("<p>")
        for temp in paragraph:
            paragraph_temp = temp.split("</p>")[0]
            paragraph_obj[paragraph_temp] = 0
            for key_i in key_word:
                keyword_list[key_i] = 0
                if key_i in  paragraph_temp:
                    paragraph_obj[paragraph_temp] += 1
        paragraph_obj_list = sorted(paragraph_obj.iteritems(),key=lambda d:d[1],reverse=True)
        main_p = paragraph_obj_list[0][0]
        new_html = html_art.replace("<p>" + main_p +"</p>", "<p style='background-color: #FDF6E3;'>" + main_p +"</p>",  1)
        return new_html,keyword_list;
    
    #整理之后的数据插入数据库    
    def createNewData(self, i, abstract, new_html, keyword_list):
        docs = self.docs
        id = docs['id'][i]
        insert_id = long(time.time()*1000);
        self.articles.insert_mongo({"id":insert_id,"thumbnail":docs['thumbnail'][i],"content":docs['content'][i],"createDate":docs['createDate'][i],"artid":int(id),'html':new_html,'mongoname': self.mongo_name,'tags':docs['tags'][i],'abstract':abstract,'title':docs['title'][i],'url':docs['url'][i],'similar':'','hits':int(docs['hits'][i])});
        self.insert_data[id] = insert_id;
        self.word_relation.insert_mongo({"id":insert_id,"artid":int(id),"keyword":keyword_list})
    
    #插入相似性文章    
    def updata_similar(self, sklearn_model, get_mongo):
        docs = self.docs
        tfidf = self.tfidf
        insert_data = self.insert_data;
        for i in range(len(docs)):
            if docs['isNew'][i]:
                similar_index = sklearn_model.get_neighbors(tfidf,i); 
                str_id = sklearn_model.get_id_str(similar_index,docs,self.articles,self.mongo_name);
                self_id = docs.loc[i,'id'];
                insert_id = insert_data[self_id]
                self.articles.updata_mongo({'id':long(insert_id)},{'similar':str_id})
                get_mongo.updata_mongo({"id":int(self_id)},{'isNew':False});
        del self.articles
        del self.word_relation
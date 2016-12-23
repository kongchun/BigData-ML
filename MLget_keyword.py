# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: Administrator
"""
import pandas as pd
import time
import pymongo_class as mongdb_class 
import MLbaidu as baidu 
class GetKeyWord:
    #初始化
    def __init__(self, docs, word, tfidf, word_freq, getWeight, mongo_name):
        self.ip = '10.82.0.1';
        self.port = 27017;
        self.table = 'bigdata';
        self.articles = mongdb_class.MongoClass(self.ip , self.port,self.table,'articles');
        self.word_relation = mongdb_class.MongoClass(self.ip , self.port,self.table,'word_relation');
        self.mongo_name = mongo_name;
        self.docs = docs;
        self.insert_data = dict();
        self.tfidf = tfidf;
        self.keyword = dict();
        self.getkeyword(word, getWeight, word_freq)
        
    #查找关键字
    def getkeyword(self, word, getWeight, word_freq):
        docs = self.docs
        baidu_search = baidu.baidu_search();
        total_docs = baidu_search.get_totalDf();
        baidu_word = {}
        for i in range(len(docs)):
            if docs['isNew'][i]:
                listAbstract = getWeight.docs_tdidf(word, i, word_freq, self.tfidf) #获取文章的词、权重、词频矩阵
                frameAbstract = pd.DataFrame(listAbstract); 
                frameAbstractSortTfidf = frameAbstract.sort(['value'], ascending=0)[0:30];
                (frame_sort,baidu_df) = getWeight.reget_tdidf(frameAbstractSortTfidf,total_docs,baidu_search)
                baidu_word.update(baidu_df)
                key_word = getWeight.delete_stop_word(frame_sort['word'][0:30],10);
                abstract = ",".join(key_word);
                (new_html,keyword_list) = self.find_mainparagraph(i,key_word);
                self.save_keyword(key_word)
                self.createNewData(i, abstract, new_html, keyword_list)
        baidu_search.write_search(baidu_word)                   
        
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
        
    def save_keyword(self,key_word):
        for key_i in key_word:
            if key_i not in self.keyword:
                self.keyword[key_i] = 1;
            else:
                self.keyword[key_i] = self.keyword[key_i] + 1;
    
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
    #关键字排序
    def insert_keyword(self):
        keyword_log = mongdb_class.MongoClass(self.ip , self.port,self.table,'keyword_log');
        keyword_sort = mongdb_class.MongoClass(self.ip , self.port,self.table,'keyword_sort');        
        insert_id = long(time.time()*1000);
        keyword_log.insert_mongo({"id":insert_id,"keyword":self.keyword});
        keword_data = keyword_log.find_mongo({});
        (arry_week,arry_month) = self.sort_keyword(keword_data)
        keyword_sort.insert_mongo({"id":insert_id,"week":arry_week,"month":arry_month})
        del keyword_log;
        del keyword_sort;
   
    def sort_keyword(self,keword_data):    
        len_week = 10;
        len_month = 10;
        (word_week,word_month) = self.count_word(keword_data);
        sort_week = sorted(word_week.iteritems(), key=lambda d:d[1], reverse = True)[0:len_week]
        arry_week = [];
        for k in range(len(sort_week)):
            word = dict();
            word['word'] = sort_week[k][0];
            word['value'] = sort_week[k][1];
            arry_week.append(word);
        sort_month = sorted(word_month.iteritems(), key=lambda d:d[1], reverse = True)[0:len_month]
        arry_month = [];
        for k in range(len(sort_month)):
            word = dict();
            word['word'] = sort_month[k][0];
            word['value'] = sort_month[k][1];
            arry_month.append(word);
        return arry_week,arry_month
        
    def count_word(self,keword_data):
        word_week = dict();
        word_month = dict();
        week = 7;
        month = 30;
        for i in range(month):
            if len(keword_data) > i:
                temp_keyword = keword_data[i]["keyword"]
                for k in temp_keyword:
                    if k not in word_month:
                        word_month[k] = temp_keyword[k];
                    else:
                        word_month[k] = word_month[k] + temp_keyword[k]; 
                    if i < week:
                        if k not in word_week:
                            word_week[k] = temp_keyword[k];
                        else:
                            word_week[k] = word_week[k] + temp_keyword[k];
        return word_week,word_month
        
    def del_mongodb(self):
        del self.articles
        del self.word_relation
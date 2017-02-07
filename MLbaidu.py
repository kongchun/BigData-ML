# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:14:53 2016

@author: Administrator
"""
#数据库中读取数据
import socket
import time
import urllib
import urllib2
import codecs 
class baidu_search:
     #初始化
    def __init__(self):
        #获取文档频数
        self.url = "http://wenku.baidu.com/";
        self.path = "E:/git_pro/BigData-ML/result_baidu.txt"
        self.word_dict = self.read_search();
        
    def get_df(self,word):
        findStr = word
        findStr = urllib.quote(findStr.encode('gbk', 'replace'))
        url = self.url + "search?word="+ findStr +"&org=0"
        timeout = 100
        socket.setdefaulttimeout(timeout)
        sleep_download_time=1
        time.sleep(sleep_download_time)
        try:
            req = urllib2.Request(url)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
        except IOError:
            print "Error: 没有搜索成功"
            return -1
        else:
            res_data.close()
            art = res.decode("gbk",'replace');
            strs = u'找到相关文档约'
            indexs = art.find(strs)
            if(indexs<0):
                df = 0
            else:
                count = art[indexs+7:].split(u"篇")[0]
                df = int(count.replace(",",""))
            return df
    #获取总的文档数
    def get_totalDf(self):
        url_wenku = self.url
        req_wenku = urllib2.Request(url_wenku)
        res_data_wenku = urllib2.urlopen(req_wenku)
        res_wenku = res_data_wenku.read()
        art_wenku = res_wenku.decode("gbk",'replace');
        strs_wenku = u'data-docnum'
        indexs_wenku = art_wenku.find(strs_wenku)
        count_wenku = art_wenku[indexs_wenku:indexs_wenku+30].split(u"\"")[1]
        total_docs = (int(count_wenku.replace(",","")))
        return total_docs
        
    def read_search(self):
        alreadyContent = {}
        f = codecs.open(self.path,'r');
        with f as df:
            for kv in [d.strip().split(' ') for d in df]:
                alreadyContent[kv[0]] = int(kv[1])
        f.close()
        return alreadyContent
        
        
    def write_search(self,arry):
        f = codecs.open(self.path,'w+','utf-8')
        write_str = "";
        for i in arry:
            write_str = write_str +  i + " " + str(arry[i]) + " " + "\r\n"
        f.write(write_str)
        f.close();
    def get_word(self):
        return self.word_dict
    def set_df(self,word,vaule):
        self.word_dict[word] = vaule
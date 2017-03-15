# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 15:40:47 2017

@author: xiaol
"""
import addNewWord as addNewWord
import numpy

#简单处理标签


#分析
#技术类：通过获取词频数就行
#IT领域类：通过获取词频也行
#IT企业类：获取词频行
#应用类：获取词频行
#国内及国际发展：比较麻烦，需要获取其他词频来获取
class tagClass:
    def __init__(self,docs):
        self.tagArray = [["深度学习","可视化","机器学习","数据挖掘"],
                ["人工智能","AI","大数据","互联网","互联网+","移动互联网","云计算","语音识别"],
                ["百度","腾讯","谷歌","阿里","微软","英特尔","苹果","亚马逊"],
                ["电商","金融","投资","股票","融资","医疗","教育","自驾","自动驾驶","无人车","通信","个人助理","安防","虚拟现实","文娱","旅游","媒体"]]
        self.tagTree=dict({"人工智能":["AI"],"金融":["投资","股票","融资"],"自动驾驶":["无人车"],"文娱":["旅游","媒体"]})
        self.allTag = self.getAllTag(self.tagArray)
        docs['titleTagVal'] = docs['wordTitle'].apply(self.getTagVal)
        docs['contentTagVal'] = docs['wordContent'].apply(self.getTagVal)
        titleTagVal = docs['titleTagVal']
        contentTagVal = docs['contentTagVal']
        docs['tagVal']= titleTagVal + contentTagVal
        self.tagVal = docs['tagVal']
        self.tag = docs['tagVal'].apply(self.getTag)

        
    addNewWord.addNewWord()
    #获取所有标签    
    def getAllTag(self,tagArray):
        allTag = []
        for tagArr in tagArray:
            allTag.extend(tagArr)
        return allTag
    #获取标签出现的频度
    def getCount(self,words,tags):
        wordsList = words.split()
        freqVal = []
        for w in tags:
            freqVal.append(wordsList.count(w))
        return freqVal
     
    #归一化处理
    def normalrize(self,arr):
        arr = arr/1.0
        maxVal = arr.max()
        minVal = arr.min()
        if(maxVal>minVal):
            arr = arr/(maxVal-minVal)
        elif(maxVal>0):
                arr = arr/maxVal
        return arr
    
    #根据标签及其频度创建字典
    def createDic(self,tags,tagVal):
        tagDic = dict.fromkeys(tags,0)
        lenTag = len(tags) 
        index = 0
        while(index<lenTag):
            tagDic[tags[index]]=tagVal[index]
            index = index+1
        return tagDic
          
    #获取标签归一化之后比重
    def getTagVal(self,words):
        tagV = []
        for tags in self.tagArray:
            tagFreqVal = self.getCount(words,tags)
            tagValArr = numpy.array(tagFreqVal)
            a=self.normalrize(tagValArr)
            tagV.append(a)
        return numpy.array(tagV)
     
    #根据标签归一化之后的比重获取文章的标签
    def getTag(self,tagVal):    
        tag = []
        numTagCategory =len( tagVal)
        index = 0
        #首先获取Tree中的所有key值
        keys = self.tagTree.keys()
        while(index<numTagCategory):
            tagDic = self.createDic(self.tagArray[index],tagVal[index])
            ###在此处处理tag
            for seq in self.tagArray[index]:
                if((seq in keys)==True):
                    for seqChild in self.tagTree[seq]:
                        tagDic[seq] = tagDic[seq]+tagDic[seqChild]
                        tagDic[seqChild]=0
            sortTagDic = sorted(tagDic.items(),key = lambda d:d[1],reverse = True)
            for t in sortTagDic:
                if(t[1]>0.1):
                    tag.append(t[0])
                else:
                    break
            index = index+1
        return tag
            


    

    


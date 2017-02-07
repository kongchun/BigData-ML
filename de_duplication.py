# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 14:02:37 2017

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 18:26:20 2017

@author: admin
"""

import simhashAlgorithm
class deduplicationClass:
    def __init__(self,docNew,docsAticles):
        self.contentLen=150
        self.duplicate = self.isDuplicate(docNew,docsAticles)

    #提前预处理html的转义字符        
    def preProcess(self,strcontent):
#        specialIndex = str.find('▼')
#        while(specialIndex!=-1):
#            str = str[:specialIndex]+str[specialIndex+1:]
#            specialIndex = str.find('▼',specialIndex)
        andIndex = strcontent.find('&')
        while(andIndex!=-1):
            semicolonIndex = strcontent.find(';',andIndex)
            if(andIndex<semicolonIndex+1):
                strcontent = strcontent[:andIndex]+strcontent[semicolonIndex+1:]
            else:
                strcontent = strcontent[:andIndex]+strcontent[andIndex+1:]
            andIndex = strcontent.find('&',andIndex)
        return strcontent
    



    #根据simhash算法判断两篇文章d1和d2是否相同
    def isDuplicateTwo(self,d1,d2):
        hash1 = simhashAlgorithm.simhash(d1.split())
        hash2 = simhashAlgorithm.simhash(d2.split())
        if(hash1.hamming_distance(hash2)>=3):
            return False
        else:
            return True
  


#def checkDoc(doc1,doc2):
#    numOfDoc1 = len(doc1)
#    numOfDoc2 = len(doc2)
#    index1 = 0
#    index2 = 0
#    while index1<numOfDoc1:
#        while index2<numOfDoc2:
#            if(isDistinct(doc1[index1],doc2[index2])!=True):
#                print 'index1:'+str(index1)+' '+'index2:'+str(index2)#当遇到重复的文章时，处理步骤
#            index2 = index2+1
#        index1 = index1+1


    
    #比较新数据和已有数据中是否有重复
    def isDuplicate(self,docNew,docsAticles): 
        docNewProcess= self.preProcess(docNew)#预处理之后新文章
        docsAticles['newContent'] = docsAticles['content'].apply(self.preProcess)#预处理之后的旧文章
        docsAticlesProcess = docsAticles['newContent']
        numDocs = len(docsAticlesProcess)#旧文章数目
        if(len(docNewProcess)>self.contentLen):
            index = 0
            while(index<numDocs):
#                print(index)
                if(self.isDuplicateTwo(docNewProcess,docsAticlesProcess[index])==True):
                    return True
                index = index+1
        return False
        
        
        #比较新数据中是否有重复
#    def checkDoc(self,docsNew): 
#        docsNew['newContent'] = docsNew['content'].apply(self.preProcess)
#        docNew = docsNew['newContent']
#        numDoc = len(docNew)
#        index1 = 0
#        del_id=[]
#        del_index=[]
#        while(index1<numDoc-1):
#            print index1
#            if(self.index(del_index,index1)==True):
#                index1 = index1+1
#                continue
#            if(len(docNew[index1])>self.contentLen):
#                index2 = index1+1
#                while(index2<numDoc):
#                    if(self.isDistinct(docNew[index1],docNew[index2])!=True):
#                        del_id.append(docsNew['id'][index2])
#                        del_index.append(index2)
#                        print ('id:'+str(docs['id'][index1])+'与'+'id:'+str(docs['id'][index2])+'重复')#当遇到重复的文章时，处理步骤
#                    index2 = index2+1
#            index1 = index1+1
#        return del_id



#    def removDuplicateRecord(self,get_mongoDS):
#        for del_id_value in self.del_id:
#            value = numpy.long(del_id_value)
#            get_mongoDS.del_id_mongo({"id":value})
        
        



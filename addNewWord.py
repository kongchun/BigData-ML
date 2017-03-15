# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:33:24 2017

@author: xiaol
"""

import jieba
class addNewWord:
    def __init__(self):
        self.newWordPath="newWord.txt"
        self.add_new_word()
    
    def add_new_word(self):
        f = open(self.newWordPath,'r')
        for w in f:
            jieba.add_word(w.strip(),freq=None,tag=None)
        f.close()
        
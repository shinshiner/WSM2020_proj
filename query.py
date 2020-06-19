#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import math
import json
import pkuseg
import numpy as np 
from scipy import sparse
from pprint import pprint
from nltk.stem.porter import PorterStemmer
import time


def txt2dict_mod(filename):
    doc_dictionary = {}
    file = open(filename,'r',encoding='utf-8')
    for line in file.readlines():

        k = (line.split('{')[0])[0:-1]
        v_temp = (line.split('{')[1])[0:-2]
        v_temp = v_temp.split(',')
        
        v = {}
        for item in v_temp:
            if item[0] == ' ':
                key =  (item.split(':')[0])[2:-1]

                value = (item.split(':')[1])[1:]
                value = float(value)
            else:
                key = (item.split(':')[0])[1:-1]
                value = (item.split(':')[1])[1:]
                value = float(value)
            v[key] =value
        
        doc_dictionary[k] = v
    
    return doc_dictionary


#initialisation
idf_dictionary = {}
doc_dictonary = {}
dis_dict = {}
normalized_dict = {}

stemmer = PorterStemmer()
seg = pkuseg.pkuseg()

path = "data/hshfy_wenshu"

#read the list of stopwords
stopword=[]
cfp = open('data/stopwords/trunk/cn_stopwords.txt','r+',1,encoding='utf-8')
for line in cfp:
    for word in line.split():
        stopword.append(word)
cfp.close()
       
# load the normalize dict
t = time.time()
normalized_dict= txt2dict_mod('data/normalize_dict.txt')
print('load normalized dict, use time: ', time.time() - t)


def getweight(filename,token):
    list_query = []
    new_term=0
    dot_pro=0
    doc1=normalized_dict[filename]
    query_tfdict = query_vector(token)

    for name,value_idf in query_tfdict.items():
        if name in doc1.keys():
            list_query.append(name)
            dot_pro = dot_pro + value_idf*doc1[name]
        else:
            return 0;
    return (dot_pro,list_query)


def query_vector(token):
    query_dictionary = {}
    query_tfdict = {}
    tf_value=0
    tokens = seg.cut(token)
    word_dictionary = {}
    stops = set(stopword)
    for word in tokens:
        if word.lower() not in stops:
            new_word = stemmer.stem(word)
            if new_word in query_dictionary.keys():
                query_dictionary[new_word] += 1
            else:
                query_dictionary[new_word] = 1
    euc_dis=0

    for name,frequency in query_dictionary.items():
        tf_value = 1 + math.log10(frequency)
        query_tfdict[name] = tf_value
        euc_dis += tf_value*tf_value
    query_norm_tfdict = {}
    for word,un_normalized_val in query_tfdict.items():
        query_norm_tfdict[word] = un_normalized_val / math.sqrt(euc_dis)
    return query_norm_tfdict


def getweight_query(token):
    dot_max = 0
    dot_pro_list = {}
    result = {}
    list_query = {}
    dot_max_key = []

    for filename,doc in normalized_dict.items():
        temp = getweight(filename,token)
        if(temp != 0):
            weight = temp[0]
            match = temp[1]
            list_query[filename] = match
            dot_pro_list[filename] = weight
        else :
            dot_pro_list[filename] = temp
    dot_max = max(dot_pro_list.values())

    for key,value in dot_pro_list.items():
        if(value>0 ):
            dot_max_key.append(key)

    if dot_max > 0:
        for key in dot_max_key :
            result[key] = dot_pro_list[key]
        result = sorted(result.items(), key=lambda x: x[-1], reverse=True)
    else :
        result = {}
        print("we do not find any relevant instrument")
    d3 = {}
    d3.update(result)
    d3.update(list_query)
    d3 = list(d3.items())

    return d3


if __name__ == '__main__':
    t = time.time()
    getweight_query("该合同系双方真实意思表示，被告没有利用强势地位强行与原告签订合同。")
    print(time.time() - t)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import shutil
import os
import math
import json
import pkuseg
import numpy as np 
from scipy import sparse
from pprint import pprint
import collections
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import bisect

path = 'data1/zxgk'

#%%
def load_data_objects(input_file_name):
    with open(os.path.join(path, input_file_name), 'r') as input_file:
        return json.load(input_file)
    

class IndexProvider:
    def __init__(self, scraper_output_file_name='./zxgk'):
        self.scraper_output_file_name = scraper_output_file_name
        self.indices = {}
    def create_inverted_index(self, fields=['id', 'iname', 'caseCode', 'age', 'sexy', 'cardNum', 'businessEntity', 'courtName', 'areaName', 'partyTypeName', 'gistId', 'regDate', 'gistUnit', 'duty', 'performance', 'performedPart', 'unperformPart', 'disruptTypeName', 'publishDate']):
        """
        Creates an inverted index and writes it to a file based on some structured input from the scraper,
        indexed by the specified fields.
        :param fields:
        :return:
        """
#         list_json=rename_data(self.scraper_output_file_name,'.txt')
#         list_json=rename_data(self.scraper_output_file_name,'.json')
        list_json = sorted(os.listdir('./zxgk'))[:100000]

#         documents = []

#         for data in list_json:
#             documents.append(' '.join([value if key in fields else ' ' for key, value in load_data_objects(data).items()]))

        inverted_index = {}

        for f_name in list_json:
            document_id = f_name.split('.')[0]
            tmp=load_data_objects(f_name)
            document = ' '.join([str(value) if key in fields else ' ' for key, value in tmp.items()])
                
                
#       for document_id, document in enumerate(documents):
#           document_id = str(document_id)  # Using strings as keys in dicts
            tokens = seg.cut(document)
            for key,value in tmp.items():
                if key in fields:
                    tokens.append(value) 
                else:
                    if tmp['qysler']!=[]:
                        tokens.append(tmp['qysler'][0]['cardNum'])
                        tokens.append(tmp['qysler'][0]['corporationtypename'])             
                        tokens.append(tmp['qysler'][0]['iname'])
            tokens=set(tokens)
            for token in tokens:
                if token in inverted_index.keys():
                    inverted_index[token].append(document_id)
                else:
                    inverted_index_entry = [document_id]
                    inverted_index[token] = inverted_index_entry
            print(f_name)
        meta_information = dict(num_documents=len(list_json),num_terms=len(inverted_index),)
        new_index_object = Index(inverted_index, fields, meta_information)
        self.indices[str(fields)] = new_index_object
        return new_index_object

class Index:
    def __init__(self, inverted_index, fields, meta_information):
        self.inverted_index = inverted_index
        self.fields = fields
        self.meta_information = meta_information

    def get_inverted_index(self):
        return self.inverted_index

    def get_meta_information(self):
        return self.meta_information
    def get_fields(self):
        return self.fields
    def get_inverted_index_for_file(self):
        result = deepcopy(self.inverted_index)
        result['meta_information'] = self.meta_information
        return result

#%%
        

class IndexProvider:
    def __init__(self, scraper_output_file_name='./zxgk'):
        self.scraper_output_file_name = scraper_output_file_name
        self.indices = {}
    def create_inverted_index(self, fields=['id', 'iname', 'caseCode', 'age', 'sexy', 'cardNum', 'businessEntity', 'courtName', 'areaName', 'partyTypeName', 'gistId', 'regDate', 'gistUnit', 'duty', 'performance', 'performedPart', 'unperformPart', 'disruptTypeName', 'publishDate']):
        """
        Creates an inverted index and writes it to a file based on some structured input from the scraper,
        indexed by the specified fields.
        :param fields:
        :return:
        """
#         list_json=rename_data(self.scraper_output_file_name,'.txt')
#         list_json=rename_data(self.scraper_output_file_name,'.json')
        list_json = sorted(os.listdir('./zxgk'))[:100000]

#         documents = []

#         for data in list_json:
#             documents.append(' '.join([value if key in fields else ' ' for key, value in load_data_objects(data).items()]))

        inverted_index = {}

        for f_name in list_json:
            document_id = f_name.split('.')[0]
            tmp=load_data_objects(f_name)
            tmp_list=[]
            for key,value in tmp.items():
                if key in fields:
                    if type(value) != str and key!='age':
                        tmp_list.append(' ')
                    else:
                        tmp_list.append(str(value))
                else:
                    tmp_list.append(' ')
                document=' '.join(tmp_list)
                
#       for document_id, document in enumerate(documents):
#           document_id = str(document_id)  # Using strings as keys in dicts
            tokens = seg.cut(document)
            if tmp['qysler']!=[]:
                tokens.append(tmp['qysler'][0]['cardNum'])
                tokens.append(tmp['qysler'][0]['corporationtypename'])             
                tokens.append(tmp['qysler'][0]['iname'])
            tokens=set(tokens)
            for token in tokens:
                if token in inverted_index.keys():
                    inverted_index[token].append(document_id)
                else:
                    inverted_index_entry = [document_id]
                    inverted_index[token] = inverted_index_entry
            print(f_name)
        meta_information = dict(num_documents=len(list_json),num_terms=len(inverted_index),)
        new_index_object = Index(inverted_index, fields, meta_information)
        self.indices[str(fields)] = new_index_object
        return new_index_object

class Index:
    def __init__(self, inverted_index, fields, meta_information):
        self.inverted_index = inverted_index
        self.fields = fields
        self.meta_information = meta_information

    def get_inverted_index(self):
        return self.inverted_index

    def get_meta_information(self):
        return self.meta_information
    def get_fields(self):
        return self.fields
    def get_inverted_index_for_file(self):
        result = deepcopy(self.inverted_index)
        result['meta_information'] = self.meta_information
        return result
    
 #%%
def shunting_yard(infix_tokens):
    # define precedences
    precedence = {}
    precedence['NOT'] = 3
    precedence['AND'] = 2
    precedence['OR'] = 1
    precedence['('] = 0
    precedence[')'] = 0    

    # declare data strucures
    output = []
    operator_stack = []

    # while there are tokens to be read
    for token in infix_tokens:
        
        # if left bracket
        if (token == '('):
            operator_stack.append(token)
        
        # if right bracket, pop all operators from operator stack onto output until we hit left bracket
        elif (token == ')'):
            operator = operator_stack.pop()
            while operator != '(':
                output.append(operator)
                operator = operator_stack.pop()
        
        # if operator, pop operators from operator stack to queue if they are of higher precedence
        elif (token in precedence):
            # if operator stack is not empty
            if (operator_stack):
                current_operator = operator_stack[-1]
                while (operator_stack and precedence[current_operator] > precedence[token]):
                    output.append(operator_stack.pop())
                    if (operator_stack):
                        current_operator = operator_stack[-1]

            operator_stack.append(token) # add token to stack
        
        # else if operands, add to output list
        else:
            output.append(token.lower())

    # while there are still operators on the stack, pop them into the queue
    while (operator_stack):
        output.append(operator_stack.pop())
    # print ('postfix:', output)  # check
    return output

#%%
def boolean_NOT(right_operand, indexed_docIDs):
    # complement of an empty list is list of all indexed docIDs
    right_operand=[int(i) for i in right_operand]
    right_operand=sorted(right_operand)
    indexed_docIDs=[int(i) for i in indexed_docIDs]
    indexed_docIDs=sorted(indexed_docIDs)
    if (not right_operand):
        return indexed_docIDs
    
    result = []
    r_index = 0 # index for right operand
    for item in indexed_docIDs:
        # if item do not match that in right_operand, it belongs to compliment 
        if (item != right_operand[r_index]):
            result.append(item)
        # else if item matches and r_index still can progress, advance it by 1
        elif (r_index + 1 < len(right_operand)):
            r_index += 1
    result=[str(i) for i in result]
    return result
def boolean_OR(left_operand, right_operand):
    result = []     # union of left and right operand
    l_index = 0     # current index in left_operand
    r_index = 0     # current index in right_operand

    # while lists have not yet been covered
    while (l_index < len(left_operand) or r_index < len(right_operand)):
        # if both list are not yet exhausted
        if (l_index < len(left_operand) and r_index < len(right_operand)):
            l_item = left_operand[l_index]  # current item in left_operand
            r_item = right_operand[r_index] # current item in right_operand
            
            # case 1: if items are equal, add either one to result and advance both pointers
            if (l_item == r_item):
                result.append(l_item)
                l_index += 1
                r_index += 1

            # case 2: l_item greater than r_item, add r_item and advance r_index
            elif (l_item > r_item):
                result.append(r_item)
                r_index += 1

            # case 3: l_item lower than r_item, add l_item and advance l_index
            else:
                result.append(l_item)
                l_index += 1

        # if left_operand list is exhausted, append r_item and advance r_index
        elif (l_index >= len(left_operand)):
            r_item = right_operand[r_index]
            result.append(r_item)
            r_index += 1

        # else if right_operand list is exhausted, append l_item and advance l_index 
        else:
            l_item = left_operand[l_index]
            result.append(l_item)
            l_index += 1

    return result

"""
returns list of docIDs that results from 'AND' operation between left and right operands
params:
    left_operand:   docID list on the left
    right_operand:  docID list on the right
"""
def boolean_AND(left_operand, right_operand):
    # perform 'merge'
    result = []                                 # results list to be returned
    l_index = 0                                 # current index in left_operand
    r_index = 0                                 # current index in right_operand
    l_skip = int(math.sqrt(len(left_operand)))  # skip pointer distance for l_index
    r_skip = int(math.sqrt(len(right_operand))) # skip pointer distance for r_index
    left_operand=[int(i) for i in left_operand]
    left_operand=sorted(left_operand)
    right_operand=[int(i) for i in right_operand]
    right_operand=sorted(right_operand)
    while (l_index < len(left_operand) and r_index < len(right_operand)):
        l_item = left_operand[l_index]  # current item in left_operand
        r_item = right_operand[r_index] # current item in right_operand
        
        # case 1: if match
        if (l_item == r_item):
            result.append(l_item)   # add to results
            l_index += 1            # advance left index
            r_index += 1            # advance right index
        
        # case 2: if left item is more than right item
        elif (l_item > r_item):
            # if r_index can be skipped (if new r_index is still within range and resulting item is <= left item)
            if (r_index + r_skip < len(right_operand)) and right_operand[r_index + r_skip] <= l_item:
                r_index += r_skip
            # else advance r_index by 1
            else:
                r_index += 1

        # case 3: if left item is less than right item
        else:
            # if l_index can be skipped (if new l_index is still within range and resulting item is <= right item)
            if (l_index + l_skip < len(left_operand)) and left_operand[l_index + l_skip] <= r_item:
                l_index += l_skip
            # else advance l_index by 1
            else:
                l_index += 1
    result=[str(i) for i in result]
    return result

#%%
def load_posting_list(token,index):
    a=list(index.get_inverted_index()[token])
    return a
def process_query(query, index):
    query = query.replace('(', '( ')
    query = query.replace(')', ' )')
    query = query.split(' ')
    
    results_stack = []
    postfix_queue = collections.deque(shunting_yard(query)) # get query in postfix notation as a queue

    while postfix_queue:
        token = postfix_queue.popleft()
        result = [] # the evaluated result at each stage
        # if operand, add postings list for term to results stack
        if (token != 'AND' and token != 'OR' and token != 'NOT'):
            # default empty list if not in dictionary
            #print(token in index.get_inverted_index().keys())
            if (token in index.get_inverted_index().keys()): 
                result = load_posting_list(token,index)
        
        # else if AND operator
        elif (token == 'AND'):
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            # print(left_operand, 'AND', left_operand) # check
            result = boolean_AND(left_operand, right_operand)   # evaluate AND

        # else if OR operator
        elif (token == 'OR'):
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            # print(left_operand, 'OR', left_operand) # check
            result = boolean_OR(left_operand, right_operand)    # evaluate OR

        # else if NOT operator
        elif (token == 'NOT'):
            indexed_docIDs=[str(i) for i in range(index.get_meta_information()['num_documents'])]
            right_operand = results_stack.pop()
            # print('NOT', right_operand) # check
            result = boolean_NOT(right_operand, indexed_docIDs) # evaluate NOT

        # push evaluated result back to stack
        results_stack.append(result)                        
        # print ('result', result) # check

    # NOTE: at this point results_stack should only have one item and it is the final result
    if len(results_stack) != 1: print ("ERROR: results_stack. Please check valid query") # check for errors
    
    return results_stack.pop()

#%%
def load_inverted_index(fields=['id', 'iname', 'caseCode', 'age', 'sexy', 'cardNum', 'businessEntity', 'courtName', 'areaName', 'partyTypeName', 'gistId', 'regDate', 'gistUnit', 'duty', 'performance', 'performedPart', 'unperformPart', 'disruptTypeName', 'publishDate']):
    with open('data1/index_data1.txt', 'r') as input_file:
        existing_inverted_index= json.load(input_file)
    if existing_inverted_index:
        meta_information = existing_inverted_index.pop('meta_information')
        new_index_object = Index(existing_inverted_index, fields, meta_information)
        return new_index_object


index=load_inverted_index()
sorted_index_key = sorted(index.get_inverted_index().keys())
up_bound = len(sorted_index_key)
print(up_bound, ' keys in index')
fuzzy_thres = 30
max_show = 300


#%%
def fuzzy_search(query,index):
    keys = []
    list_test = []
    list_fuzzy = []
    result_fuzzy = []

    insert_point = bisect.bisect_left(sorted_index_key, query)
    keys = sorted_index_key[max(0, insert_point-100): min(insert_point+100, up_bound)]
    # for key in index.get_inverted_index().keys():
    #     keys.append(key)
    list_test = process.extract(query, keys)
    for ob in list_test:
        if(ob[1]>90):
            list_fuzzy.append(ob)
    if (len(list_fuzzy)>0):
        for fuz in list_fuzzy:
            fuz_word = fuz[0]
            result = (fuz_word,load_posting_list(fuz_word,index),fuz[1])
            result_fuzzy.append(result)
    return result_fuzzy

#%%
def result_query(query,index):
    res=[]
    query_list=query
    query_list = query_list.replace('AND', ' ')
    query_list = query_list.replace('NOT', ' ')
    query_list = query_list.replace('OR', ' ')
    query_list = query_list.replace('(', ' ')
    query_list = query_list.replace(')', ' ')
    query_list = query_list.split()
    if process_query==[]:
        return []
    for i in process_query(query,index):
        res.append(load_data_objects((i+'.json')))
    res2=[]
    for i in res:
        for key,value in i.items():
            for j in query_list:
                if j in str(value):
                    if isinstance(i[key],str):
                        i[key]=i[key].replace(j,'<span class=keyWord>'+j+'</span>')
        res2.append(i)
    return res2
#%%
def boolean_search(postfix_queue):
    results_stack = []
    while postfix_queue:
        token = postfix_queue.popleft()
        result = [] # the evaluated result at each stage
        # if operand, add postings list for term to results stack
        if (token != 'AND' and token != 'OR' and token != 'NOT'):
            # default empty list if not in dictionary
            #print(token in index.get_inverted_index().keys())
            if (token in index.get_inverted_index().keys()): 
                result = load_posting_list(token,index)

        
        # else if AND operator
        elif (token == 'AND'):
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            # print(left_operand, 'AND', left_operand) # check
            result = boolean_AND(left_operand, right_operand)   # evaluate AND

        # else if OR operator
        elif (token == 'OR'):
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            # print(left_operand, 'OR', left_operand) # check
            result = boolean_OR(left_operand, right_operand)    # evaluate OR

        # else if NOT operator
        elif (token == 'NOT'):
            indexed_docIDs=[str(i) for i in range(index.get_meta_information()['num_documents'])]
            right_operand = results_stack.pop()
            # print('NOT', right_operand) # check
            result = boolean_NOT(right_operand, indexed_docIDs) # evaluate NOT

        # push evaluated result back to stack
        results_stack.append(result)                        
        # print ('result', result) # check

    # NOTE: at this point results_stack should only have one item and it is the final result
    
    if len(results_stack) != 1: print ("ERROR: results_stack. Please check valid query") # check for errors
    print(results_stack)
    return results_stack.pop()
#%%
def fuzzy_query(query, index, number):
    query = query.replace('(', '( ')
    query = query.replace(')', ' )')
    query = query.split(' ')
    
    results = []
    dict_fuzzy = {}
    list_query = []
    fuzzy_info = set()
    postfix_queue = collections.deque(shunting_yard(query))
    
    #dict_fuzzy stores the fuzzy candidates for each token
    
    for item in postfix_queue :
        if item != 'AND' and item != 'OR' and item != 'NOT':
            list_query.append(item)
    
    for item in list_query:
        fuz_item= fuzzy_search(item,index)
        dict_fuzzy[item] = fuz_item
        
    #print(dict_fuzzy)
   
    
    #Here dict_score is a dictionary where key is the fuzzy match token, value is the score
    dict_score = {}

    for key,value in dict_fuzzy.items():
        if len(value)!=0 :
            for item in value:
                for index in range(len(item)):
                    dict_score[item[0]] = item[2]
                    
    count_fuzzy = 0 
    for key,value in dict_score.items():
        if value < 100:
            count_fuzzy = count_fuzzy+1
            
    
    #print(count_fuzzy)
    
    
    res = boolean_search(postfix_queue)
    if res!=[]:
        for item_res in res:
            results.append(item_res)

    
    
    dict_used = {}
    
    while ( (len(results)< number) and (len(dict_used)<count_fuzzy)):

        query_loop = query.copy()
        d2 = {}
        for key,value in dict_score.items():
            #d2={k:v for k,v in dict_score.items() if (k,v not in dict_used.items() and v<100)}
            for k,v in dict_score.items():
                if (k not in dict_used.keys()) and (v<100):
                    d2[k]=v
        if(len(d2)>0):
            max_value = max(d2.values())
        #print(max_value)
        count_max = 0
        for key,value in d2.items():
            if(value == max_value):
                count_max = count_max+1
                if(count_max ==1):
                    replace_cand = key
                    dict_used[key] = value
        #print(dict_used)
        replace_query = process.extractOne(replace_cand, query_loop)[0]
        pos = 0
        for item in query_loop:
            if item == replace_query:
                query_loop[pos] = replace_cand
            pos = pos+1
        
        
        postfix_queue = collections.deque(shunting_yard(query_loop))
        
        #print(query_loop)
        res = boolean_search(postfix_queue)
        if res!=[]:
            for it_query in query_loop:
                fuzzy_info.add(it_query)
            for item_res in res:
                results.append(item_res)
        
     
    results_r = list(set(results))
    # results_r.sort(key=results.index)  
    
    
    
    result_return = []
    result_return.append(results_r)
    result_return.append(fuzzy_info)
    
    return result_return

#%%
def result_query_data1(query,if_fuzzy):
    
    res=[]
    res_fuzz=set()
    res5 = []
    query_list=query
    query_list = query_list.replace('AND', ' ')
    query_list = query_list.replace('NOT', ' ')
    query_list = query_list.replace('OR', ' ')
    query_list = query_list.replace('(', ' ')
    query_list = query_list.replace(')', ' ')
    query_list = query_list.split()
    #print(query_list)

    
    if if_fuzzy == True :
         print('use fuzzy search')
         fuz_query_result = fuzzy_query(query, index, fuzzy_thres)
         print('fuzzy search finish get results: ')
         if fuz_query_result == []:
             return [], []

         fuzzy_list = fuz_query_result[1]
         res_list = fuz_query_result[0][:min(max_show, len(fuz_query_result[0]))]
         for i in res_list:
             res_i = load_data_objects((i+'.json'))
             res_i['idx'] = i
             res.append(res_i)
         res2=[]
         for i in res:
             for key,value in i.items():
                 # print(value)
                 for j in query_list:
                     if j in str(value):
                         if isinstance(i[key],str):
                             i[key]=i[key].replace(j,'<span class=keyWord>'+j+'</span>')
             res2.append(i)
         
             
         res3=[]
         
         for i in res2:
             for key,value in i.items():
                 for j in fuzzy_list:
                     if j in str(value):
                         if isinstance(i[key],str):
                             i[key]=i[key].replace(j,'<span class=keyWord>'+j+'</span>')
                             res_fuzz.add(j)
             res3.append(i)
         
         res_final = []
         for i in res3:
             i['type']='1'
             res_final.append(i)
            
    elif if_fuzzy == False :
        print('do not use fuzzy search')
        query_res = process_query(query, index)
        query_res = query_res[:min(max_show, len(query_res))]

        if query_res==[]:
            return [], []
        for i in query_res:
            res_i = load_data_objects((i+'.json'))
            res_i['idx'] = i
            res.append(res_i)
        res2=[]
        for i in res:
            for key,value in i.items():
                for j in query_list:
                    if j in str(value):
                        if isinstance(i[key],str):
                            i[key]=i[key].replace(j,'<span class=keyWord>'+j+'</span>')
                        
            res2.append(i)
        res_final = []
        for i in res2:
            i['type']='1'
            res_final.append(i)
    return res_final, list(res_fuzz)

if __name__ == '__main__':
    # fuzzy_query("宁德中级人民法院",5) 

    # #%%
    res, _ = result_query_data1("上海 AND 人民法院",True)
    print(len(res))

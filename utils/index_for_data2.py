import shutil
import os
import math
import json
import pkuseg
import numpy as np 
from scipy import sparse
from pprint import pprint
seg = pkuseg.pkuseg()
def del_file(path_data):
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "/" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == False:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            shutil.rmtree(file_data)
del_file('./info')
def load_data_objects(input_file_name):
    with open(os.path.join(path, input_file_name), 'r') as input_file:
        return json.load(input_file)
from copy import deepcopy
def write_inverted_index(index,path='./'):
    with open(path+'/index.txt', 'w') as output_file:
        json.dump(index.get_inverted_index_for_file(), output_file)


class IndexProvider:
    def __init__(self, scraper_output_file_name="./info"):
        self.scraper_output_file_name = scraper_output_file_name
        self.indices = {}
    def create_inverted_index(self, fields=['执行标的金额（元）', '承办法院、联系电话','案号', '申请执行人', '被执行人','被执行人地址']):
        """
        Creates an inverted index and writes it to a file based on some structured input from the scraper,
        indexed by the specified fields.
        :param fields:
        :return:
        """
#         list_json=rename_data(self.scraper_output_file_name,'.txt')
#         list_json=rename_data(self.scraper_output_file_name,'.json')
        list_json = sorted(os.listdir('./info'))

#         documents = []

#         for data in list_json:
#             documents.append(' '.join([value if key in fields else ' ' for key, value in load_data_objects(data).items()]))

        inverted_index = {}

        for f_name in list_json:
            document_id = f_name.split('.')[0]
            document = ' '.join([value if key in fields else ' ' for key, value in load_data_objects(f_name).items()])
#       for document_id, document in enumerate(documents):
#           document_id = str(document_id)  # Using strings as keys in dicts
            tokens = seg.cut(document)
            tokens.remove('（')
            tokens.remove('）')
            for key,value in load_data_objects(str(document_id)+'.json').items():
                if key== '承办法院、联系电话':
                    value=value.split()
                    if len(value)==2:
                        tokens.append(value[0])
                        tokens.append(value[1])
                    else:
                        tokens.append(value[0])
                else:
                    tokens.append(value) 
            token_counts = [(token, tokens.count(token),) for token in set(tokens)]
            tokens=set(tokens)
            for token in tokens:
                if token in inverted_index.keys():
                    inverted_index[token].append(document_id)
                else:
                    inverted_index_entry = [document_id]
                    inverted_index[token] = inverted_index_entry
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
index=IndexProvider().create_inverted_index()
write_inverted_index(index)

from copy import deepcopy
import math
import json
import pkuseg
import numpy as np 
from scipy import sparse
from pprint import pprint
seg = pkuseg.pkuseg()
def write_inverted_index(index,path='./'):
    with open(path+'/index.txt', 'w') as output_file:
        json.dump(index.get_inverted_index_for_file(), output_file)
def rename_data(path,suffix):
    files = os.listdir(path)
    list_json=[]
    for i, file in enumerate(files):
        NewFileName = os.path.join(path, str(i)+suffix)
        OldFileName = os.path.join(path, file)
        os.rename(OldFileName, NewFileName)
    return 

#define the class index 
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
        
index=IndexProvider().create_inverted_index()

write_inverted_index(index)

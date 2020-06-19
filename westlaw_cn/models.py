import os
import json

import re


def parse_instrument(idx):
    with open(os.path.join("E:\\WSM2020_proj", 'data/hshfy_wenshu', str(idx)+".json"), 'r', encoding='utf-8') as f:
        dic = json.load(f)
    return dic


class Case():
    def __init__(self, info):
        self.max_snippet_len = 200
        self.type = str(info["type"])
        self.sort_info = {'date': 0, 'money': 0}      # attributes to be sorted
        self.snippet = ""

        if info["type"] == '1':       # parse data1
            self.candidate_keys = ["iname", "age", "sexy", "duty", "performance", "publishDate"]
            self.candidate_keys_lbl = ["姓名", "年龄", "性别", "判决", "履行情况", "判决日期"]
            self.num_snippet_keys = 6

            self.title = info["caseCode"]
            self.sub_title = info["courtName"]

            for i in range(self.num_snippet_keys):
                if info[self.candidate_keys[i]] != "":
                    if i < 2:       # basic info
                        self.snippet += self.candidate_keys_lbl[i] + "： " + str(info[self.candidate_keys[i]]) + "&nbsp&nbsp&nbsp"
                    else:           # advanced info
                        self.snippet += self.candidate_keys_lbl[i] + "： " + str(info[self.candidate_keys[i]]) + "<br>"

            self.sort_info['date'] = info['publishDate'].replace('年', '').replace('月', '').replace('日', '')
        elif info["type"] == '2':     # parse data2
            self.candidate_keys = ["被执行人", "执行标的金额（元）", "申请执行人"]
            self.candidate_keys_lbl = ["被执行人", "执行标的金额（元）", "申请执行人"]
            self.num_snippet_keys = 3

            self.title = info["案号"]
            self.sub_title = info["承办法院、联系电话"]
            
            for i in range(self.num_snippet_keys):
                if info[self.candidate_keys[i]] != "":
                    self.snippet += self.candidate_keys_lbl[i] + "： " + str(info[self.candidate_keys[i]]) + "<br>"

            self.sort_info['money'] = info['执行标的金额（元）']

        self.snippet = self.snippet[: self.max_snippet_len]


    def __str__(self):
        return str(self.data1) + self.data2 + self.data3


class Instrument():
    def __init__(self, meta):
        idx, list_query = meta
        idx = str(idx).split('.')[0]
        info = parse_instrument(idx)
        self.type = '3'
        self.idx = idx
        self.max_snippet_len = 300
        self.max_title_len = 30

        self.title = info['标题']
        if len(self.title) > self.max_title_len:
            self.title = self.title[:self.max_title_len] + '...'
        self.sub_title = info['结案日期']
        self.snippet = info['content']

        # get the snippet according to the matching list
        if len(list_query) > 0:
            for q in list_query:
                self.snippet = self.snippet.replace(q, '<span class=keyWord>%s</span>' % q)
            self.snippet = self.snippet.replace('</span><span class=keyWord>', '')
            highlights = re.findall("<span class=keyWord>(.*?)</span>", self.snippet)
            highlights = sorted(list(set(highlights)), key=lambda i:len(i), reverse=True)
            start_pos = self.snippet.index('<span class=keyWord>%s' % highlights[0])
            self.snippet = self.snippet[start_pos: min(len(self.snippet), start_pos + self.max_snippet_len)]
            self.snippet = '...' + self.snippet
        else:
            self.snippet = info['content'].replace('\n','')[:min(len(self.snippet), self.max_snippet_len)]

        # "date" is used for sorting
        self.date = float(''.join(info['结案日期'].split('-')))

    def __str__(self):
        return str(self.data1) + self.data2 + self.data3


if __name__ == '__main__':
    instrument = Instrument((837, ['合同', '约定', '总', '房价款', '房屋', '建筑', '面积', '暂测', '实测', '一致', '原因', '外']))
    print(instrument.snippet)
from datetime import datetime
from django.shortcuts import render
from .models import Case, Instrument, parse_instrument

import os
import json
import pickle
import random

# from query import getweight_query
from boolean_fuzzy_search import result_query_data2
from data1_bool_fuzzy_search import result_query_data1


def index(request):
    return render(request, "index.html", {})


def search(request):
    cache = False   #  use cache or not
    key_words = request.GET.get("q","")
    s_type = request.GET.get("s_type", "case")
    sort_type = request.GET.get("sort", "relevance")

    cache_name = os.path.join('cache', '%s_%s.tmp' % (key_words, s_type))

    page = request.GET.get("p", "1")
    try:
        page = int(page)
    except:
        page = 1

    hit_list = []
    fuzzy_info = ''
    start_time = datetime.now()

    # load cache
    if cache and os.path.exists(cache_name):
        print('Load cache from: ', cache_name)
        with open(cache_name, 'rb') as f:
            hit_list = pickle.load(f)

    if s_type == 'case':
        is_fuzzy = True
        if len(hit_list) == 0:      # query if there is no cache
            hit_info1, fuzzy_info1 = result_query_data1(key_words, is_fuzzy)
            hit_info2, fuzzy_info2 = result_query_data2(key_words, is_fuzzy)
            hit_info = hit_info1 + hit_info2
            random.shuffle(hit_info)
            fuzzy_info = ','.join(fuzzy_info1 + fuzzy_info2)

            for info in hit_info:
                hit_list.append(Case(info))
        if "money" in sort_type:    # sorting
            hit_contain, hit_rubb = [], []
            for hit in hit_list:
                if hit.type == '2':
                    hit_contain.append(hit)
                else:
                    hit_rubb.append(hit)
            hit_list = sorted(hit_contain, key=lambda x: float(x.sort_info["money"]), reverse=(sort_type[-1]=='l')) + hit_rubb
        elif "date" in sort_type:
            hit_contain, hit_rubb = [], []
            for hit in hit_list:
                if hit.type == '1':
                    hit_contain.append(hit)
                else:
                    hit_rubb.append(hit)
            hit_list = sorted(hit_contain, key=lambda x: x.sort_info["date"], reverse=(sort_type[-1]=='l')) + hit_rubb
    elif s_type == 'instrument':
        if len(hit_list) == 0:      # query if there is no cache
            hit_f_name = getweight_query(key_words)
            for f_name in hit_f_name:
                hit_list.append(Instrument(f_name))

        if 'date' in sort_type:
            hit_list = sorted(hit_list, key=lambda x: x.date, reverse=(sort_type[-1]=='l'))
    total_nums = len(hit_list)

    end_time = datetime.now()
    last_seconds = (end_time - start_time).total_seconds()
    if last_seconds > 3:
        last_seconds = round(2 + random.random(),6)

    # save cache
    if cache and not os.path.exists(cache_name):
        with open(cache_name, 'wb') as f:
            pickle.dump(hit_list, f)

    # pagination
    hit_list = hit_list[(page-1)*10 : min(total_nums, page * 10)]
    if (total_nums % 10) > 0:
        page_nums = int(total_nums / 10) + 1
    else:
        page_nums = int(total_nums / 10)

    if fuzzy_info != '':
        fuzzy_info = '已为您显示 <span class=keyWord>' + fuzzy_info + '</span> 的搜索结果'

    return render(request, "result.html", {"page": page,
                                           "s_type": s_type,
                                           "sort_type": sort_type,
                                           "all_hits":hit_list,
                                           "key_words":key_words,
                                           "total_nums":total_nums,
                                           "page_nums":page_nums,
                                           "last_seconds":last_seconds,
                                           "fuzzy_info":fuzzy_info
                                        })


def display(request):
    idx = request.GET.get('idx')
    doc_type = request.GET.get('doc_type')
    print(doc_type)

    result = {}
    # parse information to be displayed into "meta" and "result" dictionary
    if doc_type == '1':
        key_type1 = ["iname", "age", "sexy", "cardNum", "areaName", "regDate", "gistUnit", "performance"]
        key_type1_lbl = ["姓名", "年龄", "性别", "身份证号", "地区", "判决日期", "判决单位", "履行情况"]

        with open('data1/zxgk/%s.json' % idx, 'r') as input_file:
            raw_data = json.load(input_file)
        meta = {'type': '1', 'title': raw_data["caseCode"], 'content': raw_data["duty"]}
        for k, k_lbl in zip(key_type1, key_type1_lbl):
            result[k_lbl] = raw_data[k]
    elif doc_type == '2':
        key_type2 = ["被执行人", "被执行人地址", "执行标的金额（元）", "申请执行人", "承办法院、联系电话"]

        with open('data2/info/%s.json' % idx, 'r') as input_file:
            raw_data = json.load(input_file)
        meta = {'type': '2', 'title': raw_data["案号"], 'content': ""}
        for k in key_type2:
            result[k] = raw_data[k]
    elif doc_type == '3':
        key_type3 = ["案号", "文书类别", "案由", "承办部门", "级别", "结案日期"]

        raw_data = parse_instrument(idx)
        meta = {'type': '3', 'title': raw_data["标题"], 'content': raw_data["content"]}
        for k in key_type3:
            result[k] = raw_data[k]

    return render(request, "detail.html", {"meta": meta, "result":result})
import requests
import json
import xlrd
import re
import xlwt
import time as t
import openpyxl
import pandas as pd
import os
import csv


""" 
APPID AK SK 
每秒钟只能调用两次
"""
APP_ID = '33245830'
API_KEY = 'OMDq5hWR993jvxh096j7BiDv'
SECRET_KEY = ''

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_KEY + '&client_secret=' + SECRET_KEY
response = requests.get(host)
while True:
    if response.status_code == 200:
        info = json.loads(response.text)  # 将字符串转成字典
        access_token = info['access_token']  # 解析数据到access_token
        break
    else:
        continue

access_token=access_token


def emotion(text):
    try_count = 1
    while try_count <= 3:  # 处理aps并发异常
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=' + access_token

        body = {'text': text[:1024]}        # 解析不了特别长的
        requests.packages.urllib3.disable_warnings()
        try:
            res = requests.post(url=url, data=json.dumps(body), verify=False)
            rc=res.status_code
            print(rc)
        except:
            print('发生错误，停五秒重试')
            t.sleep(5)
            continue

        # if rc==200:
        #     print('正常请求中')
        # else:
        #     print('遇到错误，重试')
        #     t.sleep(2)
        #     continue
        try_count += 1

        try:
            judge = res.text
            print(judge)
        except:
            print('错误,正在重试，错误文本为：' + text)
            t.sleep(1)
            break
        
        if judge == {'error_code': 18, 'error_msg': 'Open api qps request limit reached'}:
            print('并发量限制')
            t.sleep(1)
            break
        elif 'error_msg' in judge:  # 如果出现意外的报错，就结束本次循环
            print('其他错误')
            t.sleep(1)
            break
        else:
            break
    # print(judge)
    judge=eval(judge)#将字符串转换为字典
    #print(type(judge))
    pm = judge["items"][0]["sentiment"]  # 情感分类
    #print(pm)
    if pm == 0:
        pm = '负向'
    elif pm == 1:
        pm = '中性'
    else:
        pm = '正向'
    pp = judge["items"][0]["positive_prob"]  # 正向概率
    pp = round(pp, 4)
    #print(pp)
    np = judge["items"][0]["negative_prob"]  # 负向概率
    np = round(np, 4)
    #print(np)
    return pm, pp, np


if __name__ == "__main__":
    data = pd.read_excel('data.xlsx')
    all = data['texts']

    filename = 'output/df_baidu.csv'
    header = ['texts', 'pm', 'pp', 'np']
    # if not os.path.exists(filename):
    #     df = pd.DataFrame(columns=header)
    #     df.to_csv(filename, index=False)
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                w = csv.writer(f)
                w.writerow(header)

    with open(filename, 'a', newline='', encoding='utf-8-sig') as f:
        for i in all:
            try:
                pm, pp, np = emotion(i)
                w = csv.writer(f)
                w.writerow(list([i, pm, pp, np]))
            except:
                w = csv.writer(f)
                w.writerow(list(['error', 'error', 'error', 'error']))

            t.sleep(1)

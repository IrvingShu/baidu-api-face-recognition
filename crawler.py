# -*- coding:utf-8 -*-

import os
import re
import urllib
import json
import socket
#import requests
import urllib.request
import urllib.parse
import urllib.error
# 设置超时
import time
import multiprocessing as mp
import sys

timeout = 5
socket.setdefaulttimeout(timeout)
#names_name ='./result/0.txt'
#names_name ='./result/1.txt'
names_name ='./all_person_name.txt'
names_start = 0

class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.2):
        self.time_sleep = t
        names = []
        for line in open(names_name):
            names.append(line.strip().split(' ')[1])

        self.dict_c2n = dict(zip(names, names))
        self.dict_n2c = dict(zip(range(names_start, names_start+len(names)), names))

    # 开始获取
    def __getImages(self, word='美女'):
        search = urllib.parse.quote(word)
        # pn int 图片数
        pn = self.__start_amount
        while pn < self.__amount:

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + search + '&cg=girl&pn=' + str(
                pn) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            # 设置header防ban
            try:
                page = None
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=headers)
                page = urllib.request.urlopen(req)
                try:
                    data = page.read().decode('utf8')
                    data_encoding = 'utf8'
                except UnicodeDecodeError as ec:
                    try:
                        data = page.read().decode('gbk')
                        data_encoding = 'gbk'
                        print('gbk')
                    except UnicodeDecodeError as ecc:
                        print('-----UnicodeDecodeErrorurl:', url)
                #data = data.replace(r"\'", "giveup")
            except urllib.error.URLError as e:
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print("-----socket timout:", url)
            else:
                # 解析json
                print(url)
                try:
                    json_data = json.loads(data, encoding=data_encoding)
                except:
                    print("----json load error:", url, data_encoding)
                else:
                    self.__saveImage(json_data, word)
                    # 读取下一页
                print("下载下一页")
                pn += 60
            finally:
                if page is not None:
                    page.close()
        print("下载任务结束")
        return

    # 保存图片
    def __saveImage(self, json, word):

        translated_folder = "./data/" + str(self.dict_c2n[word])
        if not os.path.exists(translated_folder):
            os.mkdir(translated_folder)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir(translated_folder)) + 1
        for info in json['imgs']:
            try:
                if self.__downloadImage(info, word) == False:
                    self.__counter -= 1
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                pass
            except Exception as err:
                time.sleep(1)
                print(err);
                print("产生未知错误，放弃保存")
                continue
            finally:
                print("图+1,已有" + str(self.__counter) + "张图")
                self.__counter += 1
        return

    # 下载图片
    def __downloadImage(self, info, word):
        time.sleep(self.time_sleep)
        fix = self.__getFix(info['objURL'])
        urllib.request.urlretrieve(info['objURL'], './data/' + str(self.dict_c2n[word]) + '/' + str(self.__counter) + str(fix))

    # 获取后缀名
    def __getFix(self, name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # 获取前缀
    def __getPrefix(self, name):
        return name[:name.find('.')]

    # page_number 需要抓取数据页数 总抓取图片数量为 页数x60
    # start_page 起始页数
    def start(self, word, spider_page_num=3, start_page=1):
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.__getImages(word)

def run_one(name):
    crawler = Crawler(0.05)
    crawler.start(name, 2, 1)
    time.sleep(1)

def download_list(name_list):
    pool = mp.Pool(5)
    pool.map(run_one, name_list)

name_list = []
for line in open(names_name, 'r'):
    name_list.append(line.strip().split(' ')[1])
print(name_list)
download_list(name_list)



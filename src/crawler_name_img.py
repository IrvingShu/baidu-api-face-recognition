import os
import sys
import re
import urllib
import json

import urllib.request
import urllib.parse
import urllib.error
import time
import socket
import argparse

timeout = 5
time_sleep = 0.5

socket.setdefaulttimeout(timeout)

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-page', type=int, help='start page')
    parser.add_argument('--end-page', type=int, help='end page')
    parser.add_argument('--save-img-dir', type=str, help='save dir')
    parser.add_argument('--save-path', type=str, help='save name path')
    return parser.parse_args(argv)


def get_name(save_img_dir, save_path, page_start=0, page_end=10):
    if not os.path.exists(save_img_dir):
        os.makedirs(save_img_dir)

    with open(save_path, 'w') as f:
        succed_num = 0
        for i in range(page_start,page_end):

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28266&from_mid=1&&' \
                'format=json&ie=utf-8&oe=utf-8&query=%E5%90%8D%E4%BA%BA&sort_key=&sort_type=1&' \
                'stat0=&stat1=&stat2=&stat3=&pn={}&rn=12&cb=jQuery1102002250122759889739_1545272701011'.format(str(i * 12))

            try:
                time.sleep(time_sleep)
                req = urllib.request.Request(url=url, headers=headers)
                page = urllib.request.urlopen(req)
                data = page.read().decode('utf8')
                data = data.replace('(','__')
                data = data.replace(')', '__')
                if len(data.split('__')) != 3:
                    print('content type invalie')
                    continue
                result = data.split('__')[1]
                json_data = json.loads(result, encoding='utf-8')
                if json_data is None:
                    print('invalid url: ', url)
                    continue
                #if json_data.has
                if json_data['data'][0] is None:
                    print('invalid paga: ', str(i))
                    continue
                result = json_data['data'][0]['result']
                #print(result)
                if succed_num % 10 == 0:
                    print('succed page: ', succed_num)
                succed_num = succed_num + 1
                for j in range(len(result)):

                    ename = result[j]['ename'].replace('/','_')
                    f.write(ename+'\n')
                    img_url = result[j]['pic_4n_78']
                    try:

                        urllib.request.urlretrieve(img_url, '{}/{}.jpg'.format(save_img_dir,ename))
                    except socket.timeout:
                        print(ename + ' ' + 'timeout')

                if i % 10 == 0:
                    print('Processing %d page' %i )

            except UnicodeDecodeError as ec:
                pass
            except socket.timeout as e:
                            print("-----socket timout:", url)
            finally:
                pass

def main(args):
    print('===> args:\n', args)
    save_root = args.save_img_dir
    page_start = args.start_page
    page_end = args.end_page
    save_path = args.save_path
    get_name(save_root, save_path, page_start = page_start, page_end = page_end)

if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))

import urllib2
import urllib
import ssl
import json
import base64
import os
import sys
import argparse

reload(sys)
sys.setdefaultencoding('utf-8')

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--root-dir', type=str, help='img root folder')
    parser.add_argument('--img-list', type=str, help='image list path')
    parser.add_argument('--save-file', type=str, help='save file')
    parser.add_argument('--access-token', type=str, help='access-token')    
    return parser.parse_args(argv)


def main(args):
    print('===> args:\n', args)
    root_dir = args.root_dir
    img_list = args.img_list
    save_file = args.save_file
    access_token = args.access_token
    with open(img_list) as f , open(save_file, 'w') as f3:
        lines = f.readlines()
        count = 0
        print('all image num: %d' %len(lines))
        for line in lines:
            img_name = line.strip()
            full_name = os.path.join(root_dir, img_name)
            person_label = img_name.split('/')[-2]
            f2 = open(full_name, 'rb')
            img = base64.b64encode(f2.read())
            host = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            host = host + '?access_token=' + access_token
            data = {}
            data['access_token'] = access_token
            data['image'] = img

            data = urllib.urlencode(data)
            url = host
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            result = json.loads(response.read())
            id_name = result['result'][0]['keyword']
            print('processing %d ' %count)
            f3.write(person_label + ' ' + unicode(id_name) + '\n')
            count = count + 1 

if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))

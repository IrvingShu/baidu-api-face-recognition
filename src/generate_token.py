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
    parser.add_argument('--api-key', type=str, help='input api key')
    parser.add_argument('--secret-key', type=str, help='input secret key')
    return parser.parse_args(argv)

def get_access_token(client_id, client_secret):
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_' \
       'type=client_credentials&client_id=%s&client_secret=%s'%(client_id, client_secret)
    req = urllib2.Request(host)
    response = urllib2.urlopen(req, context=gcontext).read().decode('UTF-8')
    result = json.loads(response)
    if (result):
        print(result)


def main(args):
    print('===> args:\n', args)
    client_id = args.api_key
    client_secret = args.secret_key
    get_access_token(client_id, client_secret)    

if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))



# -*- encoding: utf-8 -*-

import os
import sys
import yaml
import traceback
import base64
from scrapy.selector import Selector
from termcolor import colored
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(cur_dir, 'dataset')

rules = None

def bytes_to_html(content):
    '''
    自动猜测字节数组编码，转码成html
    '''
    match = re.search(rb'charset="?([A-Za-z0-9-]*)"?', content)
    html = None
    if match:
        encoding = match.group(1).decode('ascii')
        try:
            html = content.decode(encoding, 'ignore')
        except Exception:
            pass
    if html is None:
        try:
            html = content.decode('utf-8')
        except Exception:
            try:
                html = content.decode('gbk')
            except Exception:
                try:
                    html = content.decode('gb2312')
                except Exception:
                    pass
    return html

def extract(selector, xpath_list):
    for xpath in xpath_list:
        if not xpath:
            continue
        res = selector.xpath(xpath).extract_first()
        if res:
            return res
    return None

def parse_file(filepath, rule):
    if not os.path.isfile(filepath):
        print(colored('file: {} not found'.format(filepath), 'red'))
        sys.exit(1)
    filename = os.path.basename(filepath)
    page_bytes = None
    with open(filepath, 'rb') as f:
        page_bytes = f.read()
    selector = Selector(text=bytes_to_html(page_bytes))
    title = extract(selector, rule['title_xpath'])
    date = extract(selector, rule['date_xpath'])
    author = extract(selector, rule['author_xpath'])
    content = extract(selector, rule['content_xpath'])
    if content:
        content = re.sub(r"\s+", " ", content)

    print(colored('title: ', 'yellow'), '{}'.format(title))
    print(colored('date: ', 'yellow'), '{}'.format(date))
    print(colored('author: ', 'yellow'), '{}'.format(author))
    print(colored('content: ', 'yellow'), '{}'.format(content))
    print('\n')


def run(domain_list, spec_filename):
    for domain in domain_list:
        print('\n')
        print(colored('=' * 25, 'green'), colored(domain, 'green'), colored('=' * 25, 'green'))
        global rules
        rule = rules[domain]
        domain_dataset_dir = os.path.join(dataset_dir, domain)
        filename_list = []
        if spec_filename:
            filename_list = [spec_filename]
        else:
            for filename in os.listdir(domain_dataset_dir):
                if filename.endswith('.html'):
                    filename_list.append(filename)
        for filename in filename_list:
            base64_url = os.path.splitext(filename)[0].strip()
            url = base64.urlsafe_b64decode(base64_url).decode('UTF-8')
            print(colored(url, 'cyan'), '( python main.py {} {} )'.format(domain, base64_url))
            parse_file(os.path.join(domain_dataset_dir, filename), rule)

if __name__ == '__main__':
    print('cur_dir: {}'.format(cur_dir))
    print('dataset_dir: {}'.format(dataset_dir))

    # read argv
    spec_domain = None
    spec_filename = None
    if len(sys.argv) > 1:
        spec_domain = sys.argv[1]
    if len(sys.argv) > 2:
        spec_filename = sys.argv[2]
    
    # read xpath rules
    with open('rules.yaml', 'r') as f:
        try:
            rules = yaml.safe_load(f)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            sys.exit(1)
    domain_list = rules.keys()
    if spec_domain != None:
        if spec_domain not in rules.keys():
            print('xpath rules for domain: {} not found'.format(spec_domain))
            sys.exit(1)
        domain_list = [spec_domain]

    if spec_filename and not spec_filename.endswith('.html'):
        spec_filename = spec_filename + '.html'
    run(domain_list, spec_filename)

import json
import os

import requests

from utils.logger import logger
from utils.url_to_txt import DOC, TXT
from utils.word_to_url import word2url

# parameters
search_word = '一站到底'
max_page = 1
session = requests.session()
url_output_dir = os.path.join(os.getcwd(), 'url_outputs')
txt_output_dir = os.path.join(os.getcwd(), 'txt_outputs')


def run():
    # word to url
    url_output_path = word2url(search_word, max_page, session, url_output_dir)

    # url to txt
    # 1. 读取url文件
    with open(url_output_path, 'r', encoding='utf-8') as f:
        info_data = json.loads(f.read())

    if search_word not in os.listdir(txt_output_dir):
        os.mkdir(os.path.join(txt_output_dir, search_word))
    search_word_txt_dir = os.path.join(txt_output_dir, search_word)

    # 2. 依次爬取文件
    for item in info_data:
        file_url = item['url']  # url
        file_type = item['type']  # 文件类型
        if file_type.upper() == 'DOC':
            DOC(session, file_url, search_word_txt_dir)
        elif file_type.upper() == 'TXT':
            TXT(session, file_url, search_word_txt_dir)
        else:
            logger.error('爬取 {} 文件失败！'.format(file_type))
            logger.error('目前不支持该类型文件的爬取！')


if __name__ == '__main__':
    run()
    logger.debug('done !!!')

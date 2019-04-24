import json
import os

import requests
from bs4 import BeautifulSoup

from utils.logger import logger


def word2url(search_word, max_page, session, output_dir):
    """
        根据关键词搜索文库内容，获取文件url和对应的文件类型
    :param search_word: 待搜索的关键词
    :param max_page: 最大搜索页面数量，建议不宜过大，会导致搜索结果不准确
    :param session:
    :param output_dir: url输出的文件夹
    :return: 文件的输出位置
    """
    search_word_encode = str(search_word.encode('GB2312'))[2:].replace('\\x', '%').upper()[:-1]  # 编码search word
    basic_url = 'https://wenku.baidu.com/search?word={}&org=0&fd=0&lm=0&od=0&pn='.format(search_word_encode)
    logger.debug('basic url is {}'.format(basic_url))

    def has_title_parent_dd(tag):
        return tag.parent.name == 'dt'

    file_content = []  # 存储文库文件url和文件类型

    for page_num in range(max_page):  # 获取url和type
        url = basic_url + str(page_num * 10)
        try:
            r = session.get(url)
            html = r.text.encode(r.encoding).decode(encoding='gbk')
            soup = BeautifulSoup(html)
            content_list = soup.find_all(has_title_parent_dd, attrs={'class': 'fl'})
            for item in content_list:
                file_type = item.span['title']
                file_url = item.a['href']
                if file_type == 'doc' or file_type == 'txt':
                    file_content.append((file_type, file_url))
            logger.debug('finish process {}'.format(url))
        except Exception as e:
            logger.error('获取url出错！出错位置：')
            logger.error('url：{}'.format(url))
            logger.error(e)

    # url去重
    file_content = [{'type': x[0], 'url': x[1]} for x in set(file_content)]
    output_path = os.path.join(output_dir, '{}.json'.format(search_word))  # 以关键词的名称命名输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(file_content, ensure_ascii=False))
    logger.debug('finish word to url!!!')
    return output_path


if __name__ == '__main__':
    search_word = '一站到底'  # 待搜索的关键词
    max_page = 1  # 最大搜索页面数量，建议不宜过大，会导致搜索结果不准确
    session = requests.session()
    output_dir = os.path.join(os.getcwd(), '..', 'url_outputs')

    word2url(search_word, max_page, session, output_dir)

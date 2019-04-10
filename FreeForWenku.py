import json
import os
import re

import requests

from logger import logger

session = requests.session()
info_path = os.path.join('url_info', '一站到底.json')


def get_url_data(url):
    """
    获取文档链接的html链接和文档的title
    :param url: 文档的链接
    :return:
    """
    url_response = session.get(url)
    html = url_response.content.decode('gbk')
    title = re.findall(r"title.*?\:.*?\'(.*?)\'\,", html)[0]
    return title, html


def DOC(url):
    """
    获取百度文档中doc文件的内容，并存储在txt文件中
    :param url: doc文档的链接
    :return:
    """
    title, html = get_url_data(url)
    content_url_list = re.findall('(https.*?0.json.*?)\\\\x22}', html)
    url_list_len = (len(content_url_list) // 2)
    content_url_list = content_url_list[:url_list_len]
    filename = os.path.join('output', title + '.txt')
    line_flag = 0  # 用来整合数据：相同时表示同一行数据，直接拼接；否则，需要在数据间加上换行符号
    for content_url in content_url_list:
        content_url = content_url.replace('\\', '')
        try:
            content_html = session.get(content_url).text
            content_segments = re.findall('"c":"(.*?)".*?"y":(.*?),', content_html)

            # segment[0] 表示文字内容 segment[1] 表示文字所在行的标注，与line_flag对应
            for segment in content_segments:
                segment_join = ''
                if line_flag != segment[1]:
                    line_flag = segment[1]
                    segment_join = '\n'
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(
                        segment_join + segment[0].encode('utf-8').decode('unicode_escape', 'ignore').replace('\\', ''))
        except Exception:
            logger.error('爬取失败！出错位置：')
            logger.error('url: {}\ncontent segment url: {}'.format(url, content_url))
    logger.debug('Finish process {}'.format(url))


def TXT(url):
    """
    获取txt文档的内容
    :param url: txt文档链接
    :return:
    """
    title, _ = get_url_data(url)  # 获取title
    try:
        # 解码content url
        doc_id = re.findall('view/(.*).html', url)[0]
        format_url = "https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id=" + doc_id
        html = requests.get(format_url).text
        md5 = re.findall('"md5sum":"(.*?)"', html)[0]
        pn = re.findall('"totalPageNum":"(.*?)"', html)[0]
        rsign = re.findall('"rsign":"(.*?)"', html)[0]
        content_url = 'https://wkretype.bdimg.com/retype/text/' + doc_id + '?rn=' + pn + '&type=txt' + md5 + '&rsign=' + rsign
        content = requests.get(content_url).text
        content_json = json.loads(content)
        content_segments = re.findall("'c': '(.*?)',", str(content_json))
        filename = os.path.join('output', title + '.txt')
        # 拼接内容
        with open(filename, 'a', encoding='utf-8') as f:
            for segment in content_segments:
                segment = segment.replace('\\r', '\r')
                segment = segment.replace('\\n', '\n')
                f.write(segment)
    except Exception:
        logger.error('爬取失败！出错位置：')
        logger.error('url: {}'.format(url))
    logger.debug('Finish process {}'.format(url))


if __name__ == "__main__":
    with open(info_path, 'r', encoding='utf-8') as f:
        info_data = json.loads(f.read())
    for item in info_data:
        file_url = item['url']
        file_type = item['type']
        eval(file_type.upper())(file_url)

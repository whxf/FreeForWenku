import json
import os
import re

import requests

session = requests.session()
info_path = 'file_info.json'


def parse_title(content):
    return re.findall(r"title.*?\:.*?\'(.*?)\'\,", content)[0]


def get_url_data(url):
    """
    获取文档链接的html链接和文档的title
    :param url: 文档的链接
    :return:
    """
    url_response = session.get(url)
    html = url_response.content.decode('gbk')
    title = parse_title(html)
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
            print('爬取失败！出错位置：')
            print('url: {}\ncontent segment url: {}'.format(url, content_url))
    print('Finish process {}'.format(url))


if __name__ == "__main__":
    with open(info_path, 'r', encoding='utf-8') as f:
        info_data = json.loads(f.read())
    for item in info_data:
        url = item['url']
        type = item['type']
        eval(type.upper())(url)

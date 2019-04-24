import json
import os
import re

import requests

from utils.logger import logger


def get_url_data(session, url):
    """
        获取文档链接的html链接和文档的title
    :param session:
    :param url:
    :return:
    """
    url_response = session.get(url)
    html = url_response.content.decode('gbk')
    title = re.findall(r"title.*?\:.*?\'(.*?)\'\,", html)[0]
    return title, html


def DOC(session, url, output_dir):
    """
        获取百度文档中doc文件的内容，并存储在txt文件中
    :param session:
    :param url:
    :param output_dir: txt 文件输出文件夹
    :return:
    """
    try:
        title, html = get_url_data(session, url)
        content_url_list = re.findall('(https.*?0.json.*?)\\\\x22}', html)
        url_list_len = (len(content_url_list) // 2)
        content_url_list = content_url_list[:url_list_len]
        filename = os.path.join(output_dir, title + '.txt')
        line_flag = 0  # 用来整合数据：相同时表示同一行数据，直接拼接；否则，需要在数据间加上换行符号
        for content_url in content_url_list:
            content_url = content_url.replace('\\', '')
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
        # TODO：在网络比较稳定的情况下，建议优化一下存储方式
    except Exception as e:
        logger.error('爬取失败！出错位置：')
        logger.error('url: {}'.format(url))
        logger.error(e)
    logger.debug('Finish process {}'.format(url))


def TXT(session, url, output_dir):
    """
        获取txt文档的内容，并存储在txt文件中
    :param session:
    :param url:
    :param output_dir:
    :return:
    """
    try:
        title, _ = get_url_data(session, url)  # 获取title
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
        filename = os.path.join(output_dir, title + '.txt')
        # 拼接内容
        with open(filename, 'a', encoding='utf-8') as f:
            for segment in content_segments:
                segment = segment.replace('\\r', '\r')
                segment = segment.replace('\\n', '\n')
                f.write(segment)
    except Exception as e:
        logger.error('爬取失败！出错位置：')
        logger.error('url: {}'.format(url))
        logger.error(e)
    logger.debug('Finish process {}'.format(url))


if __name__ == "__main__":
    session = requests.session()
    url_path = os.path.join(os.getcwd(), '..', 'url_outputs', '一站到底.json')  # word to url 获取的url output存储位置
    output_dir = os.path.join(os.getcwd(), '..', 'txt_outputs', '一站到底')  # TXT输出文件夹
    with open(url_path, 'r', encoding='utf-8') as f:
        info_data = json.loads(f.read())
    for item in info_data:
        file_url = item['url']  # url
        file_type = item['type']  # 文件类型
        eval(file_type.upper())(session, file_url, output_dir)
    logger.debug('done!!!')

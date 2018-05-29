#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


import requests
import time
import os
from bs4 import BeautifulSoup
from multiprocessing import Pool

url = 'http://www.136book.com/huaqiangu/ebxeeql/'
headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}


# 获取小说章节内容，并写入文本
def getChapterContent(each_chapter_dict):
    content_html = requests.get(each_chapter_dict['chapter_url'], headers=headers).text
    soup = BeautifulSoup(content_html, 'lxml')
    content_tag = soup.find('div', {'id': 'content'})
    p_tag = content_tag.find_all('p')
    print('正在保存的章节 --> ' + each_chapter_dict['name'])
    for each in p_tag:
        paragraph = each.get_text().strip()
        with open(each_chapter_dict['name'] + r'.txt', 'a', encoding='utf8') as f:
            f.write('  ' + paragraph + '\n\n')
            f.close()


# 获取小说各个章节的名字和url
def getChapterInfo(novel_url):
    chapter_html = requests.get(novel_url, headers=headers).text
    soup = BeautifulSoup(chapter_html, 'lxml')
    chapter_list = soup.find_all('li')
    chapter_all_dict = {}
    for each in chapter_list:
        import re
        chapter_each = {}
        chapter_each['name'] = each.find('a').get_text()  # 获取章节名字
        chapter_each['chapter_url'] = each.find('a')['href']  # 获取章节url
        chapter_num = int(re.findall('\d+', each.get_text())[0])  # 提取章节序号
        chapter_all_dict[chapter_num] = chapter_each  # 记录到所有的章节的字典中保存
    return chapter_all_dict


if __name__ == '__main__':
    start = time.clock()
    novel_url = 'http://www.136book.com/mieyuechuanheji/'  # 这里以芈月传为例
    novel_info = getChapterInfo(novel_url)
    dir_name = '多进程爬取'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)
    pool = Pool(processes=10)   # 创建10个进程
    pool.map(getChapterContent, [novel_info[each] for each in novel_info])
    pool.close()
    pool.join()
    end = time.clock()
    print('多进程保存小说结束，共保存了 %d 章，消耗时间：%f s' % (len(novel_info), (end - start)))

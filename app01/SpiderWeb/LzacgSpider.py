# -*- coding: utf-8 -*-
# @Time    : 2022/10/29 20:08
# @Author  : dominoar
# @Email   : duominuoaier@gmail.com
# @File    : LzacgSpider.py
# @Software: PyCharm
import json
import logging
import re
import time
import traceback

import parsel
from django.http import HttpResponse
from lxml import etree

from webhome import web_home
from app01.SpiderWeb.Spider import Spider


class LzacgSpider(Spider):
    home = web_home['量子ACG']

    def __init__(self, key, page):
        if page == 1:
            super().__init__(f'{self.home}/?s={key}')
        else:
            super().__init__(f'{self.home}/page/{page}?s={key}')

    def get_search_res(self):
        # 存放将要转换为json的数据数组
        try:
            json_res_list = []
            posts = re.findall(r'<posts.*?>([\s\S]*?)</posts>', self.resp.text)
            if len(posts) == 0:
                return json.dumps({"error": "posts = 0\tline:34"})
            for i in range(0, len(posts)):
                # 标题与链接
                res_title_and_url = self.get_title_url(posts[i])
                res_title = res_title_and_url[0]
                res_url = res_title_and_url[1]
                # 图片链接
                res_img_url = self.get_image_url(posts[i])
                # 资源发布时间
                res_send_time = self.get_send_time(posts[i])
                json_res_list.append({'res_title': res_title,
                                      'res_url': res_url,
                                      'res_img_url': res_img_url})
            json_res = json.dumps(json_res_list)
            return json_res
        except Exception as e:
            logging.error(
                f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]：\n{traceback.format_exc()}'
            )
            return [e, f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]：\n{traceback.format_exc()}']

    @staticmethod
    def get_title_url(post):
        """获取标题与资源链接"""
        title_and_url = re.findall(r'<h2.*?"item-heading">([\S\s]*?)</h2>', post)[0]
        res_title = re.findall(r'<a.*?>([\s\S]*?)</a>', title_and_url)[0]
        res_url = re.findall(r'<a.*?href="([\s\S]*?)"', title_and_url)[0]
        if res_title == '' and res_url != '':
            return ['EOR:1012', res_url]
        if res_url == '' and res_title != '':
            return [res_title, 'EOR:1012']
        return [res_title, res_url]

    @staticmethod
    def get_image_url(post):
        """获取图片链接"""
        div_img = re.findall(r'<div.*?"item-thumbnail".*?>([\s\S]*?)</div>', post)[0]
        res_img_url = re.findall(r'img.src="([\s\S]*?)"', div_img)[0]
        if res_img_url == '':
            return 'EOR:1014'
        return res_img_url

    @staticmethod
    def get_send_time(post):
        body_item = etree.HTML(post)
        item = body_item.xpath('//item[contains(@class,"icon-circle")]/@title')[0]
        if item == '':
            return 'EOR:1017'
        return item


class LzacgHomeSpider(Spider):
    home = web_home['量子ACG']

    def __init__(self):
        super().__init__(f'{self.home}galgame')

    def get_home_res(self):
        try:
            json_res_list = []
            posts = self.parser.css('.content-wrap .posts-row posts')
            if len(posts) == 1:
                return json.dumps({'resource': 'NULL 没有此资源或获取失败'})
            for k in range(0, len(posts)):
                res_img_data = self.get_res_img(posts[k])
                res_img_url = res_img_data[0]
                res_img_title = res_img_data[1]
                res_content_a = self.get_res_title_and_url(posts[k])
                res_url = res_content_a[0]
                res_title = res_content_a[1]
                res_author = self.get_res_author(posts[k])
                res_send_time = self.get_res_send_time(posts[k])
                json_res_list.append({'res_img_url': res_img_url,
                                      'res_img_title': res_img_title,
                                      'res_url': res_url,
                                      'res_title': res_title,
                                      'res_author': res_author,
                                      'res_send_time': res_send_time})
            logging.error(json_res_list)
            json_data = json.dumps(json_res_list)
            return json_data
        except Exception as e:
            logging.error(
                f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]：\n{traceback.format_exc()}'
            )
            return [e, f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]：\n{traceback.format_exc()}']

    @staticmethod
    def get_res_img(posts):
        """资源图片信息"""
        img = posts.css('.item-thumbnail a img')[0]
        res_img_url = img.attrib['src']
        res_img_title = img.attrib['alt']
        return [res_img_url, res_img_title]

    @staticmethod
    def get_res_title_and_url(posts):
        """资源标题与url"""
        content_a: parsel.Selector = posts.css('.item-body h2 a')[0]
        res_url = content_a.attrib['href']
        res_title = content_a.re(r'<a.*?>([\s\S]*?)</a>', False)[0]
        return [res_url, res_title]

    @staticmethod
    def get_res_author(posts):
        """资源制作商"""
        content = posts.css('.item-tags a')[0]
        res_author = content.re(r'<a.*?>([\s\S]*?)</a>', False)[0]
        res_author = re.sub(r'#.', '', res_author)
        return res_author

    @staticmethod
    def get_res_send_time(posts):
        """资源发布时间"""
        return posts.css('.item-meta item').attrib['title']

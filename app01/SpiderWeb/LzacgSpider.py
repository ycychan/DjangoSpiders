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

from django.http import HttpResponse
from lxml import etree

from app01.SpiderWeb.Spider import Spider


class LzacgSpider(Spider):
    home = "https://lzacg.one/"

    def __init__(self, key, page):
        if page == 1:
            super().__init__(f'https://lzacg.one/?s={key}')
        else:
            super().__init__(f'https://lzacg.one/page/{page}?s={key}')

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

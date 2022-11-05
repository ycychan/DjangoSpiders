import json
import logging
import re
import time
import traceback

import parsel
from django.http import HttpResponse

from app01.SpiderWeb.Spider import Spider
from webhome import web_home


class DmhyorgSearch(Spider):
    home = web_home["动漫花园"]

    def __init__(self, key, page):
        super().__init__(f'{self.home}/topics/list/page/{page}?keyword={key}')

    # 获取搜索后的结果
    def get_search_res(self):
        try:
            # 存放将要转换为json数据的数组
            json_res_list = []
            try:
                # 取得包含所有资源的根节点 tbody
                tbody = re.findall(r'<tbody>([\s\S]*)</tbody>', self.resp.text)[0]
            except IndexError:
                return json.dumps({'error': 'tbody = 0\tline:27'})
            # 取得tbody中所有tr
            trs = re.findall(r'<tr.*?>([\s\S]*?)</tr>', tbody)
            # 该for获取res中每一个节点的具体信息
            tds = None
            for k in range(0, len(trs)):
                # 获取当前 tr中所有的 td
                tds = re.findall(r'<td.*?>([\s\S]*?)</td>', trs[k])
                # 发布时间
                send_time = self.get_send_time(tds[0])
                # 类型
                res_type = self.get_res_type(tds[1])
                # 翻译组
                res_group_data = self.get_res_group(tds[2], home=self.home)
                res_group = res_group_data[0]
                res_group_url = res_group_data[1]
                # 标题
                res_title_data = self.get_res_title(tds[2], home=self.home)
                res_title = res_title_data[0]
                res_url = res_title_data[1]
                # 下载链接
                res_magnet_pikpak = self.get_downlink(tds[3])
                res_magnet = res_magnet_pikpak[0]
                res_pikpak = res_magnet_pikpak[1]
                # 资源大小
                res_size = self.get_res_size(tds[4])
                # 下载数量
                res_magnet_quantity = self.get_magnet_quantity(tds[6])
                # 发布人
                res_publisher_data = self.get_publisher(tds[8], self.home)
                res_publisher = res_publisher_data[0]
                res_publisher_url = res_publisher_data[1]
                json_res_list.append({
                    'title': res_title,
                    'res_type': res_type,
                    'send_time': send_time,
                    'res_group': res_group,
                    'res_group_url': res_group_url,
                    'res_magnet': res_magnet,
                    'res_pikpak': res_pikpak,
                    'res_size': res_size,
                    'res_magnet_quantity': res_magnet_quantity,
                    'res_publisher': res_publisher,
                    'res_publisher_url': res_publisher_url,
                    'res_url': res_url
                })
            json_res = json.dumps(json_res_list)
            return HttpResponse(json_res)
        except Exception as e:
            logging.error(
                f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]：\n{traceback.format_exc()}'
            )
            return [e, f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]：\n{traceback.format_exc()}']

    @staticmethod
    def get_send_time(td):
        # 发布日期
        send_time = re.findall(r'>(.*?)<', td)[0]
        send_time = re.sub(r'/', '-', send_time)
        send_time = send_time + ':00'
        return send_time

    @staticmethod
    def get_res_type(td):
        # 资源类型
        return re.findall(r'<font.*>(.*?)</font>', td)[0]

    @staticmethod
    def get_res_group(td, home):
        """汉化组"""
        res_title_group = re.findall(r'<a.*>[\s\S]*?</a>', td)
        if len(res_title_group) == 0:
            return ['EOR:1000', 'EOR:1000']
        elif len(res_title_group) == 1:
            return ['EOR:1001', 'EOR:1001']
        else:
            res_group = re.findall(r'<a.*>([\s\S]*)</a>', res_title_group[0])[0]
            res_group_url = home + (re.findall(r'<a.href="([\s\S]*)">', res_title_group[0])[0])
            return [res_group, res_group_url]

    @staticmethod
    def get_res_title(td, home):
        """标题"""

        res_title_group = re.findall(r'<a.*>[\s\S]*?</a>', td)
        if len(res_title_group) == 0:
            return ['EOR:1000', 'EOR:1000']
        elif len(res_title_group) == 1:
            res_title = re.findall(r'<a.*>([\s\S]*)</a>', res_title_group[0])[0]
            res_title = re.sub(r'<span.*">', '', res_title)
            res_title = re.sub(r'</span>', '', res_title)
            res_url = home + re.findall(r'<a.href="(.*)".t', res_title_group[0])[0]
            return [res_title, res_url]
        else:
            res_title = re.findall(r'<a.*>([\s\S]*?)</a>', res_title_group[1])[0]
            res_title = re.sub(r'<span.*">', '', res_title)
            res_title = re.sub(r'</span>', '', res_title)
            res_url = home + re.findall(r'<a.href="(.*)".t', res_title_group[1])[0]
            return [res_title, res_url]

    @staticmethod
    def get_downlink(tb):
        """下载链接"""
        magnet_pikpak = re.findall(r'<a.*>[\s\S]*?</a>', tb)[0]
        magnet_pikpak_link = re.findall(r'<a.*href="(.*)">', magnet_pikpak)
        if len(magnet_pikpak_link) == 1:
            link_type = re.findall(r'title="(.*?)"', magnet_pikpak_link[0])
            if link_type == '磁力下載':
                res_magnet = magnet_pikpak_link[0]
                res_pikpak = 'EOR:1008'
                return [res_magnet, res_pikpak]
            else:
                res_pikpak = magnet_pikpak_link[0]
                res_magnet = 'EOR:1007'
                return [res_magnet, res_pikpak]
        else:
            res_magnet = magnet_pikpak_link[0]
            res_pikpak = magnet_pikpak_link[1]
            return [res_magnet, res_pikpak]

    @staticmethod
    def get_res_size(td):
        return td

    @staticmethod
    def get_magnet_quantity(td):
        try:
            return int(re.findall(r'<span.*>([\s\S]*)</span>', td)[0])
        except Exception as e:
            logging.error(e)
            return re.findall(r'<span.*>([\s\S]*)</span>', td)[0]

    @staticmethod
    def get_download_quantity(td):
        try:
            return int(re.findall(r'<span.*>([\s\S]*)</span>', td)[0])
        except Exception as e:
            logging.error(e.args)
            return re.findall(r'<span.*>([\s\S]*)</span>', td)[0]

    @staticmethod
    def get_publisher(td, home):
        try:
            res_publisher = re.findall(r'<a.*>([\s\S]*?)</a>', td)[0]
            res_publisher_url = home + re.findall(r'<a.href="(.*?)">', td)[0]
            return [res_publisher, res_publisher_url]
        except Exception as e:
            logging.error(e.args)
            return ['EOR:1010', 'EOR:1011']


class DmhyHomeSpider(Spider):
    home = web_home['动漫花园']

    def __init__(self, page):
        if page > 1:
            super().__init__(url=self.home + f'topics/list/page/{page}')
        else:
            super().__init__(url=self.home)

    def get_home_res(self):
        json_res_list = []
        try:
            trs = self.parser.css('#topic_list > tbody > tr')
            if len(trs) == 0:
                return json.dumps({'error:EOR': 'EOR:1018'})
            for tr in trs:
                tds = tr.css('td')
                res_send_time_data = self.get_send_time(tds[0])
                res_send_time = res_send_time_data[0]
                res_send_time_text = res_send_time_data[1]
                res_type = self.get_res_type(tds[1])
                res_author_title = self.get_res_author_title(tds[2], self.home)
                res_author = res_author_title[0]
                res_author_url = res_author_title[1]
                res_title = res_author_title[2]
                res_url = res_author_title[3]
                res_downlink = self.get_res_downlink(tds[3])
                res_magent = res_downlink[0]
                res_pikpak = res_downlink[1]
                res_size = self.get_res_size(tds[4])
                json_res_list.append({'res_title': res_title,
                                      'res_url': res_url,
                                      'res_author': res_author,
                                      'res_author_url': res_author_url,
                                      'res_send_time': res_send_time,
                                      'res_send_time_text': res_send_time_text,
                                      'res_type': res_type,
                                      'res_magent': res_magent,
                                      'res_pikpak': res_pikpak,
                                      'res_size': res_size})
            return json.dumps(json_res_list)

        except Exception as e:
            logging.error(
                f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]：\n{traceback.format_exc()}'
            )
            return [e, f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]：\n{traceback.format_exc()}']

    @staticmethod
    def get_send_time(td: parsel.Selector):
        try:
            send_time = re.sub(r'/', '-', td.re(r'<span.*?>([\s\S]*?)</span>')[0])
            send_time_text = td.re(r'(.*?)<span')[0]
            if send_time_text is None:
                return [send_time, 'EOR:1020']
            if send_time is None:
                return ['EOR:1019', send_time_text]
            return [send_time, send_time_text]
        except Exception as e:
            return ['EOR:1019', 'EOR:1020']

    @staticmethod
    def get_res_type(td: parsel.Selector):
        try:
            res_type = td.re(r'<font.*?>([\s\S]*?)</font>')[0]
            if res_type is None:
                return 'EOR:1021'
            return res_type
        except Exception as e:
            return e

    @staticmethod
    def get_res_author_title(td: parsel.Selector, home_url):
        try:
            try:
                res_author = td.css('span').re(r'<a.*?>([\s\S]*?)</a>')[0]
                res_author_url = home_url + td.css('span > a')[0].attrib['href']
                res_title = re.findall(r'<a.*?>([\s\S]*?)</a>', str(td.css('span + a').get()))[0]
                res_url = home_url + td.css('span + a').attrib['href']
            except IndexError:
                res_author = 'EOR:1022'
                res_author_url = 'EOR:1023'
                res_title = td.re('<a.*?>([\S\s]*?)</a>')[0]
                res_url = home_url + td.xpath('//td/a/@href').get()
            return [res_author, res_author_url, res_title, res_url]
        except Exception as e:
            traceback.print_exc()
            return ['EOR:1022', 'EOR:1023', 'EOR:NULL,EOR:NULL']
            pass

    @staticmethod
    def get_res_downlink(td: parsel.Selector):
        res_magent = td.xpath('//td/a[@title="磁力下載"]/@href').get()
        res_pikpak = td.xpath('//td/a[contains(@class,"download-pikpak")]/@href').get()
        return [res_magent, res_pikpak]

    @staticmethod
    def get_res_size(td: parsel.Selector):
        return td.re(r'<td.*?>([\s\S]*?)</td>')[0]

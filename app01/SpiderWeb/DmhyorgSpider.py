import json
import logging
import re
import time
import traceback

from django.http import HttpResponse

from app01.SpiderWeb.Spider import Spider


class DmhyorgSearch(Spider):
    home = 'https://dmhy.b168.net'

    def __init__(self, key, page):
        super().__init__(f'https://dmhy.b168.net/topics/list/page/{page}?keyword={key}')

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
                    'res_publisher_url': res_publisher_url
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
        return re.findall(r'>(.*?)<', td)[0]

    @staticmethod
    def get_res_type(td):
        # 资源类型
        return re.findall(r'<font.*>(.*?)</font>', td)

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

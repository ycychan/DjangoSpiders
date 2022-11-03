# -*- coding: utf-8 -*-
# @Time    : 2022/11/3 11:05
# @Author  : dominoar
# @Email   : duominuoaier@gmail.com
# @File    : webhome.py
# @Software: PyCharm

# 需要爬取页的url地址
web_home = {'量子ACG': 'https://lzacg.one/',
            '动漫花园': 'https://dmhy.anoneko.com/'}

# 爬取类的搜索反射类名
search_reflex = {'lzacgsearch': 'LzacgSpider',
                 'dmhysearch': 'DmhyorgSearch'}

# 爬取类的主页反射类名
home_reflex = {'lzacghome': 'LzacgHomeSpider',
               'dmhyhome': 'DmhyHomeSpider'}

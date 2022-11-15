# Create your views here.
import json
import logging
import re

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import webhome
from app01.SpiderWeb.DmhyorgSpider import DmhyorgSearch, DmhyHomeSpider
from app01.SpiderWeb.LzacgSpider import LzacgSpider, LzacgHomeSpider


def default(req):
    """首页返回值"""
    return render(req, '4-404/index.html')


@csrf_exempt
def search(req: HttpRequest):
    """需要添加的所有爬虫都必须将入口函数定义为get_search_res()"""
    json_body = json.loads(req.body.decode())
    key = json_body['key']
    page = json_body['page']
    mapping = re.sub(r'/', '', req.path_info)
    # IOC 创建对象
    searci = globals()[webhome.search_reflex[mapping]](key, page)
    res = searci.get_search_res()
    return resp_parser(res)


@csrf_exempt
def home(req: HttpRequest):
    """需要添加的所有爬虫都需要将入口函数定义为get_home_res"""
    page = json.loads(req.body.decode())['page']
    print(page)
    mapping = re.sub(r'/', '', req.path_info)
    homo = globals()[webhome.home_reflex[mapping]](page)
    res = homo.get_home_res()
    return resp_parser(res)


# 响应爬取的资源
def resp_parser(resource):
    if type(resource) == list:
        error_msg = {
            'res_title': resource[0],
            'res_url': resource[1]
        }
        json_error = json.dumps([error_msg])
        logging.error(json_error)
        resp = HttpResponse(json_error, content_type="application/json")
        resp['Access-Control-Allow-Headers'] = 'Content-Type'
        resp['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = HttpResponse(resource, content_type="application/json")
        resp['Access-Control-Allow-Headers'] = 'Content-Type'
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


def index(req):
    return render(req, 'index.html')

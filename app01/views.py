# Create your views here.
import json
import logging
import re

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import webhome
from app01.SpiderWeb.DmhyorgSpider import DmhyorgSearch
from app01.SpiderWeb.LzacgSpider import LzacgSpider, LzacgHomeSpider


@csrf_exempt
def search(req: HttpRequest):
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
    mapping = re.sub(r'/', '', req.path_info)
    homo = globals()[webhome.home_reflex[mapping]]()
    res = homo.get_home_res()
    return resp_parser(res)


# 响应爬取的资源
def resp_parser(resource):
    if type(resource) == list:
        error_msg = {
            'log': resource[0],
            'error': resource[1]
        }
        json_error = json.dumps(error_msg)
        logging.error(json_error)
        resp = HttpResponse(resource, content_type="application/json")
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

# Create your views here.
import json
import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app01.SpiderWeb.DmhyorgSpider import DmhyorgSearch
from app01.SpiderWeb.LzacgSpider import LzacgSpider


@csrf_exempt
def dmhy_search(req: HttpRequest):
    json_body = json.loads(req.body.decode())
    key = json_body['key']
    page = json_body['page']
    dmhy = DmhyorgSearch(key=key, page=page)
    resources = dmhy.get_search_res()
    return resp_parser(resources)


@csrf_exempt
def lzacg_search(req: HttpRequest):
    json_body = json.loads(req.body.decode())
    key = json_body['key']
    page = json_body['page']
    lzacg = LzacgSpider(key=key, page=page)
    resource = lzacg.get_search_res()
    return resp_parser(resource)


def index(req: HttpRequest):
    return render(req, 'index.html')


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

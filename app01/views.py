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
    if type(resources) == list:
        error_msg = {
            'log': resources[0],
            'error': resources[1]
        }
        json_error = json.dumps(error_msg)
        logging.error(json_error)
        return HttpResponse(json_error, content_type="application/json")
    else:
        return HttpResponse(resources, content_type="application/json")


@csrf_exempt
def lzacg_search(req: HttpRequest):
    json_body = json.loads(req.body.decode())
    key = json_body['key']
    page = json_body['page']
    print(type(key), type(page))
    lzacg = LzacgSpider(key=key, page=page)
    resource = lzacg.get_search_res()
    if type(resource) == list:
        error_msg = {
            'log': resource[0],
            'error': resource[1]
        }
        json_error = json.dumps(error_msg)
        logging.error(json_error)
        return HttpResponse(json_error, content_type="application/json")
    else:
        return HttpResponse(resource, content_type="application/json")


def index(req: HttpRequest):
    return render(req, 'index.html')

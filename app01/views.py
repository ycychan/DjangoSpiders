# Create your views here.
import json

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01.SpiderWeb.DmhyorgSpider import DmhyorgSearch
from app01.SpiderWeb.LzacgSpider import LzacgSpider


@csrf_exempt
def dmhy_search(req: HttpRequest):
    key = req.POST.get(key='key')
    page = req.POST.get(key='page')
    dmhy = DmhyorgSearch(key=key, page=page)
    resources = dmhy.get_search_res()
    if type(resources) == list:
        error_msg = {
            'log': resources[0],
            'error': resources[1]
        }
        json_error = json.dumps(error_msg)
        print(json_error)
        return HttpResponse(json_error)
    else:
        return HttpResponse(resources)


@csrf_exempt
def lzacg_search(req: HttpRequest):
    key = req.POST.get('key')
    page = req.POST.get('page')
    lzacg = LzacgSpider(key=key, page=page)
    resource = lzacg.get_search_res()
    if type(resource) == list:
        error_msg = {
            'log': resource[0],
            'error': resource[1]
        }
        json_error = json.dumps(error_msg)
        print(json_error)
        return HttpResponse(json_error)
    else:
        return HttpResponse(resource)

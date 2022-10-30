# Create your views here.
from django.http import HttpRequest, HttpResponse

from app01.SpiderWeb.DmhyorgSpider import DmhyorgSearch
from app01.SpiderWeb.LzacgSpider import LzacgSpider


def dmhy_search(req: HttpRequest):
    key = req.GET.get(key='key')
    page = req.GET.get(key='page')
    dmhy = DmhyorgSearch(key=key, page=page)
    resources = dmhy.get_search_res()
    if type(resources) == list:
        error_msg = {
            'log': resources[0],
            'error': resources[1]
        }
        return HttpResponse("EOR:500")
    else:
        return HttpResponse(resources)


def lzacg_search(req: HttpRequest):
    key = req.GET.get('key')
    page = req.GET.get('page')
    lzacg = LzacgSpider(key=key, page=page)
    resource = lzacg.get_search_res()
    if type(resource) == list:
        error_msg = {
            'log': resource[0],
            'error': resource[1]
        }
        return HttpResponse("EOR:500")
    else:
        return HttpResponse(resource)

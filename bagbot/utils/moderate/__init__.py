from bagbot.utils import requests
from nonebot import get_driver

moderatecontent_api = 'https://api.moderatecontent.com/anime/'
config = get_driver().config
params = {
    'key': config.moderatecontent
}


def truncateYandereUrl(url: str):
    cnt = 0
    for c in url:
        cnt += c == '/'
    assert cnt == 5
    url = url[:url.rfind('/')]+'/image'+url[url.rfind('.'):]
    return url


async def getModerated(url: str):
    if url.find('files.yande.re') != -1:
        url = truncateYandereUrl(url)
    params['url'] = url
    res = await requests.get(moderatecontent_api,params=params,timeout=15)
    return res.json()


async def getRating(url: str):
    data = await getModerated(url)
    return data['rating_label']

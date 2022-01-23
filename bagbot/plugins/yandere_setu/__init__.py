from nonebot import on_command
from nonebot.adapters import Event
from nonebot.adapters.telegram import MessageSegment
from bagbot.utils import requests
import random
import urllib.parse

yandere_api = 'https://yande.re/post.json'
params = {
    'api_version': 2,
    'limit': 100
}
basetags = 'rating:questionable'

setu = on_command('yandere')
ctime = -1


@setu.handle()
async def deal_setu(event: Event):
    args = str(event.get_plaintext()).split()
    params['tags'] = basetags
    for i in range(1, len(args)):
        params['tags'] += '+' + args[i]
    payload = urllib.parse.urlencode(params, safe=':+')
    try:
        res = await requests.get(yandere_api, params=payload)
        data = res.json()['posts']
    except Exception as e:
        await setu.finish('访问yandere API失败，错误为：'+repr(e))
    if len(data) == 0:
        await setu.finish('返回列表为空')
    i = random.randint(0, len(data)-1)
    url = data[i]['sample_url']
    description = 'yandereID: ' + str(data[i]['id']) + '\n'
    description += 'tags: ' + data[i]['tags'] + '\n'
    await setu.finish(MessageSegment.photo(file=url, caption=description))

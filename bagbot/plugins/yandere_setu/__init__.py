from nonebot import on_startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment
from bagbot.utils import requests
import random, urllib.parse

yandere_api = 'https://yande.re/post.json'
params = {
    'api_version': 2,
    'limit': 100
}

setu = on_startswith('yandere')
ctime = -1

@setu.handle()
async def deal_setu(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    if len(args) > 1:
        params['tags'] = args[1]
        for i in range(2, len(args)):
            params['tags'] += '+' + args[i]
    else:
        if 'tags' in params:
            params.pop['tags']
    payload = urllib.parse.urlencode(params, safe=':+')
    try:
        res = await requests.get(yandere_api, params=payload)
        data = res.json()['posts']
    except Exception as e:
        await setu.finish('访问yandere API失败，错误为：'+repr(e))
    if len(data) == 0:
        await setu.finish('返回列表为空')
    li = list()
    for i in range(0, len(data)):
        if data[i]['rating'] == 'q' and data[i]['score'] >= 4:
            li.append(i)
    if not li:
        await setu.finish('因为设计上的原因没有找到涩图')
    i = li[random.randint(0, len(li)-1)]
    url = data[i]['sample_url']
    description = 'yandereID: ' + str(data[i]['id']) + '\n'
    description += 'tags: ' + data[i]['tags'] + '\n'
    await setu.send(description)
    await setu.finish(MessageSegment.image(url))

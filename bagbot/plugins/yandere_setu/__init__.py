from nonebot import on_startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment
from bagbot.utils import requests
import random
import urllib.parse
import asyncio

yandere_api = 'https://yande.re/post.json'
params = {
    'api_version': 2,
    'limit': 100
}
basetags = 'rating:questionable'

setu = on_startswith('yandere')
ctime = -1


@setu.handle()
async def deal_setu(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    if args[0] != 'yandere':
        await setu.finish()
    params['tags'] = basetags
    if len(args) > 1:
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
    await setu.send(description)
    message = await setu.send(MessageSegment.image(url))
    await asyncio.sleep(30)
    await bot.call_api('/delete_msg',message)

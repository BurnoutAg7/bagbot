from nonebot import on_startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment
import httpx
async def get(url: str, **kwargs):
    async with httpx.AsyncClient() as client:
        return await client.get(url, **kwargs)

lolicon_api = 'https://api.lolicon.app/setu/v2'
pic_size = 'regular'

setu = on_startswith('涩图')


@setu.handle()
async def deal_setu(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    params = dict()
    params['size'] = pic_size
    if len(args) > 1:
        params['tag'] = args[1]
    try:
        req = await get(lolicon_api, params=params)
        data = req.json()
    except Exception as e:
        await setu.finish('访问lolicon API失败，错误为：'+str(repr(e)))
    if data['error'] != '':
        await setu.finish('lolicon API返回了一个错误')
    if len(data['data']) == 0:
        await setu.finish('找不到指定tag的涩图')
    data = data['data'][0]
    description = 'PixivID: '+str(data['pid'])+'\n'
    url = data['urls'][pic_size]
    if len(data['tags']):
        for i in range(1, len(data['tags'])):
            description += '#'+data['tags'][i]+' '
        description = description[:-1]+'\n'+url
    else:
        description = description+url
    await setu.send(description)
    await setu.finish(MessageSegment.image(url))

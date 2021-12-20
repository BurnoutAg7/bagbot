from nonebot import on_startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment
import httpx
async def get(url: str, **kwargs):
    async with httpx.AsyncClient() as client:
        return await client.get(url, **kwargs)

tianque_api = 'http://www.tianque.top/d2api/today/'

daily = on_startswith('日报')


@daily.handle()
async def deal_daily(bot: Bot, event: Event, state: T_State):
    try:
        req = await get(tianque_api)
        data = req.json()
    except Exception as e:
        await daily.finish('访问天阙API失败，错误为：'+repr(e))
    try:
        url = data['img_url']
    except Exception as e:
        await daily.finish('返回的JSON解析失败，错误为：'+repr(e))
    await daily.finish(MessageSegment.image(url))

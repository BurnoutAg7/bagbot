from nonebot import on_command
from nonebot.adapters import Event
from nonebot.adapters.telegram import MessageSegment
from urllib.parse import urlencode

yurafuca = 'http://yurafuca.com/5000choyen/result_cn.html?'

params = {
    'top': '',
    'bottom': '',
    'bx': '250',
    'order': 'false',
    'color': 'false',
    'width': '900',
    'height': '290'
}

choyen = on_command('5000choyen')


@choyen.handle()
async def deal_choyen(event: Event):
    args = str(event.get_plaintext()).split()
    if len(args) < 3:
        await choyen.finish('没有指定上下两行的话呢')
    params['top'] = args[1]
    params['bottom'] = args[2]
    for i in range(3, len(args)):
        params['bottom'] += ' ' + args[i]
    url = yurafuca + urlencode(params)
    await choyen.finish(url)

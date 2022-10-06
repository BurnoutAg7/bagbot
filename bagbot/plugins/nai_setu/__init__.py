from nonebot import on_command
from nonebot.adapters import Event
from nonebot.adapters.telegram.message import File
from bagbot.utils import requests
from nonebot import get_driver
import json
import httpx
import base64

config = get_driver().config
headers = {
    'Authorization': 'Bearer '
}
headers['Authorization'] = 'Bearer '+config.nai_token
body = json.loads('''
{
  "input": "",
  "model": "safe-diffusion",
  "parameters": {
    "width": 512,
    "height": 768,
    "scale": 12,
    "sampler": "k_euler_ancestral",
    "steps": 28,
    "n_samples": 1,
    "strength": 0.7,
    "noise": 0.2,
    "ucPreset": 0,
    "uc": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"
  }
}
''')
url = 'https://api.novelai.net/ai/generate-image'

portrait = on_command('nai_portrait')


@portrait.handle()
async def deal_portrait(event: Event):
    args = str(event.get_plaintext()).split()
    if len(args) == 1:
        await portrait.finish('必须给 nai 指定作图要求')
    args = ' '.join(args[1:])
    body['input'] = args
    body['parameters']['width'] = 512
    body['parameters']['height'] = 768
    try:
        res = await requests.post(url=url, headers=headers, json=body, timeout=30)
    except httpx.ReadTimeout:
        await portrait.send('请求超时')
    if res.status_code != 201:
        await portrait.finish('返回状态码不正常')
    b64s = res.text[res.text.find('data:')+5:]
    img = base64.b64decode(b64s)
    await portrait.finish(File.photo(img))

landscape = on_command('nai_landscape')


@landscape.handle()
async def deal_landscape(event: Event):
    args = str(event.get_plaintext()).split()
    if len(args) == 1:
        await landscape.finish('必须给 nai 指定作图要求')
    args = ' '.join(args[1:])
    body['input'] = args
    body['parameters']['width'] = 768
    body['parameters']['height'] = 512
    try:
        res = await requests.post(url=url, headers=headers, json=body, timeout=30)
    except httpx.ReadTimeout:
        await landscape.send('请求超时')
    if res.status_code != 201:
        await landscape.finish('返回状态码不正常')
    b64s = res.text[res.text.find('data:')+5:]
    img = base64.b64decode(b64s)
    await landscape.finish(File.photo(img))

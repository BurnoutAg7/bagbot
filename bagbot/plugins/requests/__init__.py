import httpx
from nonebot.plugin import export
export = export()


@export
async def send_get(url: str, **kwargs):
    async with httpx.AsyncClient() as client:
        return await client.get(url, **kwargs)


@export
async def send_post(url: str, **kwargs):
    async with httpx.AsyncClient() as client:
        return await client.post(url, **kwargs)

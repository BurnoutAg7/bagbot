from time import time
from nonebot import on_command
from nonebot.adapters.telegram import Event, Bot
from nonebot.adapters.telegram.event import MessageEvent

ban = on_command('ban')


@ban.handle()
async def deal_setu(event: Event, bot: Bot):
    try:
        ban_len = str(event.get_plaintext()).split()[1]
    except Exception:
        await ban.finish('未指定时间')
    if type(ban_len) != int:
        await ban.finish('时间不是整数')
    message_event = MessageEvent(event)
    original = message_event.reply_to_message
    if original == None:
        await ban.finish('请回复一个消息')
    chat = original.get_session_id()
    user = original.get_user_id()
    bot.ban_chat_member(chat_id=chat, user_id=user, until_date=time()+ban_len)
    await ban.finish('已举办')

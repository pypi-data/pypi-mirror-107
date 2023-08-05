from nonebot import on_command
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.typing import T_State

from ...database import DB as Config
from ...utils import permission_check, to_me


dynamic_off = on_command('关闭动态', rule=to_me(), priority=5)

dynamic_off.handle()(permission_check)

@dynamic_off.handle()
async def handle_first_recive(bot: Bot, event: MessageEvent, state: T_State):
    args = str(event.message).strip()
    if args:
        state['uid'] = args

@dynamic_off.got('uid', prompt='请输入主播的 uid')
async def _(bot: Bot, event: MessageEvent, state: T_State):
    uid = state['uid']
    with Config(event) as config:
        msg = await config.set('dynamic', uid, False)
    await dynamic_off.finish(msg.replace('name', '关闭动态'))

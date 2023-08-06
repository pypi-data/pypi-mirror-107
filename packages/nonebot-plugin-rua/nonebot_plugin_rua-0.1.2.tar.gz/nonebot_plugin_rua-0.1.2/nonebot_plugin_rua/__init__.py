from io import BytesIO
from os import path

import requests
from nonebot import get_driver, on_command, on_notice
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, PokeNotifyEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State
from PIL import Image

from .data_source import generate_gif

master = get_driver().config.master


data_dir = path.join(path.dirname(__file__), 'data')
path = path.abspath(__file__).split('__')[0]
img_src = path +  '/data/output.gif'
img = MessageSegment.image(f'file://{img_src}')


rua_me = on_notice()
'''
戳一戳事件
'''      
@rua_me.handle()
async def _t3(bot: Bot, event: PokeNotifyEvent):

    if event.target_id in master:
        creep_id = event.sender_id
    else: creep_id = event.target_id


    try:
        
        url = f'http://q1.qlogo.cn/g?b=qq&nk={creep_id}&s=160'
        resp = requests.get(url)
        resp_cont = resp.content
        avatar = Image.open(BytesIO(resp_cont))
        #<class 'PIL.JpegImagePlugin.JpegImageFile'>
        generate_gif(data_dir, avatar)
        await bot.send(event, message=img)
    except:
        pass

    
rua = on_command('rua')
@rua.handle()
async def rua_handle(bot: Bot, event: Event, state: T_State):
    try:
        msg = (str(event.raw_message).split('rua')[1].strip())
        if ':image' in msg:         
            state['url'] = (msg.split('url=')[-1][:-2])     
        elif msg.isdigit():
            id = int(msg)
            state['url'] = f'http://q1.qlogo.cn/g?b=qq&nk={id}&s=160'
    except:
        pass


@rua.got("url", prompt="要rua点什么～")
async def rua_got(bot: Bot, event: Event, state: T_State):
    msg = str(state['url'])
    state['url'] = (msg.split('url=')[-1][:-2])
    resp = requests.get(state['url'])
    resp_cont = resp.content
    try:
        avatar = Image.open(BytesIO(resp_cont))
        generate_gif(data_dir, avatar)
        await rua.finish(img)
    except:
        pass

import os
from nonebot import on_message, on_command
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command

from nonebot.adapters.onebot.v11 import Bot, MessageEvent

from nonebot.plugin import PluginMetadata

current_dir = os.path.dirname(os.path.abspath(__file__))
resource_dir = os.path.join(current_dir, "resource")

__plugin_meta__ = PluginMetadata(
    name='一些插件',
    description='一些插件',
    usage='/文档 /仓库 /公众号 /报名',
)

get_doc = on_command("文档", priority=15, block=True)
get_repo = on_command("仓库", priority=15, block=True)
get_wechat = on_command("公众号", priority=15, block=True)
get_signup = on_command("报名", priority=15, block=True)
get_advertise = on_command("宣传片", priority=15, block=True)

@get_doc.handle()
async def handle_doc(bot: Bot, event: MessageEvent):
    await get_doc.send(message="https://paa.abc235.site/documentation/")


@get_repo.handle()
async def handle_repo(bot: Bot, event: MessageEvent):
    await get_repo.send(message="https://github.com/Peiyang-Aeromodelling-Association/")


@get_wechat.handle()
async def handle_wechat(bot: Bot, event: MessageEvent):
    qr_code_path = os.path.join(resource_dir, "wechat.png")
    await get_wechat.send(message=Message(f"[CQ:image,file=file:///{qr_code_path}]"))


@get_signup.handle()
async def handle_signup(bot: Bot, event: MessageEvent):
    qr_code_path = os.path.join(resource_dir, "signup.png")
    await get_signup.send(message=Message(f"[CQ:image,file=file:///{qr_code_path}]"))

@get_advertise.handle()
async def handle_advertise(bot: Bot, event: MessageEvent):
    video_path = os.path.join(resource_dir, "advertise.mp4")
    await get_advertise.send(message=Message(f"[CQ:video,file=file:///{video_path}]"))
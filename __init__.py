import os
import time

import nonebot
from nonebot import on_message, on_command, on_notice
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command

from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupIncreaseNoticeEvent

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

broadcast = on_command("broadcast", priority=15, block=True, permission=GROUP_OWNER | GROUP_ADMIN)

# if a person joins the group 537857732, send a welcome message
welcome = on_notice(priority=15, block=True)


@welcome.handle()
async def handle_welcome(bot: Bot, event: GroupIncreaseNoticeEvent):
    if event.group_id == 537857732:  # 537857732 is the group id of PAA
        signup_qr_code_path = os.path.join(resource_dir, "signup.png")
        wechat_qr_code_path = os.path.join(resource_dir, "wechat.png")
        # send private message
        await bot.send_private_msg(user_id=event.user_id,
                                   group_id=event.group_id,
                                   message=Message(f"欢迎加入北洋小飞机协会！我是外联bot。\n"
                                                   f"报名二维码：[CQ:image,file=file:///{signup_qr_code_path}]\n"
                                                   f"公众号二维码：[CQ:image,file=file:///{wechat_qr_code_path}]\n"
                                                   f"文档：https://paa.abc235.site/documentation/\n"
                                                   f"github：https://github.com/Peiyang-Aeromodelling-Association/\n"
                                                   f"欢迎进一步交流！\n"))


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
    video_path = os.path.join(resource_dir, "advertise_compressed.mp4")
    await get_advertise.send(message=Message(f"[CQ:video,file=file:///{video_path}]"))


@broadcast.handle()
async def handle_broadcast(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    # send message to all members in the group in private
    msg = args.extract_plain_text()

    if not msg:
        await broadcast.finish("请输入要广播的内容")

    group_id = event.group_id
    member_list = await bot.get_group_member_list(group_id=group_id)

    success_count = 0

    self_id = nonebot.get_bot().self_id
    logger.debug(f"broadcast self_id: {self_id}")
    logger.debug(f"broadcast to {len(member_list)} members in group {group_id} with message: {msg} ")

    for member in member_list:
        try:
            if member["user_id"] == self_id:
                continue

            await bot.send_private_msg(user_id=member["user_id"],
                                       group_id=group_id,
                                       message=msg)
            time.sleep(1)  # TODO: avoid being blocked by server
            logger.info(f"broadcast sent message to user {member['user_id']} in group {group_id}")
            success_count += 1
        except nonebot.adapters.onebot.v11.exception.ActionFailed as e:
            logger.error(f"broadcast failed to send message to user {member['user_id']} in group {group_id} with exception: {e}")
            continue

    await broadcast.finish(f"广播成功发送给{success_count}人")

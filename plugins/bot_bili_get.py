from time import sleep

from botoy import Action, FriendMsg, GroupMsg

from modules import bot_config
from modules.get_bili_dyn import get_dyn
from modules.my_send import Send as send
from botoy import decorators as deco
from plugins.bot_bili_find import get_bili_name
import re


action = Action(qq=bot_config.bot_qq, host=bot_config.host, port=bot_config.port)


@deco.ignore_botself
@deco.in_content("最新动态")
def receive_friend_msg(ctx: FriendMsg):
    Action(ctx.CurrentQQ)


@deco.ignore_botself
@deco.in_content("最新动态")
def receive_group_msg(ctx: GroupMsg):
    msg = ctx.Content
    num = re.findall("最新动态(.*?)条", msg)
    try:
        uid = msg.split()[1]
    except:
        send.text(ctx, "uid异常，请检查是否输入有误！")
        return
    if not num:
        num = 1
    else:
        num = num[0]
    try:
        num = int(num)
    except:
        num_dict = {"一": "1", "二": "2", "两": "2", "三": "3", "四": "4", "五": "5", "六": "6",
                    "七": "7", "八": "8", "九": "9", "十": "10"}
        num = int(num_dict.get(num))
    if num > 12:
        send.text(ctx, "输入条数过多")
        return
    for i in range(num):
        try:
            recv = get_dyn(i, uid)
            if recv == "less":
                send.text(ctx, "没有更多动态了")
            cont = recv.split("***")
            upz = get_bili_name(uid)
            text = upz + "\n" + cont[0].split("@@@")[0]
            send.text(ctx, text)
            cont.pop(0)
            for pic in cont:
                sleep(1)
                pic = pic.split("@@@")[0]
                action.sendGroupPic(ctx.FromGroupId, picUrl=pic)
            sleep(1)
        except:
            send.text(ctx, "动态解析异常！")

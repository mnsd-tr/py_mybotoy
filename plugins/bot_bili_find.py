import json
import sys

from botoy import Action, FriendMsg, GroupMsg
from botoy import decorators as deco
import requests
from modules.my_send import Send as send


def get_bili_info(uid):
    url = "http://api.bilibili.com/x/web-interface/card?mid=" + str(uid)
    res = requests.get(url)
    res.encoding = 'utf-8'
    dict_cont = json.loads(res.text)
    cont = dict_cont["data"]
    card = cont["card"]
    text = "uid:"+str(uid)+"\nup主:"+card["name"]+"\n性别:"+card["sex"]+"\n认证:"+card["Official"]["title"]+"\n签名:" \
           ""+card["sign"]+"\n等级:"+str(card["level_info"]["current_level"])+"\n投稿数:"+str(cont["archive_count"])+"\n" \
           "关注数:"+str(card["attention"])+"\n粉丝数:"+str(cont["follower"])+"!@#"+card["face"]
    return text


def get_bili_name(uid):
    url = "http://api.bilibili.com/x/web-interface/card?mid=" + str(uid)
    res = requests.get(url)
    res.encoding = 'utf-8'
    dict_cont = json.loads(res.text)
    cont = dict_cont["data"]
    card = cont["card"]
    return card["name"]


def receive_friend_msg(ctx: FriendMsg):
    Action(ctx.CurrentQQ)


# 通过uid查询用户信息
@deco.ignore_botself
@deco.in_content("查询uid")
def receive_group_msg(ctx: GroupMsg):
    try:
        uid = ctx.Content[5:]
        cont = get_bili_info(uid).split("!@#")
        if sys.platform == "win32":
            send.text(ctx, cont[0] + "\n头像:" + cont[1])
        else:
            send.picture(ctx, cont[0], cont[1])
    except:
        send.text(ctx, "查询异常，请检查uid是否正确！")


# print(get_bili_info(21648772).split("!@#"))

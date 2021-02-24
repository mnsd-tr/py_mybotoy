from botoy import FriendMsg, GroupMsg
from modules.my_send import Send as send
from botoy import decorators as deco


@deco.ignore_botself
@deco.in_content("视频解析")
def receive_friend_msg(ctx: FriendMsg):
    send.text(ctx, "通用解析接口：\nhttp://video.mnsd.xyz/\n"
                   "B站解析接口：\nhttps://bilibili.iiilab.com/")


@deco.ignore_botself
# @deco.from_these_users()
@deco.in_content("视频解析")
def receive_group_msg(ctx: GroupMsg):
    send.text(ctx, "通用解析接口：\nhttp://video.mnsd.xyz/\n"
                   "B站解析接口：\nhttps://bilibili.iiilab.com/", True)



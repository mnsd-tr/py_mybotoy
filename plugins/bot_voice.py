from botoy import FriendMsg, GroupMsg, Action

from modules import bot_config
from modules.my_send import Send as send
from botoy import decorators as deco


action = Action(qq=bot_config.bot_qq, host=bot_config.host, port=bot_config.port)


@deco.ignore_botself
@deco.in_content("语音")
def receive_friend_msg(ctx: FriendMsg):
    print(ctx.FromUin)
    action.sendFriendVoice(ctx.FromUin, voiceUrl="http://video.mnsd.xyz/voice/yyw.mp3")


@deco.ignore_botself
@deco.in_content("晓丹的月牙湾")
def receive_group_msg(ctx: GroupMsg):
    action.sendGroupVoice(ctx.FromGroupId, voiceUrl="http://123.57.155.177/voice/yyw.mp3")



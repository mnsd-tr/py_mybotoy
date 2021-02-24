import base64

from modules import bot_config
from botoy import Action, FriendMsg, GroupMsg


action = Action(qq=bot_config.bot_qq, host=bot_config.host, port=bot_config.port)


class Send:
    @staticmethod
    def to_base64(filename):
        with open(filename, 'rb') as f:
            coding = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
            # logger.info('本地base64转码~')
            return coding.decode()

    @staticmethod
    def text(ctx, text, atUser: bool = False):
        # ------------------------------------
        if ctx.__class__.__name__ == 'GroupMsg':
            if atUser:
                action.sendGroupText(ctx.FromGroupId, text, ctx.FromUserId)
            else:
                action.sendGroupText(ctx.FromGroupId, text)
        else:
            if ctx.TempUin is None:  # None为好友会话
                action.sendFriendText(ctx.FromUin, text)
            else:  # 临时会话
                action.sendPrivateText(ctx.FromUin, text, ctx.TempUin)
        return

    @staticmethod
    def picture(ctx, text='', picUrl='', flashPic=False, atUser: bool = False, base64code='', fileMd5=''):
        # ------------------------------------------------------
        if ctx.__class__.__name__ == 'GroupMsg':
            if atUser:
                action.sendGroupPic(ctx.FromGroupId, content=text, picUrl=picUrl, picBase64Buf=base64code,
                                    fileMd5=fileMd5, flashPic=flashPic)
            else:
                action.sendGroupPic(ctx.FromGroupId, content=text, picUrl=picUrl, picBase64Buf=base64code,
                                    fileMd5=fileMd5, flashPic=flashPic)
        else:
            if ctx.TempUin is None:
                action.sendFriendPic(ctx.FromUin, picUrl=picUrl, picBase64Buf=base64code, fileMd5=fileMd5,
                                     content=text, flashPic=flashPic)
            else:
                action.sendPrivatePic(ctx.FromUin, ctx.FromGroupID, text, picUrl=picUrl,
                                      picBase64Buf=base64code,
                                      fileMd5=fileMd5)
        return

    @staticmethod
    def revoke(ctx):
        # ------------------------------------------------------
        action.revokeGroupMsg(ctx.QQG, ctx.MsgSeq, ctx.MsgRandom)


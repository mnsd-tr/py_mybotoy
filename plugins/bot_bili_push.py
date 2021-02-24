import json
import threading
from botoy import Action, FriendMsg, GroupMsg
from modules.my_send import Send as send
from botoy import decorators as deco
from modules import get_bili_dyn as get_dynamic, bot_config
from time import sleep
from modules.db_helper import DbHelper
from modules.stop_thread import stop_thread
from plugins.bot_bili_find import get_bili_name

action = Action(qq=bot_config.bot_qq, host=bot_config.host, port=bot_config.port)


def create_bili_push():
    while 1:
        print("呼吸...........")
        cnt = 0
        goq_l = DbHelper.get_open_qg()
        u_t_l = []
        for qg in goq_l:
            u_t_l.extend(DbHelper.get_uid_time(qg))
        u_t_l = list(set([tuple(t) for t in u_t_l]))
        u_t_l = [list(v) for v in u_t_l]
        for u_t in u_t_l:
            uid = u_t[0]
            log_time = u_t[1]
            try:
                recv = get_dynamic.get_dyn(0, uid)
                get_time = int(recv.split("@@@")[1])
                if get_time > log_time:
                    cont = recv.split("@@@")[0].split("***")
                    upz = get_bili_name(uid)
                    text = "up主:" + upz + " 更新动态：" + cont[0][3:]
                    qg_l = DbHelper.get_qg(uid)
                    cont.pop(0)
                    for qg in qg_l:
                        action.sendGroupText(qg, text)
                        for pic in cont:
                            sleep(1)
                            action.sendGroupPic(qg, picUrl=pic)
                        DbHelper.time_update(qg, uid, get_time)
                elif get_time < log_time:
                    upz = get_bili_name(uid)
                    qg_l = DbHelper.get_qg(uid)
                    text = "up主:" + upz + "可能删除了最新一条动态哟，猜猜是什么！"
                    for qg in qg_l:
                        action.sendGroupText(qg, text)
                        DbHelper.time_update(qg, uid, get_time)
                cnt = 0
            except:
                cnt += 1
                if cnt > 3:
                    timeout = [20, 60, 300, 1800, 3600]
                    to_str = ["1分钟", "5分钟", "30分钟", "1小时"]
                    text = "扫描失败，可能ip已被关小黑屋，将于" + str(to_str[cnt - 4]) + "后再次发起请求..."
                    action.sendFriendText(bot_config.su_admin, text)
                    sleep(timeout[cnt])
            sleep(bot_config.timeout)
        sleep(2)


def del_bili_push(uid, qg):
    rlt = DbHelper.delete(qg, uid)
    if rlt == 1:
        action.sendGroupText(qg, "删除成功")
    else:
        action.sendGroupText(qg, "删除失败，可能该群并未设置此uid")


@deco.ignore_botself
@deco.from_these_users(364988395)
@deco.in_content("推送列表")
def receive_friend_msg(ctx: FriendMsg):
    text = DbHelper.read()
    send.text(ctx, str(text))


# @deco.from_these_users(364988395)
@deco.ignore_botself
@deco.in_content("推送")
def receive_group_msg(ctx: GroupMsg):
    if ctx.Content == "推送检测":
        push_status = bot_config.get_push_status()
        if push_status == 0:
            send.text(ctx, "程序已被终止，请联系管理员")
        else:
            qg_status = DbHelper.qg_status(ctx.FromGroupId)
            if qg_status == 0:
                send.text(ctx, "程序正在运行，但本群推送已关闭，发送”推送开启“以打开")
            else:
                send.text(ctx, "本群推送服务已开启，请等待接收...")

    elif ctx.Content[:4] == "推送新建":
        try:
            uid = int(ctx.Content[4:])
            name = get_bili_name(uid)
            qg = ctx.FromGroupId
            DbHelper.creat(qg, uid, ctx.FromGroupName)
            send.text(ctx, "为up主 " + name + " 新建成功")
        except:
            send.text(ctx, "参数异常！添加方式：推送新建+uid")
    elif ctx.Content[:4] == "推送删除":
        # 获取到消息里面的uid，qg参数新建对象
        uid = ctx.Content[4:]
        del_bili_push(uid, ctx.FromGroupId)
    elif ctx.Content[:4] == "推送列表":
        u_t_l = DbHelper.get_uid_time(ctx.FromGroupId)
        text = "已为以下up在本群开启推送服务："
        for u_t in u_t_l:
            uid = u_t[0]
            text = text + "\n" + get_bili_name(uid)
        send.text(ctx, text)
    elif ctx.Content[:6] == "推送关闭本群":
        DbHelper.close_status(ctx.FromGroupId)
        send.text(ctx, "已关闭")
    elif ctx.Content[:6] == "推送开启本群":
        DbHelper.open_status(ctx.FromGroupId)
        send.text(ctx, "已开启")
    else:
        send.text(ctx, "bilibili动态推送服务\n=====================\n"
                       "推送新建+uid => 在本群生成uid对应up的推送\n"
                       "推送删除+uid => 删除本群中uid对应up的推送\n"
                       "推送开启本群 => 打开本群推送服务\n"
                       "推送关闭本群 => 关闭本群推送服务\n"
                       "推送检测 => 查询目前推送状态\n"
                       "推送列表 => 查询本群已添加推送的up")


push = threading.Thread(target=create_bili_push)
if bot_config.push_status:
    push.start()

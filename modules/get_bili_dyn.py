import json
import time

import requests


headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 '
    'Safari/537.36 Edg/88.0.705.56 '
}


def pic_dyn(card):
    try:
        text = card["item"]["description"]
        try:
            pic_list = card["item"]["pictures"]
            pict_num = len(pic_list)
            text = text + "\n共" + str(pict_num) + "张图片：\n------------------\n"
            pic = ""
            for j in pic_list:
                text = text + j["img_src"] + "\n"
                pic = pic + "***" + j["img_src"]
            return text + "(图片由于体积过大正在发送中...)" + pic
        except Exception as e:
            print(e)
    except:
        text = card["item"]["content"]
    return text


def vid_dyn(card):
    cont = card["dynamic"]  # 动态描述
    title = card["title"]  # 视频标题
    desc = card["desc"]  # 视频描述
    pic = card["pic"]  # 封面图片
    link = card["short_link"]  # 短链接
    info = card["stat"]
    view = str(info["view"])  # 播放量
    coin = str(info["coin"])  # 硬币
    favor = str(info["favorite"])  # 收藏
    like = str(info["like"])  # 点赞
    reply = str(info["reply"])  # 评论
    share = str(info["share"])  # 转发
    cnt = "\n点赞:" + like +"  投币:" + coin + "\n收藏:" + favor + "   评论:" + reply + "\n转发:" + share + "   播放:" + view
    text = cont + "\n------------------\n" + "title:" + title + "\ndesc:" + desc + "\ndetail:" + link + cnt + "\n------------------\n" \
                   "封面图：\n" + pic + "(图片由于体积过大正在发送中...)" + "***" + pic
    return text


def zhuan_fa(card):
    cont = card["item"]["content"]
    link = json.loads(card["origin"])["short_link"]
    text = cont + "\n------------------\nfrom_link:" + link + "(此消息为转发消息)"
    return text


def send_msg(num, real_url):
    res = requests.get(real_url, headers=headers)
    res.encoding = 'utf-8'
    dict_cont = json.loads(res.text)
    next_index = dict_cont["data"]["next_offset"]
    try:
        text = "第" + str(num + 1) + "条\n"
        try:
            timeStamp = dict_cont["data"]["cards"][num]["desc"]["timestamp"]
        except IndexError:
            return "less"
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        text = text  + otherStyleTime + " \n====================\n"
        card = dict_cont["data"]["cards"][num]["card"]
        card = json.loads(card)
        try:
            is_video = card["videos"]
            text = text + vid_dyn(card)
        except Exception as e:
            try:
                text = text + zhuan_fa(card)
            except Exception as e:
                text = text + pic_dyn(card)
        return text + "@@@" + str(timeStamp)
    except Exception as e:
        print(e)


def get_dyn(num, uid):
    real_url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=" + str(uid) + "&off_set_dynamic=0"
    return send_msg(num, real_url)

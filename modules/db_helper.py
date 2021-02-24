import json
from time import sleep

from tinydb import TinyDB, where
from tinydb import Query


file = './config/bili_push.json'
db = TinyDB(file)
q = Query()


class DbHelper:
    # status表示该群的推送状态
    @staticmethod
    def creat(_qg: int, u_id: int, group_name: str, time=970329):
        dict_cont = DbHelper.read()
        for i in dict.keys(dict_cont):
            qg = int(dict_cont[i]["qg"])
            if qg == _qg:
                detail = dict_cont[i]["detail"]
                for j in detail:
                    uid = j[0]
                    if u_id == uid:
                        return 0
                detail.append([u_id, time])
                db.update({"detail": detail}, where("qg") == _qg)
                return 1
        db.insert({"qg": _qg, "name": group_name, "detail": [[u_id, time]], "push_status": 1})
        return 1

    @staticmethod
    def read():
        with open(file, "r") as f:
            cont = json.load(f)
        cont = cont["_default"]
        return cont

    @staticmethod
    def time_update(qg: int, uid: int, time: int):
        dict_cont = DbHelper.read()
        for i in dict.keys(dict_cont):
            c_qg = dict_cont[i]["qg"]
            if qg == c_qg:
                detail = dict_cont[i]["detail"]
                for j in detail:
                    c_uid = j[0]
                    if uid == c_uid:
                        detail.remove(j)
                        detail.append([c_uid, time])
                        db.update({"detail": detail}, where('qg') == qg)
                        return 1
        return 0

    @staticmethod
    def delete(_qg, u_id):
        try:
            dict_cont = DbHelper.read()
            for i in dict.keys(dict_cont):
                qg = int(dict_cont[i]["qg"])
                if qg == _qg:
                    detail = dict_cont[i]["detail"]
                    for j in detail:
                        uid = j[0]
                        if u_id == uid:
                            detail.remove(j)
                    if not detail:
                        db.remove(where('qg') == _qg)
                        return 1
                    db.update({"detail": detail}, where('qg') == _qg)
                    return 1
        except:
            return 0

    # 通过该群号qg返回一个uid列表值
    @staticmethod
    def get_uid_time(qg):
        dict_cont = DbHelper.read()
        for i in dict.keys(dict_cont):
            c_qg = dict_cont[i]["qg"]
            if qg == c_qg:
                detail = dict_cont[i]["detail"]
                if detail:
                    return detail
        return 0

    # 先获取一个状态不是1的所有qg
    @staticmethod
    def get_open_qg():
        dict_cont = DbHelper.read()
        qg_list = []
        for i in dict.keys(dict_cont):
            push_status = dict_cont[i]["push_status"]
            if push_status == 1:
                qg = dict_cont[i]["qg"]
                qg_list.append(qg)
        return qg_list

    # 通过uid返回一个状态不是0的qg的列表
    @staticmethod
    def get_qg(uid):
        dict_cont = DbHelper.read()
        qg_list = []
        for i in dict.keys(dict_cont):
            push_status = dict_cont[i]["push_status"]
            if push_status == 1:
                qg = dict_cont[i]["qg"]
                detail = dict_cont[i]["detail"]
                for j in detail:
                    c_uid = j[0]
                    if uid == c_uid:
                        qg_list.append(qg)
        qg_list = set(qg_list)
        qg_list = list(qg_list)
        if qg_list:
            return qg_list
        return 0

    # 通过qg查询当前群push状态
    @staticmethod
    def qg_status(qg):
        dict_cont = DbHelper.read()
        for i in dict.keys(dict_cont):
            cont = dict_cont[i]
            c_qg = cont["qg"]
            if qg == c_qg:
                return cont["push_status"]

    @staticmethod
    def open_status(qg):
        dict_cont = DbHelper.read()
        for i in dict.keys(dict_cont):
            cont = dict_cont[i]
            c_qg = cont["qg"]
            if qg == c_qg:
                db.update({"push_status": 1}, where('qg') == qg)
                return 1

    @staticmethod
    def close_status(qg):
        print("guanbi")
        dict_cont = DbHelper.read()
        for i in dict.keys(dict_cont):
            cont = dict_cont[i]
            c_qg = cont["qg"]
            if qg == c_qg:
                db.update({"push_status": 0}, where('qg') == qg)
                return 1


# uid = [1234, 5678, 9012, 3456]
# qg = [9876, 5432, 1098, 7654]
# group_name = "default"
# print(DbHelper.delete(qg, uid))

# for i in uid:
#     for j in qg:
#         DbHelper.creat(j, i, group_name)
# for xxx in qg:
#     print(DbHelper.qg_status(xxx))
# for xxx in qg:
#     print(DbHelper.close_status(xxx))
# for xxx in qg:
#     print(DbHelper.qg_status(xxx))
# for i in uid:
#     print(DbHelper.get_qg(i))


# 通过群号qg查找需要push的uid，再通过uid查询需要push到的群，一次查询，多次发送（尽量尝试连续不sleep发送）
# 通过qg查询到uid时同时返回对应的time，通过检测time在修改值时直接

# DbHelper.delete(711072397, 1722069106)
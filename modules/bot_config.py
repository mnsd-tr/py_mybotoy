import configparser

conf = configparser.ConfigParser()
file = "./config.ini"
conf.read(file, encoding="utf-8")

# bot
bot_qq = int(conf['bot']['qq'])
host = str(conf['bot']['host'])
port = int(conf['bot']['port'])
su_admin = int(conf['bot']['su_admin'])
use_plugins = bool(conf['bot']['use_plugins'])


# bili_push
timeout = int(conf['bili_push']['timeout'])
push_status = int(conf['bili_push']['push_status'])


def set_push_status(num):
    conf.remove_option("bili_push", "push_status")
    conf.set("bili_push", "push_status", num)
    # conf.remove_section("mq")
    with open(file, "w+") as f:
        conf.write(f)


def get_push_status():
    conf.read(file, encoding="utf-8")
    ps = int(conf['bili_push']['push_status'])
    return ps

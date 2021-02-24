from botoy import decorators as deco
from botoy import Botoy, GroupMsg
from botoy import Action
from modules import bot_config


action = Action(qq=bot_config.bot_qq, host=bot_config.host, port=bot_config.port)


bot = Botoy(qq=bot_config.bot_qq,
            host=bot_config.host,
            port=bot_config.port,
            log=False,
            use_plugins=bot_config.use_plugins)


@bot.on_group_msg
@deco.from_these_users(364988395)
@deco.queued_up(name="manage_plugin")
def manage_plugin(ctx: GroupMsg):
    c = ctx.Content
    if c == "插件管理":
        action.sendGroupText(
            ctx.FromGroupId,
            (
                "插件列表 => 发送启用插件列表\n"
                "已停用插件 => 发送停用插件列表\n"
                "刷新所有插件 => 刷新所有插件,包括新建文件\n"
                "重载插件+插件名 => 重载指定插件\n"
                "停用插件+插件名 => 停用指定插件\n"
                "启用插件+插件名 => 启用指定插件\n"
            ),
        )
        return
    # 发送启用插件列表
    if c == "插件列表":
        action.sendGroupText(ctx.FromGroupId, "\n".join(bot.plugins))
        return
    # 发送停用插件列表
    if c == "已停用插件":
        action.sendGroupText(ctx.FromGroupId, "\n".join(bot.removed_plugins))
        return
    try:
        if c == "刷新所有插件":
            bot.reload_plugins()
            action.sendGroupText(ctx.FromGroupId, "操作成功")
        # 重载指定插件 重载py插件+[插件名]
        elif c.startswith("重载插件"):
            plugin_name = c[4:]
            bot.reload_plugin(plugin_name)
            action.sendGroupText(ctx.FromGroupId, "操作成功")
        # 停用指定插件 停用py插件+[插件名]
        elif c.startswith("停用插件"):
            plugin_name = c[4:]
            bot.remove_plugin(plugin_name)
            action.sendGroupText(ctx.FromGroupId, "操作成功")
        # 启用指定插件 启用py插件+[插件名]
        elif c.startswith("启用插件"):
            plugin_name = c[4:]
            bot.recover_plugin(plugin_name)
            action.sendGroupText(ctx.FromGroupId, "操作成功")
    except Exception as e:
        action.sendGroupText(ctx.FromGroupId, "操作失败: %s" % e)


@bot.on_group_msg
@deco.ignore_botself
@deco.queued_up(name="nemu")
def menu(ctx: GroupMsg):
    menu = ctx.Content
    if menu == "菜单":
        action.sendGroupText(ctx.FromGroupId, "1.B站动态订阅推送 <= “推送”\n"
                                              "2.B站用户查询 <= “查询uid”+uid\n"
                                              "3.B站动态浏览 <= “最新动态n条(空格)”+uid\n"
                                              "4.视频解析")


if __name__ == '__main__':
    bot.run()

# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.


from .. import udB

try:
    eval(udB.get("BOTCHAT"))
except BaseException:
    udB.set("BOTCHAT", "{}")


def add_stuff(msg_id, user_id):
    ok = eval(udB.get("BOTCHAT"))
    ok.update({msg_id: user_id})
    udB.set("BOTCHAT", str(ok))


def get_who(msg_id):
    ok = eval(udB.get("BOTCHAT"))
    try:
        user = ok.get(msg_id)
        return user
    except BaseException:
        return

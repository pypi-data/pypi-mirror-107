# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.

from .. import udB

try:
    eval(udB.get("ECHO"))
except BaseException:
    udB.set("ECHO", "{}")


def add_echo(chat, user):
    x = eval(udB.get("ECHO"))
    try:
        k = x[chat]
        if user not in k:
            k.append(user)
        x.update({chat: k})
    except BaseException:
        x.update({chat: [user]})
    return udB.set("ECHO", str(x))


def rem_echo(chat, user):
    x = eval(udB.get("ECHO"))
    try:
        k = x[chat]
        if user in k:
            k.remove(user)
        x.update({chat: k})
    except BaseException:
        pass
    return udB.set("ECHO", str(x))


def check_echo(chat, user):
    x = eval(udB.get("ECHO"))
    try:
        k = x[chat]
        if user in k:
            return True
        return
    except BaseException:
        return


def list_echo(chat):
    x = eval(udB.get("ECHO"))
    try:
        k = x[chat]
        return k
    except BaseException:
        return

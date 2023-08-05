# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.

from .. import udB


def add_goodbye(chat, msg, media):
    x = {"goodbye": msg, "media": media}
    return udB.set(f"{chat}_99", str(x))


def get_goodbye(chat):
    wl = udB.get(f"{chat}_99")
    if wl:
        x = eval(wl)
        return x
    else:
        return


def delete_goodbye(chat):
    return udB.delete(f"{chat}_99")

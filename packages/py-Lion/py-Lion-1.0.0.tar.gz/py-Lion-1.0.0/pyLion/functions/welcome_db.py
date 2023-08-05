# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.

from .. import udB


def add_welcome(chat, msg, media):
    x = {"welcome": msg, "media": media}
    return udB.set(f"{chat}_100", str(x))


def get_welcome(chat):
    wl = udB.get(f"{chat}_100")
    if wl:
        x = eval(wl)
        return x
    else:
        return


def delete_welcome(chat):
    return udB.delete(f"{chat}_100")

# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.

from .. import udB


def is_clean_added(chat):
    k = udB.get("CLEANCHAT")
    if k:
        if str(chat) in k:
            return True
        return
    return


def add_clean(chat):
    if not is_clean_added(chat):
        k = udB.get("CLEANCHAT")
        if k:
            return udB.set("CLEANCHAT", k + " " + str(chat))
        return udB.set("CLEANCHAT", str(chat))
    return


def rem_clean(chat):
    if is_clean_added(chat):
        k = udB.get("CLEANCHAT")
        udB.set("CLEANCHAT", k.replace(str(chat), ""))
        return True
    return

# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.

import ast

from . import udB


def get_chats():
    n = []
    cha = udB.get("FORCESUB")
    if not cha:
        cha = "{}"
    n.append(ast.literal_eval(cha))
    return n[0]


def add_forcesub(chat_id, chattojoin):
    omk = get_chats()
    omk.update({str(chat_id): str(chattojoin)})
    udB.set("FORCESUB", str(omk))
    return True


def get_forcesetting(chat_id):
    omk = get_chats()
    if str(chat_id) in omk.keys():
        return omk[str(chat_id)]
    else:
        return None


def rem_forcesub(chat_id):
    omk = get_chats()
    if str(chat_id) in omk.keys():
        try:
            del omk[str(chat_id)]
            udB.set("FORCESUB", str(omk))
            return True
        except KeyError:
            return False
    else:
        return None

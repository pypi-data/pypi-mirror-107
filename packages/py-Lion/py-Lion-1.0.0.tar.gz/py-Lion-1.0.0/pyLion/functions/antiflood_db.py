# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.

import ast

from .. import udB


def get_flood():
    if udB.get("ANTIFLOOD"):
        n = []
        n.append(ast.literal_eval(udB.get("ANTIFLOOD")))
        return n[0]
    else:
        return {}


def set_flood(chat_id, limit):
    omk = get_flood()
    omk[str(chat_id)] = str(limit)
    udB.set("ANTIFLOOD", str(omk))
    return True


def get_flood_limit(chat_id):
    omk = get_flood()
    if str(chat_id) in omk.keys():
        return omk[str(chat_id)]
    else:
        return None


def rem_flood(chat_id):
    omk = get_flood()
    if str(chat_id) in omk.keys():
        try:
            del omk[str(chat_id)]
            udB.set("ANTIFLOOD", str(omk))
            return True
        except KeyError:
            return False
    else:
        return None

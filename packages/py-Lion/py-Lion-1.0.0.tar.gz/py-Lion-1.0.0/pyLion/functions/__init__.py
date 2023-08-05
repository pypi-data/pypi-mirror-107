# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.

from pyLion import *

from ..dB.database import Var

DANGER = [
    "SESSION",
    "HEROKU_API",
    "base64",
    "bash",
    "get_me()",
    "phone",
    "REDIS_PASSWORD",
    "load_addons",
    "load_plugins",
    "os.system",
    "sys.stdout",
    "sys.stderr",
    "subprocess",
]

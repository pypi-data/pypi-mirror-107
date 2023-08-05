# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.

from sys import *

from telethon import *

from . import *


def load_plugins(plugin_name):
    if plugin_name.startswith("__"):
        pass
    elif plugin_name.endswith("_"):
        import importlib
        from pathlib import Path

        path = Path(f"plugins/{plugin_name}.py")
        name = "plugins.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        import importlib
        import sys
        from pathlib import Path

        from . import HNDLR, LOGS, udB, Lion_bot
        from .dB.database import Var
        from .misc import _supporter as xxx
        from .misc._assistant import (
            asst_cmd,
            callback,
            in_pattern,
            inline,
            inline_owner,
            owner,
        )
        from .misc._decorators import Lion_cmd
        from .misc._wrappers import eod, eor

        path = Path(f"plugins/{plugin_name}.py")
        name = "plugins.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.asst = Lion_bot.asst
        mod.tgbot = Lion_bot.asst
        mod.Lion_bot = Lion_bot
        mod.bot = Lion_bot
        mod.Lion = Lion_bot
        mod.owner = owner()
        mod.in_owner = inline_owner()
        mod.inline = inline()
        mod.in_pattern = in_pattern
        mod.eod = eod
        mod.edit_delete = eod
        mod.LOGS = LOGS
        mod.hndlr = HNDLR
        mod.HNDLR = HNDLR
        mod.Var = Var
        mod.eor = eor
        mod.edit_or_reply = eor
        mod.asst_cmd = asst_cmd
        mod.Lion_cmd = Lion_cmd
        mod.on_cmd = Lion_cmd
        mod.callback = callback
        mod.Redis = udB.get
        sys.modules["support"] = xxx
        sys.modules["userbot"] = xxx
        sys.modules["userbot.utils"] = xxx
        sys.modules["userbot.config"] = xxx
        spec.loader.exec_module(mod)
        sys.modules["plugins." + plugin_name] = mod
        if not plugin_name.startswith("_"):
            try:
                PLUGINS.append(plugin_name)
            except BaseException:
                if plugin_name not in PLUGINS:
                    PLUGINS.append(plugin_name)
                else:
                    pass


# for addons


def load_addons(plugin_name):
    if plugin_name.startswith("__"):
        pass
    elif plugin_name.endswith("_"):
        import importlib
        from pathlib import Path

        path = Path(f"addons/{plugin_name}.py")
        name = "addons.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        import importlib
        import sys
        from pathlib import Path

        from . import HNDLR, LOGS, udB, Lion_bot
        from .dB.database import Var
        from .misc import _supporter as xxx
        from .misc._assistant import (
            asst_cmd,
            callback,
            in_pattern,
            inline,
            inline_owner,
            owner,
        )
        from .misc._decorators import Lion_cmd
        from .misc._supporter import Config, admin_cmd, sudo_cmd
        from .misc._wrappers import eod, eor

        path = Path(f"addons/{plugin_name}.py")
        name = "addons.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.asst = Lion_bot.asst
        mod.tgbot = Lion_bot.asst
        mod.Lion_bot = Lion_bot
        mod.ub = Lion_bot
        mod.bot = Lion_bot
        mod.Lion = Lion_bot
        mod.borg = Lion_bot
        mod.telebot = Lion_bot
        mod.jarvis = Lion_bot
        mod.friday = Lion_bot
        mod.owner = owner()
        mod.in_owner = inline_owner()
        mod.inline = inline()
        mod.eod = eod
        mod.edit_delete = eod
        mod.LOGS = LOGS
        mod.in_pattern = in_pattern
        mod.hndlr = HNDLR
        mod.handler = HNDLR
        mod.HNDLR = HNDLR
        mod.CMD_HNDLR = HNDLR
        mod.Config = Config
        mod.Var = Var
        mod.eor = eor
        mod.edit_or_reply = eor
        mod.asst_cmd = asst_cmd
        mod.Lion_cmd = Lion_cmd
        mod.on_cmd = Lion_cmd
        mod.callback = callback
        mod.Redis = udB.get
        mod.admin_cmd = admin_cmd
        mod.sudo_cmd = sudo_cmd
        sys.modules["ub"] = xxx
        sys.modules["var"] = xxx
        sys.modules["jarvis"] = xxx
        sys.modules["support"] = xxx
        sys.modules["userbot"] = xxx
        sys.modules["telebot"] = xxx
        sys.modules["fridaybot"] = xxx
        sys.modules["jarvis.utils"] = xxx
        sys.modules["uniborg.util"] = xxx
        sys.modules["telebot.utils"] = xxx
        sys.modules["userbot.utils"] = xxx
        sys.modules["userbot.events"] = xxx
        sys.modules["jarvis.jconfig"] = xxx
        sys.modules["userbot.config"] = xxx
        sys.modules["fridaybot.utils"] = xxx
        sys.modules["fridaybot.Config"] = xxx
        sys.modules["userbot.uniborgConfig"] = xxx
        spec.loader.exec_module(mod)
        sys.modules["addons." + plugin_name] = mod
        if not plugin_name.startswith("_"):
            try:
                ADDONS.append(plugin_name)
            except BaseException:
                if plugin_name not in ADDONS:
                    ADDONS.append(plugin_name)
                else:
                    pass


# for assistant


def load_assistant(plugin_name):
    if plugin_name.startswith("__"):
        pass
    elif plugin_name.endswith("_"):
        import importlib
        from pathlib import Path

        path = Path(f"assistant/{plugin_name}.py")
        name = "assistant.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        import importlib
        import sys
        from pathlib import Path

        from . import HNDLR, udB, Lion_bot
        from .misc._assistant import asst_cmd, callback, in_pattern, inline_owner, owner
        from .misc._wrappers import eod, eor

        path = Path(f"assistant/{plugin_name}.py")
        name = "assistant.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.Lion_bot = Lion_bot
        mod.Lion = Lion_bot
        mod.Redis = udB.get
        mod.udB = udB
        mod.bot = Lion_bot
        mod.asst = Lion_bot.asst
        mod.owner = owner()
        mod.in_pattern = in_pattern
        mod.in_owner = inline_owner()
        mod.eod = eod
        mod.eor = eor
        mod.callback = callback
        mod.hndlr = HNDLR
        mod.HNDLR = HNDLR
        mod.asst_cmd = asst_cmd
        spec.loader.exec_module(mod)
        sys.modules["assistant." + plugin_name] = mod


# msg forwarder


def load_pmbot(plugin_name):
    if plugin_name.startswith("__"):
        pass
    elif plugin_name.endswith("_"):
        import importlib
        from pathlib import Path

        path = Path(f"assistant/pmbot/{plugin_name}.py")
        name = "assistant.pmbot.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        import importlib
        import sys
        from pathlib import Path

        from . import HNDLR, udB, Lion_bot
        from .misc._assistant import asst_cmd, callback, owner
        from .misc._wrappers import eod, eor

        path = Path(f"assistant/pmbot/{plugin_name}.py")
        name = "assistant.pmbot.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.Lion_bot = Lion_bot
        mod.Lion = Lion_bot
        mod.bot = Lion_bot
        mod.Redis = udB.get
        mod.udB = udB
        mod.asst = Lion_bot.asst
        mod.owner = owner()
        mod.eod = eod
        mod.eor = eor
        mod.callback = callback
        mod.hndlr = HNDLR
        mod.HNDLR = HNDLR
        mod.asst_cmd = asst_cmd
        spec.loader.exec_module(mod)
        sys.modules["assistant.pmbot" + plugin_name] = mod

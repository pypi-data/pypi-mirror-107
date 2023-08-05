# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.

import asyncio
import glob
import os
import traceback
import urllib
from pathlib import Path
from random import randint

import telethon.utils
from telethon import TelegramClient
from telethon import __version__ as vers
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    JoinChannelRequest,
)
from telethon.tl.types import (
    ChatAdminRights,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)

from . import *
from .functions.all import updater
from .utils import *
from .version import __version__ as ver

x = ["resources/auths", "resources/downloads", "addons"]
for x in x:
    if not os.path.isdir(x):
        os.mkdir(x)

if udB.get("CUSTOM_THUMBNAIL"):
    os.system(f"wget {udB.get('CUSTOM_THUMBNAIL')} -O resources/extras/Lion.jpg")

if udB.get("GDRIVE_TOKEN"):
    with open("resources/auths/auth_token.txt", "w") as t_file:
        t_file.write(udB.get("GDRIVE_TOKEN"))


async def autobot():
    await Lion_bot.start()
    if Var.BOT_TOKEN:
        udB.set("BOT_TOKEN", str(Var.BOT_TOKEN))
        return
    LOGS.info("MAKING A TELEGRAM BOT FOR YOU AT @BotFather , Please Kindly Wait")
    who = await Lion_bot.get_me()
    name = who.first_name + "'s Assistant Bot"
    if who.username:
        username = who.username + "_bot"
    else:
        username = "Lion_" + (str(who.id))[5:] + "_bot"
    bf = "Botfather"
    await Lion_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await Lion_bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await Lion_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    await Lion_bot.send_message(bf, name)
    await asyncio.sleep(1)
    await Lion_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await Lion_bot.get_messages(bf, limit=1))[0].text
    await Lion_bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "Lion_" + (str(who.id))[6:] + str(ran) + "_bot"
        await Lion_bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await Lion_bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            udB.set("BOT_TOKEN", token)
            await Lion_bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await Lion_bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await Lion_bot.send_message(bf, "Search")
            LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
        else:
            LOGS.info(
                f"Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
            )
            exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        udB.set("BOT_TOKEN", token)
        await Lion_bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await Lion_bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await Lion_bot.send_message(bf, "Search")
        LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
    else:
        LOGS.info(
            f"Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
        )
        exit(1)


if not udB.get("BOT_TOKEN") and str(BOT_MODE) != "True":
    Lion_bot.loop.run_until_complete(autobot())


async def istart(ult):
    await Lion_bot.start(ult)
    Lion_bot.me = await Lion_bot.get_me()
    Lion_bot.uid = telethon.utils.get_peer_id(Lion_bot.me)
    Lion_bot.first_name = Lion_bot.me.first_name
    if not Lion_bot.me.bot:
        udB.set("OWNER_ID", Lion_bot.uid)
    if str(BOT_MODE) == "True":
        if Var.OWNER_ID:
            OWNER = await Lion_bot.get_entity(Var.OWNER_ID)
            Lion_bot.me = OWNER
            asst.me = OWNER
            Lion_bot.uid = OWNER.id
            Lion_bot.first_name = OWNER.first_name
        elif udB.get("OWNER_ID"):
            OWNER = await Lion_bot.get_entity(int(udB.get("OWNER_ID")))
            Lion_bot.me = OWNER
            asst.me = OWNER
            Lion_bot.uid = OWNER.id
            Lion_bot.first_name = OWNER.first_name


async def autopilot():
    await Lion_bot.start()
    if Var.LOG_CHANNEL and str(Var.LOG_CHANNEL).startswith("-100"):
        udB.set("LOG_CHANNEL", str(Var.LOG_CHANNEL))
    if udB.get("LOG_CHANNEL"):
        try:
            await Lion_bot.get_entity(int(udB.get("LOG_CHANNEL")))
            return
        except BaseException:
            udB.delete("LOG_CHANNEL")
    r = await Lion_bot(
        CreateChannelRequest(
            title="My Lion Logs",
            about="My Lion Log Group\n\n Join @LionXUpdates",
            megagroup=True,
        ),
    )
    chat_id = r.chats[0].id
    if not str(chat_id).startswith("-100"):
        udB.set("LOG_CHANNEL", "-100" + str(chat_id))
    else:
        udB.set("LOG_CHANNEL", str(chat_id))
    rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        anonymous=False,
        manage_call=True,
    )
    await Lion_bot(EditAdminRequest(chat_id, asst.me.username, rights, "Assistant"))
    pfpa = await Lion_bot.download_profile_photo(chat_id)
    if not pfpa:
        urllib.request.urlretrieve(
            "https://telegra.ph/file/950919bfdd8d91b87c551.jpg", "channelphoto.jpg"
        )
        ll = await Lion_bot.upload_file("channelphoto.jpg")
        await Lion_bot(EditPhotoRequest(chat_id, InputChatUploadedPhoto(ll)))
        os.remove("channelphoto.jpg")
    else:
        os.remove(pfpa)


Lion_bot.asst = None


async def bot_info(asst):
    await asst.start()
    asst.me = await asst.get_me()
    return asst.me


LOGS.info("Initialising...")
LOGS.info(f"py-Lion Version - {ver}")
LOGS.info(f"Telethon Version - {vers}")
LOGS.info("Lion Version - 1.0")

if str(BOT_MODE) == "True":
    mode = "Bot Mode - Started"
else:
    mode = "User Mode - Started"

# log in
BOT_TOKEN = udB.get("BOT_TOKEN")
if BOT_TOKEN:
    LOGS.info("Starting Lion-X...")
    try:
        Lion_bot.asst = TelegramClient(
            None, api_id=Var.API_ID, api_hash=Var.API_HASH
        ).start(bot_token=BOT_TOKEN)
        asst = Lion_bot.asst
        Lion_bot.loop.run_until_complete(istart(asst))
        Lion_bot.loop.run_until_complete(bot_info(asst))
        LOGS.info("Done, startup completed")
        LOGS.info(mode)
    except AuthKeyDuplicatedError:
        LOGS.info(
            "Session String expired. Please create a new one! Lion-X is stopping..."
        )
        exit(1)
    except BaseException:
        LOGS.info("Error: " + str(traceback.print_exc()))
        exit(1)
else:
    LOGS.info(mode)
    Lion_bot.start()

BOTINVALID_PLUGINS = [
    "globaltools",
    "autopic",
    "pmpermit",
    "fedutils",
    "_userlogs",
    "webupload",
    "clone",
    "inlinefun",
    "tscan",
    "animedb",
    "limited",
    "quotly",
    "findsong",
    "sticklet",
]

if str(BOT_MODE) != "True":
    Lion_bot.loop.run_until_complete(autopilot())

# for userbot
path = "plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        try:
            if str(BOT_MODE) == "True" and plugin_name in BOTINVALID_PLUGINS:
                LOGS.info(
                    f"Lion - Official - BOT_MODE_INVALID_PLUGIN - {plugin_name}"
                )
            else:
                load_plugins(plugin_name.replace(".py", ""))
                if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                    LOGS.info(f"Lion - Official -  Installed - {plugin_name}")
        except Exception:
            LOGS.info(f"Lion - Official - ERROR - {plugin_name}")
            LOGS.info(str(traceback.print_exc()))


# for addons
addons = udB.get("ADDONS")
if addons == "True" or addons is None:
    try:
        os.system("git clone https://github.com/TeamUltroid/UltroidAddons.git addons/")
    except BaseException:
        pass
    LOGS.info("Installing packages for addons")
    os.system("pip install -r addons/addons.txt")
    path = "addons/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            try:
                if str(BOT_MODE) == "True" and plugin_name in BOTINVALID_PLUGINS:
                    LOGS.info(
                        f"Lion - Addons - BOT_MODE_INVALID_PLUGIN - {plugin_name}"
                    )
                else:
                    load_addons(plugin_name.replace(".py", ""))
                    if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                        LOGS.info(f"Lion - Addons - Installed - {plugin_name}")
            except Exception as e:
                LOGS.info(f"Lion - Addons - ERROR - {plugin_name}")
                LOGS.info(str(e))
else:
    os.system("cp plugins/__init__.py addons/")


# for assistant
path = "assistant/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        try:
            load_assistant(plugin_name.replace(".py", ""))
            if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                LOGS.info(f"Lion - Assistant - Installed - {plugin_name}")
        except Exception as e:
            LOGS.info(f"Lion - Assistant - ERROR - {plugin_name}")
            LOGS.info(str(e))

# for channel plugin
Plug_channel = udB.get("PLUGIN_CHANNEL")
if Plug_channel:

    async def plug():
        if str(BOT_MODE) == "True":
            LOGS.info("PLUGIN_CHANNEL Can't be used in BOT_MODE")
            return
        try:
            if Plug_channel.startswith("@"):
                chat = Plug_channel
            else:
                try:
                    chat = int(Plug_channel)
                except BaseException:
                    return
            async for x in Lion_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument
            ):
                await asyncio.sleep(0.6)
                files = await Lion_bot.download_media(x.media, "./addons/")
                file = Path(files)
                plugin = file.stem
                if "(" not in files:
                    try:
                        load_addons(plugin.replace(".py", ""))
                        LOGS.info(f"Lion - PLUGIN_CHANNEL - Installed - {plugin}")
                    except Exception as e:
                        LOGS.info(f"Lion - PLUGIN_CHANNEL - ERROR - {plugin}")
                        LOGS.info(str(e))
                else:
                    LOGS.info(f"Plugin {plugin} is Pre Installed")
                    os.remove(files)
        except Exception as e:
            LOGS.info(str(e))


# chat via assistant
pmbot = udB.get("PMBOT")
if pmbot == "True":
    path = "assistant/pmbot/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            load_pmbot(plugin_name.replace(".py", ""))
    LOGS.info(f"Lion - PM Bot Message Forwards - Enabled.")

# customize assistant


async def customize():
    try:
        chat_id = int(udB.get("LOG_CHANNEL"))
        xx = await Lion_bot.get_entity(asst.me.username)
        if xx.photo is None:
            LOGS.info("Customising Ur Assistant Bot in @BOTFATHER")
            UL = f"@{asst.me.username}"
            if (Lion_bot.me.username) is None:
                sir = Lion_bot.me.first_name
            else:
                sir = f"@{Lion_bot.me.username}"
            await Lion_bot.send_message(
                chat_id, "Auto Customisation Started on @botfather"
            )
            await asyncio.sleep(1)
            await Lion_bot.send_message("botfather", "/cancel")
            await asyncio.sleep(1)
            await Lion_bot.send_message("botfather", "/start")
            await asyncio.sleep(1)
            await Lion_bot.send_message("botfather", "/setuserpic")
            await asyncio.sleep(1)
            await Lion_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await Lion_bot.send_file(
                "botfather", "resources/extras/Lion_assistant.jpg"
            )
            await asyncio.sleep(2)
            await Lion_bot.send_message("botfather", "/setabouttext")
            await asyncio.sleep(1)
            await Lion_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await Lion_bot.send_message(
                "botfather", f"✨ Hello ✨!! I'm Assistant Bot of {sir}"
            )
            await asyncio.sleep(2)
            await Lion_bot.send_message("botfather", "/setdescription")
            await asyncio.sleep(1)
            await Lion_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await Lion_bot.send_message(
                "botfather",
                f"✨ PowerFul Lion Assistant Bot ✨\n✨ Master ~ {sir} ✨\n\n✨ Powered By ~ @LionXUpdates ✨",
            )
            await asyncio.sleep(2)
            await Lion_bot.send_message("botfather", "/start")
            await asyncio.sleep(1)
            await Lion_bot.send_message(
                chat_id, "**Auto Customisation** Done at @BotFather"
            )
            LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.warning(str(e))


# some stuffs
async def ready():
    try:
        chat_id = int(udB.get("LOG_CHANNEL"))
        MSG = f"**Lion-X has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{Lion_bot.me.first_name}](tg://user?id={Lion_bot.me.id})\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖\n**Support**: @LionXUpdates\n➖➖➖➖➖➖➖➖➖"
        BTTS = None
        updava = await updater()
        if updava:
            BTTS = [[Button.inline(text="Update Available", data="updtavail")]]
        await Lion_bot.asst.send_message(chat_id, MSG, buttons=BTTS)
    except BaseException:
        try:
            MSG = f"**Lion-X has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{Lion_bot.me.first_name}](tg://user?id={Lion_bot.me.id})\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖\n**Support**: @LionXUpdates\n➖➖➖➖➖➖➖➖➖"
            await Lion_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.info(ef)
    try:
        # To Let Them know About New Updates and Changes
        await Lion_bot(JoinChannelRequest("@LionXUpdates"))
    except BaseException:
        pass


if Var.HEROKU_APP_NAME:
    ws = f"WEBSOCKET_URL=https://{Var.HEROKU_APP_NAME}.herokuapp.com"
else:
    ws = f"WEBSOCKET_URL=127.0.0.1"
lg = f"LOG_CHANNEL={udB.get('LOG_CHANNEL')}"
bt = f"BOT_TOKEN={udB.get('BOT_TOKEN')}"
try:
    with open(".env", "r") as x:
        m = x.read()
    if "WEBSOCKET_URL" not in m:
        with open(".env", "a+") as t:
            t.write("\n" + ws)
    if "LOG_CHANNEL" not in m:
        with open(".env", "a+") as t:
            t.write("\n" + lg)
    if "BOT_TOKEN" not in m:
        with open(".env", "a+") as t:
            t.write("\n" + bt)
except BaseException:
    with open(".env", "w") as t:
        t.write(ws + "\n" + lg + "\n" + bt)


if str(BOT_MODE) != "True":
    Lion_bot.loop.run_until_complete(customize())
    if Plug_channel:
        Lion_bot.loop.run_until_complete(plug())
Lion_bot.loop.run_until_complete(ready())

LOGS.info(
    """
                ----------------------------------------------------------------------
                    Lion-X has been deployed! Visit @LionXUpdates for updates!!
                ----------------------------------------------------------------------
"""
)

if __name__ == "__main__":
    Lion_bot.run_until_disconnected()

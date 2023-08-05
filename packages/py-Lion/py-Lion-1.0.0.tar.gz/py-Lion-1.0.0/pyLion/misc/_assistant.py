# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.


import functools

from telethon import *
from telethon import events
from telethon.tl.types import InputWebDocument
from telethon.utils import get_display_name

from .. import *
from ..dB.core import *
from ..utils import *
from ._decorators import sed

OWNER_NAME = Lion_bot.me.first_name
OWNER_ID = Lion_bot.me.id
Lion_PIC = "https://telegra.ph/file/950919bfdd8d91b87c551.jpg"
MSG = f"""
**Lion - UserBot**
➖➖➖➖➖➖➖➖➖➖
**Owner**: [{get_display_name(Lion_bot.me)}](tg://user?id={Lion_bot.me.id})
**Support**: @LionXUpdates
➖➖➖➖➖➖➖➖➖➖
"""

# decorator for assistant


def inline_owner():
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(event):
            if event.sender_id in sed:
                try:
                    await function(event)
                except BaseException:
                    pass
            else:
                try:
                    builder = event.builder
                    sur = builder.article(
                        title="Lion Userbot",
                        url="https://t.me/LionXUpdates",
                        description="(c) TeamLion",
                        text=MSG,
                        thumb=InputWebDocument(Lion_PIC, 0, "image/jpeg", []),
                        buttons=[
                            [
                                Button.url(
                                    "Repository",
                                    url="https://github.com/TeamLion/Lion-X",
                                ),
                                Button.url(
                                    "Support", url="https://t.me/LionXUpdates"
                                ),
                            ]
                        ],
                    )
                    await event.answer(
                        [sur],
                        switch_pm=f"🤖: Assistant of {OWNER_NAME}",
                        switch_pm_param="start",
                    )
                except BaseException:
                    pass

        return wrapper

    return decorator


def asst_cmd(dec):
    def ult(func):
        pattern = "^/" + dec  # todo - handlers for assistant?
        Lion_bot.asst.add_event_handler(
            func, events.NewMessage(incoming=True, pattern=pattern)
        )

    return ult


def callback(sed):
    def ultr(func):
        data = sed
        Lion_bot.asst.add_event_handler(
            func, events.callbackquery.CallbackQuery(data=data)
        )

    return ultr


def inline():
    def ultr(func):
        Lion_bot.asst.add_event_handler(func, events.InlineQuery)

    return ultr


def in_pattern(pat):
    def don(func):
        pattern = pat
        Lion_bot.asst.add_event_handler(func, events.InlineQuery(pattern=pattern))

    return don


# check for owner
def owner():
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(event):
            if event.sender_id in sed:
                await function(event)
            else:
                try:
                    await event.answer(f"This is {OWNER_NAME}'s bot!!")
                except BaseException:
                    pass

        return wrapper

    return decorator

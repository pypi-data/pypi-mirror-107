# py-Lion Library
A stable userbot base library, based on Telethon.

[![PyPI - Version](https://img.shields.io/pypi/v/py-Lion?style=for-the-badge)](https://pypi.org/project/py-Lion)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py-Lion?label=DOWNLOADS&style=for-the-badge)](https://pypi.org/project/py-Lion)

## Installation
`pip install py-Lion`

## Usage
=> Create folders named `plugins`, `addons`, `assistant` and `resources`.<br/>
=> Add your plugins in the `plugins` folder and others accordingly.<br/>
=> Create a `.env` file with `API_ID`, `API_HASH`, `SESSION`, 
`BOT_TOKEN`, `BOT_USERNAME`, `REDIS_URI`, `REDIS_PASSWORD` & 
`LOG_CHANNEL` as mandatory environment variables. Check
[`.env.sample`](https://github.com/TeamLion-X/Lion-x/.env.sample) for more details.<br/>
=> Run `python -m pyLion` to start the bot.<br/>

### Creating plugins
To work everywhere

```python
@Lion_cmd(
    pattern="start",
)   
async def _(e):   
    await eor(e, "Lion Started")   
```

To work only in groups

```python
@Lion_cmd(
    pattern="start",
    groups_only=True,
)   
async def _(e):   
    await eor(e, "Lion Started")   
```

Assistant Plugins 👇

```python
@asst_cmd("start")   
async def _(e):   
    await e.reply("Lion Started")   
```

Made with 💕 by [@TeamLion](https://github.com/TeamLion-X/Lion-x). <br />

# Credits
* [Lonami](https://github.com/LonamiWebs/) for [Telethon](https://github.com/LonamiWebs/Telethon)

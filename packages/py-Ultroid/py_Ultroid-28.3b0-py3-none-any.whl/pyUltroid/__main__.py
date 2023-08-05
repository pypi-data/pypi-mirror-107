# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

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
from telethon.errors.rpcerrorlist import (
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
    PhoneNumberInvalidError,
)
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
    os.system(f"wget {udB.get('CUSTOM_THUMBNAIL')} -O resources/extras/ultroid.jpg")

if udB.get("GDRIVE_TOKEN"):
    with open("resources/auths/auth_token.txt", "w") as t_file:
        t_file.write(udB.get("GDRIVE_TOKEN"))


async def autobot():
    await ultroid_bot.start()
    if Var.BOT_TOKEN:
        udB.set("BOT_TOKEN", str(Var.BOT_TOKEN))
        return
    LOGS.info("MAKING A TELEGRAM BOT FOR YOU AT @BotFather , Please Kindly Wait")
    who = await ultroid_bot.get_me()
    name = who.first_name + "'s Assistant Bot"
    if who.username:
        username = who.username + "_bot"
    else:
        username = "ultroid_" + (str(who.id))[5:] + "_bot"
    bf = "Botfather"
    await ultroid_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await ultroid_bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await ultroid_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    await ultroid_bot.send_message(bf, name)
    await asyncio.sleep(1)
    await ultroid_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
    await ultroid_bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "ultroid_" + (str(who.id))[6:] + str(ran) + "_bot"
        await ultroid_bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            udB.set("BOT_TOKEN", token)
            await ultroid_bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await ultroid_bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await ultroid_bot.send_message(bf, "Search")
            LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
        else:
            LOGS.info(
                f"Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
            )
            exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        udB.set("BOT_TOKEN", token)
        await ultroid_bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await ultroid_bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await ultroid_bot.send_message(bf, "Search")
        LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
    else:
        LOGS.info(
            f"Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
        )
        exit(1)


if not udB.get("BOT_TOKEN") and str(BOT_MODE) != "True":
    ultroid_bot.loop.run_until_complete(autobot())


async def istart(ult):
    await ultroid_bot.start(ult)
    ultroid_bot.me = await ultroid_bot.get_me()
    ultroid_bot.uid = telethon.utils.get_peer_id(ultroid_bot.me)
    ultroid_bot.first_name = ultroid_bot.me.first_name
    if not ultroid_bot.me.bot:
        udB.set("OWNER_ID", ultroid_bot.uid)
    if str(BOT_MODE) == "True":
        if Var.OWNER_ID:
            OWNER = await ultroid_bot.get_entity(Var.OWNER_ID)
            ultroid_bot.me = OWNER
            asst.me = OWNER
            ultroid_bot.uid = OWNER.id
            ultroid_bot.first_name = OWNER.first_name
        elif udB.get("OWNER_ID"):
            OWNER = await ultroid_bot.get_entity(int(udB.get("OWNER_ID")))
            ultroid_bot.me = OWNER
            asst.me = OWNER
            ultroid_bot.uid = OWNER.id
            ultroid_bot.first_name = OWNER.first_name


async def autopilot():
    await ultroid_bot.start()
    if Var.LOG_CHANNEL and str(Var.LOG_CHANNEL).startswith("-100"):
        udB.set("LOG_CHANNEL", str(Var.LOG_CHANNEL))
    if udB.get("LOG_CHANNEL"):
        try:
            await ultroid_bot.get_entity(int(udB.get("LOG_CHANNEL")))
            return
        except BaseException:
            udB.delete("LOG_CHANNEL")
    r = await ultroid_bot(
        CreateChannelRequest(
            title="My Ultroid Logs",
            about="My Ultroid Log Group\n\n Join @TeamUltroid",
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
    await ultroid_bot(EditAdminRequest(chat_id, asst.me.username, rights, "Assistant"))
    pfpa = await ultroid_bot.download_profile_photo(chat_id)
    if not pfpa:
        urllib.request.urlretrieve(
            "https://telegra.ph/file/bac3a1c21912a7b35c797.jpg", "channelphoto.jpg"
        )
        ll = await ultroid_bot.upload_file("channelphoto.jpg")
        await ultroid_bot(EditPhotoRequest(chat_id, InputChatUploadedPhoto(ll)))
        os.remove("channelphoto.jpg")
    else:
        os.remove(pfpa)


ultroid_bot.asst = None


async def bot_info(asst):
    await asst.start()
    asst.me = await asst.get_me()
    return asst.me


LOGS.info("Initialising...")
LOGS.info(f"py-Ultroid Version - {ver}")
LOGS.info(f"Telethon Version - {vers}")
LOGS.info("Ultroid Version - 0.0.7")

if str(BOT_MODE) == "True":
    mode = "Bot Mode - Started"
else:
    mode = "User Mode - Started"

# log in
BOT_TOKEN = udB.get("BOT_TOKEN")
if BOT_TOKEN:
    LOGS.info("Starting Ultroid...")
    try:
        ultroid_bot.asst = TelegramClient(
            None, api_id=Var.API_ID, api_hash=Var.API_HASH
        ).start(bot_token=BOT_TOKEN)
        asst = ultroid_bot.asst
        ultroid_bot.loop.run_until_complete(istart(asst))
        ultroid_bot.loop.run_until_complete(bot_info(asst))
        LOGS.info("Done, startup completed")
        LOGS.info(mode)
    except AuthKeyDuplicatedError or PhoneNumberInvalidError:
        LOGS.info(
            "Session String expired. Please create a new one! Ultroid is stopping..."
        )
        exit(1)
    except ApiIdInvalidError:
        LOGS.info("Your API ID/API HASH combination is invalid. Kindly recheck.")
        exit(1)
    except BaseException:
        LOGS.info("Error: " + str(traceback.print_exc()))
        exit(1)
else:
    LOGS.info(mode)
    ultroid_bot.start()

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
    ultroid_bot.loop.run_until_complete(autopilot())

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
                    f"Ultroid - Official - BOT_MODE_INVALID_PLUGIN - {plugin_name}"
                )
            else:
                load_plugins(plugin_name.replace(".py", ""))
                if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                    LOGS.info(f"Ultroid - Official -  Installed - {plugin_name}")
        except Exception:
            LOGS.info(f"Ultroid - Official - ERROR - {plugin_name}")
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
                        f"Ultroid - Addons - BOT_MODE_INVALID_PLUGIN - {plugin_name}"
                    )
                else:
                    load_addons(plugin_name.replace(".py", ""))
                    if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                        LOGS.info(f"Ultroid - Addons - Installed - {plugin_name}")
            except Exception as e:
                LOGS.info(f"Ultroid - Addons - ERROR - {plugin_name}")
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
                LOGS.info(f"Ultroid - Assistant - Installed - {plugin_name}")
        except Exception as e:
            LOGS.info(f"Ultroid - Assistant - ERROR - {plugin_name}")
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
            async for x in ultroid_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument
            ):
                await asyncio.sleep(0.6)
                files = await ultroid_bot.download_media(x.media, "./addons/")
                file = Path(files)
                plugin = file.stem
                if "(" not in files:
                    try:
                        load_addons(plugin.replace(".py", ""))
                        LOGS.info(f"Ultroid - PLUGIN_CHANNEL - Installed - {plugin}")
                    except Exception as e:
                        LOGS.info(f"Ultroid - PLUGIN_CHANNEL - ERROR - {plugin}")
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
    LOGS.info(f"Ultroid - PM Bot Message Forwards - Enabled.")

# customize assistant


async def customize():
    try:
        chat_id = int(udB.get("LOG_CHANNEL"))
        xx = await ultroid_bot.get_entity(asst.me.username)
        if xx.photo is None:
            LOGS.info("Customising Ur Assistant Bot in @BOTFATHER")
            UL = f"@{asst.me.username}"
            if (ultroid_bot.me.username) is None:
                sir = ultroid_bot.me.first_name
            else:
                sir = f"@{ultroid_bot.me.username}"
            await ultroid_bot.send_message(
                chat_id, "Auto Customisation Started on @botfather"
            )
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/cancel")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/start")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/setuserpic")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_file(
                "botfather", "resources/extras/ultroid_assistant.jpg"
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/setabouttext")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                "botfather", f"✨ Hello ✨!! I'm Assistant Bot of {sir}"
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/setdescription")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                "botfather",
                f"✨ PowerFul Ultroid Assistant Bot ✨\n✨ Master ~ {sir} ✨\n\n✨ Powered By ~ @TeamUltroid ✨",
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/start")
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                chat_id, "**Auto Customisation** Done at @BotFather"
            )
            LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.warning(str(e))


# some stuffs
async def ready():
    try:
        chat_id = int(udB.get("LOG_CHANNEL"))
        MSG = f"**Ultroid has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.me.id})\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖\n**Support**: @TeamUltroid\n➖➖➖➖➖➖➖➖➖"
        BTTS = None
        updava = await updater()
        if updava:
            BTTS = [[Button.inline(text="Update Available", data="updtavail")]]
        await ultroid_bot.asst.send_message(chat_id, MSG, buttons=BTTS)
    except BaseException:
        try:
            MSG = f"**Ultroid has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.me.id})\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖\n**Support**: @TeamUltroid\n➖➖➖➖➖➖➖➖➖"
            await ultroid_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.info(ef)
    try:
        # To Let Them know About New Updates and Changes
        await ultroid_bot(JoinChannelRequest("@TheUltroid"))
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
    ultroid_bot.loop.run_until_complete(customize())
    if Plug_channel:
        ultroid_bot.loop.run_until_complete(plug())
ultroid_bot.loop.run_until_complete(ready())

LOGS.info(
    """
                ----------------------------------------------------------------------
                    Ultroid has been deployed! Visit @TheUltroid for updates!!
                ----------------------------------------------------------------------
"""
)

if __name__ == "__main__":
    ultroid_bot.run_until_disconnected()

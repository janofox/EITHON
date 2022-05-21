import random
import re
from datetime import datetime
import asyncio
import pyfiglet
import asyncio
import calendar
import json
import os
from telethon.errors import ChatSendInlineForbiddenError, ChatSendStickersForbiddenError
from telethon import Button, functions
from telethon import events
from telethon.events import CallbackQuery
from telethon.utils import get_display_name
from asyncio.exceptions import TimeoutError
from bs4 import BeautifulSoup
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ExportChatInviteRequest
from collections import deque
from random import choice
from userbot import iqthon
from userbot.core.logger import logging
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id, _catutils, parse_pre, yaml_format, install_pip, get_user_from_event, _format
from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper import pmpermit_sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers import get_user_from_event, sanga_seperator
from . import mention
from . import ALIVE_NAME, PM_START, PMMENU, PMMESSAGE_CACHE, check, get_user_from_event, parse_pre, set_key
from datetime import datetime
from urllib.parse import quote
import barcode
import qrcode
import requests
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from PIL import Image, ImageColor
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.utils import admin_cmd
from ..helpers import AioHttp
from ..helpers.utils import _catutils, _format, reply_id
CACHE = {}
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER
async def do_pm_permit_action(event, chat):  
    reply_to_id = await reply_id(event)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    me = await event.client.get_me()
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    if str(chat.id) not in PM_WARNS:
        PM_WARNS[str(chat.id)] = 0
    try:
        MAX_FLOOD_IN_PMS = int(gvarstatus("MAX_FLOOD_IN_PMS") or 10)
    except (ValueError, TypeError):
        MAX_FLOOD_IN_PMS = 10
    totalwarns = MAX_FLOOD_IN_PMS + 1
    warns = PM_WARNS[str(chat.id)] + 1
    remwarns = totalwarns - warns
    if PM_WARNS[str(chat.id)] >= MAX_FLOOD_IN_PMS:
        try:
            if str(chat.id) in PMMESSAGE_CACHE:
                await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
                del PMMESSAGE_CACHE[str(chat.id)]
        except Exception as e:
            LOGS.info(str(e))
        custompmblock = gvarstatus("pmblock") or None
        if custompmblock is not None:
            USER_BOT_WARN_ZERO = custompmblock.format(mention=mention, first=first, last=last, fullname=fullname, username=username, userid=userid, my_first=my_first, my_last=my_last, my_fullname=my_fullname, my_username=my_username, my_mention=my_mention, totalwarns=totalwarns, warns=warns, remwarns=remwarns)
        else:
            USER_BOT_WARN_ZERO = f"**𓆩𓆩ꕥ ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن الـتـڪـرار . تـم حـظـرڪ ، لا يـمـڪـنـڪ ازعـاج الـمـالـڪ !𓆪𓆪**"
        msg = await event.reply(USER_BOT_WARN_ZERO)
        await event.client(functions.contacts.BlockRequest(chat.id))
        the_message = f"**ꕥ ⦙  الـمـحـضـوريـن مـن الـخـاص : 📩**\n𖠄 ⦙   [{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .🚫** \n**𖠒 ⦙   عـدد الـرسـائـل :** {PM_WARNS[str(chat.id)]}"
        del PM_WARNS[str(chat.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
        try:
            return await event.client.send_message(BOTLOG_CHATID,the_message)
        except BaseException:
            return
    custompmpermit = gvarstatus("pmpermit_txt") or None
    if custompmpermit is not None:
        USER_BOT_NO_WARN = custompmpermit.format(mention=mention,first=first,last=last,fullname=fullname,username=username,userid=userid,my_first=my_first,my_last=my_last,my_fullname=my_fullname,my_username=my_username,my_mention=my_mention,totalwarns=totalwarns,warns=warns,remwarns=remwarns)
    elif gvarstatus("pmmenu") is None:
        USER_BOT_NO_WARN = f"⩹┉┉┉┉⊶❲𓆩⸤Ξ𝗜𝗧𝗛𝗢𝗡⸥𓆪❳⊷┉┉┉┉⩺\n\n❞ هـاﺂ هـݪـو٘ {mention} ❝ 𖠄\nاﻧـا آݪان ﻣـﺷـغٓول ݪاتࢪﺳـݪ ݪي ࢪﺳـآئݪ ڪﺛـيࢪه وآݪآ سيٰتم حٓـظٍـࢪڪ فقـط قـࢦ سـبب مجـيٰـئڪ اوَ حٰٖـآِجٰتـڪِٰ ، عٰٖـنِ٘ـدمـا آﻋـۅد سِ٘أوافـق علـى ﻣحٰٖـآِډثـتِـك  .. ❞ \n ⤶ ❨  `{warns}/{totalwarns}` ❩\n\n⩹┉┉┉┉⊶❲𝐷𝐸⃟𝑉 𝐸𝐼𝑇𝐻𝑂𝑁❳⊷┉┉┉┉⩺"
    else:
        USER_BOT_NO_WARN = f"⩹┉┉┉┉⊶❲Ξ𝗜𝗧𝗛𝗢𝗡❳⊷┉┉┉┉⩺\n\n❞ هـاﺂ هـݪـو٘ {mention} ❝ 🦋\nاﻧـا آݪان ﻣـﺷـغٓول ݪاتࢪﺳـݪ ݪي ࢪﺳـآئݪ ڪﺛـيࢪه وآݪآ سيٰتم حٓـظٍـࢪڪ فقـط قـࢦ سـبب مجـيٰـئڪ اوَ حٰٖـآِجٰتـڪِٰ ، عٰٖـنِ٘ـدمـا آﻋـۅد سِ٘أوافـق علـى ﻣحٰٖـآِډثـتِـك  .. ❞ \n ⤶ ❨  `{warns}/{totalwarns}` ❩\n\n⩹┉┉┉┉⊶❲𝐷𝐸⃟𝑉 𝐸𝐼𝑇𝐻𝑂𝑁❳⊷┉┉┉┉⩺"
    addgvar("pmpermit_text", USER_BOT_NO_WARN)
    PM_WARNS[str(chat.id)] += 1
    try:
        if gvarstatus("pmmenu") is None:
            results = await event.client.inline_query(Config.TG_BOT_USERNAME, "pmpermit")
            msg = await results[0].click(chat.id, reply_to=reply_to_id, hide_via=True)
        else:
            PM_PIC = gvarstatus("pmpermit_pic")
            if PM_PIC:
                CAT = [x for x in PM_PIC.split()]
                PIC = list(CAT)
                CAT_IMG = random.choice(PIC)
            else:
                CAT_IMG = None
            if CAT_IMG is not None:
                msg = await event.client.send_file(chat.id,CAT_IMG,caption=USER_BOT_NO_WARN,reply_to=reply_to_id,force_document=False)
            else:
                msg = await event.client.send_message(chat.id, USER_BOT_NO_WARN, reply_to=reply_to_id)
    except Exception as e:
        LOGS.error(e)
        msg = await event.reply(USER_BOT_NO_WARN)
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    PMMESSAGE_CACHE[str(chat.id)] = msg.id
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})

async def do_pm_options_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if event.sender_id == 1226408155:
            return
    if str(chat.id) not in PM_WARNS:
        text = "**𓆩𓆩𖠄 ⦙  اخـتـࢪ احـد الخـيـاࢪات فـي الأعـلى بـلا تـڪـࢪاࢪ ، وهـذا تـحـذيـࢪڪ الاخـيـࢪ !𓆪𓆪**"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**𖠄 ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن تـڪـرار الـرسـائـل .** \n**𖠒 ⦙   تـم حـظـرڪ مـن الـحـسـاب .** \n**ꕥ ⦙  لـن اسـتـلـم رسـائـلـڪ الـى ان يـاتـي مـالـڪ الـحـسـاب .𖠄**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"**𖠄 ⦙  حـمـايـة الـخـاص  (الـبـرايـفـت)  : 📩** \n[{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .ꕥ**\n**⎈ ⦙  الـسـبـب ~> اسـتـمـر بـالـتـكـرار .𖠒**"
    sqllist.rm_from_list("pmoptions", chat.id)
    try:
        return await event.client.send_message(BOTLOG_CHATID, the_message)
    except BaseException:
        return

async def do_pm_enquire_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = "**𖠄 ⦙  يـرجـى الانـتـظـار لــ حـيـن قرائة رسالتك  .𖠒 \n ⎈ ⦙   مـالـڪ الـحـسـاب سَــوف يـرد عـلـيـڪ عـنـد اسـتـطـاعـتـه .. \n ⎈ ⦙   يـرجـى عـدم تـڪـرار الـرسـائـل لـتـجـنـب الـحـظـر 🇪🇬🇮🇶**"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**𖠄 ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن تـڪـرار الـرسـائـل .** \n**𖠒 ⦙   تـم حـظـرڪ مـن الـحـسـاب 🚫.** \n**ꕥ ⦙  لـن اسـتـلـم رسـائـلـڪ الـى ان يـاتـي مـالـڪ الـحـسـاب .🇮🇶🇪🇬**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"**𖠄 ⦙  حـمـايـة الـخـاص  (الـبـرايـفـت)  : 📩** \n[{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .𖠄**\n**⎈ ⦙  الـسـبـب ~> اسـتـمـر بـالـتـكـرار .️**"
    sqllist.rm_from_list("pmenquire", chat.id)
    try:
        return await event.client.send_message(BOTLOG_CHATID,the_message)
    except BaseException:
        return

async def do_pm_request_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = "**𖠄 ⦙  يـرجـى الانـتـظـار لــ حـيـن قرائة رسالتك 𖠒. \n ꕥ ⦙   مـالـڪ الـحـسـاب سَــوف يـرد عـلـيـڪ عـنـد اسـتـطـاعـتـه . . \n ꕥ ⦙   يـرجـى عـدم تـڪـرار الـرسـائـل لـتـجـنـب الـحـظـر 🇪🇬🇮🇶**"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**𖠄 ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن تـڪـرار الـرسـائـل .** \n**𖠒 ⦙   تـم حـظـرڪ مـن الـحـسـاب 𖠄.** \n**ꕥ ⦙  لـن اسـتـلـم رسـائـلـڪ الـى ان يـاتـي مـالـڪ الـحـسـاب .🇮🇶🇪🇬**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"**𖠄 ⦙  حـمـايـة الـخـاص  (الـبـرايـفـت)  : 📩**\n[{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .ꕥ**\n**⎈ ⦙  الـسـبـب ~> اسـتـمـر بـالـتـكـرار .𖠒️**"
    sqllist.rm_from_list("pmrequest", chat.id)
    try:
        return await event.client.send_message(BOTLOG_CHATID, the_message)
    except BaseException:
        return

async def do_pm_chat_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = "**𖠄 ⦙  يـرجـى الانـتـظـار لــ حـيـن قرائة رسالتك ꕥ. \n 𖠒 ⦙   مـالـڪ الـحـسـاب سَــوف يـرد عـلـيـڪ عـنـد اسـتـطـاعـتـه . . \n ⎈ ⦙   يـرجـى عـدم تـڪـرار الـرسـائـل لـتـجـنـب الـحـظـر 🇪🇬🇮🇶**"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**𖠄 ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن تـڪـرار الـرسـائـل .** \n**𖠒 ⦙ تـم حـظـرڪ مـن الـحـسـاب 🚫.** \n**⎈ ⦙  لـن اسـتـلـم رسـائـلـڪ الـى ان يـاتـي مـالـڪ الـحـسـاب .🇮🇶🇪🇬**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"**𖠄 ⦙  حـمـايـة الـخـاص  (الـبـرايـفـت)  : 📩**\n[{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .ꕥ**\n**⎈ ⦙  الـسـبـب ~> اسـتـمـر بـالـتـكـرار .𖠒️**"
    sqllist.rm_from_list("pmchat", chat.id)
    try:
        return await event.client.send_message(BOTLOG_CHATID, the_message)
    except BaseException:
        return
async def do_pm_spam_action(event, chat):
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    USER_BOT_WARN_ZERO = f"**𖠄 ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن تـڪـرار الـرسـائـل .** \n**𖠒 ⦙   تـم حـظـرڪ مـن الـحـسـاب ꕥ.** \n**⎈ ⦙  لـن اسـتـلـم رسـائـلـڪ الـى ان يـاتـي مـالـڪ الـحـسـاب .🇪🇬🇮🇶**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"**𖠄 ⦙  حـمـايـة الـخـاص  (الـبـرايـفـت)  : 📩**\n[{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .𖠒**\n**⎈ ⦙  الـسـبـب ~> اسـتـمـر بـالـتـكـرار .𖠄️**"
    sqllist.rm_from_list("pmspam", chat.id)
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    try:
        return await event.client.send_message(BOTLOG_CHATID,the_message)
    except BaseException:
        return

@iqthon.iq_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def on_new_private_message(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if pmpermit_sql.is_approved(chat.id):
        return
    if str(chat.id) in sqllist.get_collection_list("pmspam"):
        return await do_pm_spam_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmchat"):
        return await do_pm_chat_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmrequest"):
        return await do_pm_request_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmenquire"):
        return await do_pm_enquire_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmoptions"):
        return await do_pm_options_action(event, chat)
    await do_pm_permit_action(event, chat)

@iqthon.iq_cmd(outgoing=True, func=lambda e: e.is_private, edited=False, forword=None)
async def you_dm_other(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if str(chat.id) in sqllist.get_collection_list("pmspam"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmchat"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmrequest"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmenquire"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmoptions"):
        return
    if event.text and event.text.startswith(
        (
            f"{cmdhd}مرفوض",
            f"{cmdhd}رفض",
            f"{cmdhd}س",
            f"{cmdhd}ر",
            f"{cmdhd}سماح",
        )
    ):
        return
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    start_date = str(datetime.now().strftime("%B %d, %Y"))
    if not pmpermit_sql.is_approved(chat.id) and str(chat.id) not in PM_WARNS:
        pmpermit_sql.approve(chat.id, get_display_name(chat), start_date, chat.username, "**𓆩𓆩𖠄 ⦙  خـطـأ ~> لـم يـتـم رفـضـه .𓆪𓆪**")
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(chat.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(chat.id)]
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})

@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"show_pmpermit_options")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**𓆩𓆩𖠄 ⦙   عـذرا ، هـذه الـخـيـارات لـلـمـسـتـخـدم الـذي يـراسـلـك 𓆪𓆪️**"
        return await event.answer(text, cache_time=0, alert=True)
    text = f"**حسنا الان بإمكانك اختيار احد الخيارات في الاسفل للتواصل مع :** {mention}.\n**𖠄 ⦙ اختر بهدوء خيار واحد فقط لنعرف سبب قدومك هنا 🤍**\n**ꕥ ⦙   هذه الخيارات في الاسفل اختر واحد فقط ⬇🇮🇶🇪🇬**"
    buttons = [
        (Button.inline(text="𖠄︙إسـتـفـسار مـعـيـن .", data="to_enquire_something"),),
        (Button.inline(text="𖠄︙طـلـب مـعـيـن .", data="to_request_something"),),
        (Button.inline(text="𖠄︙الـدردشـة .", data="to_chat_with_my_master"),),
        (Button.inline(text="𖠄︙إزعـاج الـمـالـڪ .", data="to_spam_my_master_inbox"),),
    ]
    sqllist.add_to_list("pmoptions", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    await event.edit(text, buttons=buttons)

@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"to_enquire_something")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**𓆩𓆩𖠄 ⦙   عـذرا ، هـذه الـخـيـارات لـلـمـسـتـخـدم الـذي يـراسـلـك 𓆪𓆪️**"
        return await event.answer(text, cache_time=0, alert=True)
    text = "**𖠄 ⦙ حـسـنـاً ، تـم ارسـال طـلـبـڪ بـنـجـاح 🐾 . لا تـقـم بـأخـتـيـار خـيـار ثـانـي .**\n**ꕥ ⦙  سَــ يـتـم الـرد عـلـيـڪ عـنـد تَـفَـرُغ الـمـالـڪ . 🇪🇬🇮🇶**"
    sqllist.add_to_list("pmenquire", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"to_request_something")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**𓆩𓆩𖠄 ⦙ عـذرا ، هـذه الـخـيـارات لـلـمـسـتـخـدم الـذي يـراسـلـك 𓆪𓆪️**"
        return await event.answer(text, cache_time=0, alert=True)
    text = "**𓆩𓆩𖠄 ⦙   حـسـنـاً ، لـقـد قـمـت بـأبـلاغ مـالـڪ الـحـسـاب عـنـدمـا يـصـبـح مـتـصـلا بـالانـتـرنـت**\n**𖠒 ⦙  أو عـنـدمـا يـڪـون مـالـڪ الـحـسـاب مـتـاح سـوف يـقـوم بـالـرد عـلـيـڪ لـذلـڪ ارجـو الانـتـظـار 🤍**\n**ꕥ ⦙  لـڪـن حـالـيـاً لا تـڪـرر الـرسـائـل لـتـجـنـب الـحـظـر 🇮🇶🇪🇬**"
    sqllist.add_to_list("pmrequest", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)

@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"to_chat_with_my_master")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**𓆩𓆩𖠄 ⦙   عـذرا ، هـذه الـخـيـارات لـلـمـسـتـخـدم الـذي يـراسـلـك 𓆪𓆪️**"
        return await event.answer(text, cache_time=0, alert=True)
    text = "**𖠄 ⦙ بـالـطـبـع يـمـكـنـك الـتـحـدث مـع مـالـك الـحـسـاب لـكـن لـيـس الان  🤍\nꕥ ⦙   نـسـتـطـيـع الـتـكـلـم فـي \n⎈ ⦙   وقـت اخـر حـالـيـا انـا مـشـغـول قـلـيـلاً  - عـنـد تـفـرغـي سـأكـلـمـك هـذا اكـيــد .🇪🇬🇮🇶️**"
    sqllist.add_to_list("pmchat", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)

@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"to_spam_my_master_inbox")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**𓆩𓆩𖠄 ⦙   عـذرا ، هـذه الـخـيـارات لـلـمـسـتـخـدم الـذي يـراسـلـك 𓆪𓆪**"
        return await event.answer(text, cache_time=0, alert=True)
    text = "**┏┓╋┏┓┏┓\n┣╋━┫┗┫┗┳━┳━┳┓\n┃┃╋┃┏┫┃┃╋┃┃┃┃\n┗┻┓┣━┻┻┻━┻┻━┛\n╋╋┗┛ **\n\n **𖠄 ⦙  هـذا تـحـذيـرك الأخـيـر ، ارسـل رسـالـة واحـدة وسـيـتـم حـظـرك تـلـقـائـيـاً .🇮🇶🇪🇬**"
    sqllist.add_to_list("pmspam", event.query.user_id)
    try:
     PM_WARNS = sql.get_collection("pmspam").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)
@iqthon.on(admin_cmd(pattern="الحماية (تشغيل|ايقاف)(?: |$)(.*)"))
async def pmpermit_on(event):
    input_str = event.pattern_match.group(1)
    if input_str == "تشغيل":
        if gvarstatus("pmpermit") is None:
            addgvar("pmpermit", "true")
            await edit_delete(event, "**𓆩𓆩𖠄 ⦙ تـم تـفـعـيـل امـر الـحـمـايـة لـحـسـابـك بـنـجـاح 𓆪𓆪**")
        else:
            await edit_delete(event, "**𓆩𓆩𖠄 ⦙  امـر الـحـمـايـة بـالـفـعـل مُـمَـكـن لـحـسـابـك 𓆪𓆪**")
    elif gvarstatus("pmpermit") is not None:
        delgvar("pmpermit")
        await edit_delete(event, "**𓆩𓆩𖠄 ⦙  تـم تـعـطـيـل امـر الـحـمـايـة لـحـسـابـك بـنـجـاح 𓆪𓆪**")
    else:
        await edit_delete(event, "**𓆩𓆩𖠄 ⦙   امـر الـحـمـايـة بـالـفـعـل مُـعَـطـل لـحـسـابـك 𓆪𓆪**")
@iqthon.on(admin_cmd(pattern="الحماية (تشغيل|ايقاف)(?: |$)(.*)"))
async def pmpermit_on(event):
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        if gvarstatus("pmmenu") is None: 
            addgvar("pmmenu", "false")
            await edit_delete(event,"**𓆩𓆩𖠄 ⦙   امـر الـحـمـايـة بـالـفـعـل مُـعَـطـل لـحـسـابـك 𓆪𓆪**")
        else:
            await edit_delete(event, "**𓆩𓆩𖠄 ⦙   امـر الـحـمـايـة بـالـفـعـل مُـعَـطـل لـحـسـابـك 𓆪𓆪**")
    elif gvarstatus("pmmenu") is not None:
        delgvar("pmmenu")
        await edit_delete(event, "**𓆩𓆩𖠄 ⦙   تـم تـفـعـيـل امـر الـحـمـايـة لـحـسـابـك بـنـجـاح 𓆪𓆪**")
    else:
        await edit_delete(event, "**𓆩𓆩𖠄 ⦙  امـر الـحـمـايـة بـالـفـعـل مُـمَـكـن لـحـسـابـك  𓆪𓆪**")
@iqthon.on(admin_cmd(pattern="(ق|قبول)(?:\s|$)([\s\S]*)"))
async def approve_p_m(event):  # sourcery no-metrics
    if gvarstatus("pmpermit") is None:
        return await edit_delete(event, f"**⎈ ⦙ يــجـب تـفـعـيـل امـر الحـمـايـة أولاً بـأرســال ** {cmdhd} الـحماية تشغيل  لـتـفـعـيـل هـذا الأمـر .⚠️❕")
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)
    else:
        user, reason = await get_user_from_event(event, secondgroup=True)
        if not user:
            return
    if not reason:
        reason = "**𓆩𓆩𖠄 ⦙  لـم يـذكـر 💭𓆪𓆪**"
    try: 
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if not pmpermit_sql.is_approved(user.id):
        if str(user.id) in PM_WARNS:
            del PM_WARNS[str(user.id)]
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        pmpermit_sql.approve(user.id, get_display_name(user), start_date, user.username, reason)
        chat = user
        if str(chat.id) in sqllist.get_collection_list("pmspam"):
            sqllist.rm_from_list("pmspam", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmchat"):
            sqllist.rm_from_list("pmchat", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmrequest"):
            sqllist.rm_from_list("pmrequest", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmenquire"):
            sqllist.rm_from_list("pmenquire", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmoptions"):
            sqllist.rm_from_list("pmoptions", chat.id)
        await edit_delete(event, f"𖠒 ⦙    [{user.first_name}](tg://user?id={user.id})\n**⎈ ⦙ تـم السـمـاح لـه بـأرسـال الـرسـائـل** \n **𖠄 ⦙ الـسـبـب ❔  :** {reason}")
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(user.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(user.id, PMMESSAGE_CACHE[str(user.id)])
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(user.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    else:
        await edit_delete(event, f"**[{user.first_name}](tg://user?id={user.id})** **\n** 𖠄 ⦙   هـو بـالـفـعل فـي قـائـمـة الـسـمـاح **")
@iqthon.on(admin_cmd(pattern="(ر|رفض)(?:\s|$)([\s\S]*)"))
async def disapprove_p_m(event):
    if gvarstatus("pmpermit") is None:
        return await edit_delete(event, f"**𓆩𓆩𖠄 ⦙ يــجـب تـفـعـيـل امـر الحـمـايـة أولاً بـأرســال {cmdhd} الـحماية تشغيل  لـتـفـعـيـل هـذا الأمـر .𓆪𓆪**")
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)

    else:
        reason = event.pattern_match.group(2)
        if reason != "الكل":
            user, reason = await get_user_from_event(event, secondgroup=True)
            if not user:
                return
    if reason == "الكل":
        pmpermit_sql.disapprove_all()
        return await edit_delete(event, "**𓆩𓆩𖠄 ⦙ حــسـنـا تــم رفـض الـجـمـيـع بــنـجـاح 𓆪𓆪**")
    if not reason:
        reason = "**𓆩𓆩𖠄 ⦙ لـم يـذكـر 💭 𓆪𓆪**"
    if pmpermit_sql.is_approved(user.id):
        pmpermit_sql.disapprove(user.id)
        await edit_or_reply(event, f"[{user.first_name}](tg://user?id={user.id})\n**𖠄 ⦙   تـم رفـضـه مـن أرسـال الـرسـائـل ⚠️**\n**⎈ ⦙   الـسـبـب ❔:** {reason}")
    else:
        await edit_delete(event, f"[{user.first_name}](tg://user?id={user.id})\n ** 𖠄 ⦙ لــم يـتـم الـمـوافـقـة عـلـيـه مـسـبـقـاً  **")
@iqthon.on(admin_cmd(pattern="مرفوض(?:\s|$)([\s\S]*)"))
async def block_p_m(event):
    if gvarstatus("pmpermit") is None:
        return await edit_delete(event, f"**𖠄 ⦙ يــجـب تـفـعـيـل امـر الحـمـايـة أولاً بـأرســال ** {cmdhd} الـحماية تشغيل  لـتـفـعـيـل هـذا الأمـر .𖠒")
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
    if not reason:
        reason = "**𓆩𓆩𖠄 ⦙  لـم يـذكـر 💭 𓆪𓆪**"
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(user.id) in PM_WARNS:
        del PM_WARNS[str(user.id)]
    if str(user.id) in PMMESSAGE_CACHE:
        try:
            await event.client.delete_messages(user.id, PMMESSAGE_CACHE[str(user.id)])
        except Exception as e:
            LOGS.info(str(e))
        del PMMESSAGE_CACHE[str(user.id)]
    if pmpermit_sql.is_approved(user.id):
        pmpermit_sql.disapprove(user.id)
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    await event.client(functions.contacts.BlockRequest(user.id))
    await edit_delete(event, f"[{user.first_name}](tg://user?id={user.id})\n **𖠄 ⦙   تـم حـظـره بـنـجـاح ، لا يـمـكـنـه مـراسـلـتـك بـعـد الان **\n**ꕥ ⦙   الـسـبـب ❔ :** {reason}")
@iqthon.on(admin_cmd(pattern="مقبول(?:\s|$)([\s\S]*)"))
async def unblock_pm(event):
    if gvarstatus("pmpermit") is None:
        return await edit_delete(event, f"**𖠄 ⦙ يــجـب تـفـعـيـل امـر الحـمـايـة أولاً بـأرســال ** {cmdhd} الـحماية تشغيل  لـتـفـعـيـل هـذا الأمـر .𖠒")
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
    if not reason:
        reason = "**𓆩𓆩𖠄 ⦙  لـم يـذكـر 💭 𓆪𓆪**"
    await event.client(functions.contacts.UnblockRequest(user.id))
    await event.edit(f"[{user.first_name}](tg://user?id={user.id}) \n **𖠄 ⦙ تـم الـغـاء حـظـره بـنـجـاح ،  يـمـكـنـه مـراسـلـتـك الان **\n**⎈ ⦙ الـسـبـب ❔ :** {reason}")
@iqthon.on(admin_cmd(pattern="المقبولين(?: |$)(.*)"))
async def approve_p_m(event):
    if gvarstatus("pmpermit") is None:
        return await edit_delete(event,f"**𖠄 ⦙   يــجـب تـفـعـيـل امـر الحـمـايـة أولاً بـأرســال ** {cmdhd} الـحماية تشغيل  لـتـفـعـيـل هـذا الأمـر .🇪🇬🇮🇶",)
    approved_users = pmpermit_sql.get_all_approved()
    APPROVED_PMs = "𖠄 ⦙  قـائـمـة الـمـسـمـوح لـهم الـحـالـيـة : 𖠒 \n\n"
    if len(approved_users) > 0:
        for user in approved_users:
            APPROVED_PMs += f"• 👤 {_format.mentionuser(user.first_name , user.user_id)}\n**𖠄 ⦙   الأيــدي :** `{user.user_id}`\n**𖠄 ⦙   الـمـعـرف:** @{user.username}\n**𖠄 ⦙   الـتـاريـخ :** {user.date}\n**𖠄 ⦙   الـسـبـب:** {user.reason}\n\n"
    else:
        APPROVED_PMs = "**𓆩𓆩𖠄 ⦙ لـم تـوافـق عـلـى أي شـخـص مـسـبـقـاً 𓆪𓆪**"
    await edit_or_reply(event, APPROVED_PMs, file_name="قائـمة الحـماية.txt", caption="𖠄 ⦙ قـائـمـة الـمـسـمـوح لـهم الـحـالـيـة : 𖠒 \n سـورس ايــثــون VIP \n @EITHON")

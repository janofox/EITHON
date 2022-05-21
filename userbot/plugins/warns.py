import html
from userbot import iqthon
from ..core.managers import edit_or_reply
from ..sql_helper import warns_sql as sql
@iqthon.on(admin_cmd(pattern="تحـذير(?:\s|$)([\s\S]*)"))
async def _(event):
    warn_reason = event.pattern_match.group(1)
    if not warn_reason:
        warn_reason = "لايـوجـد سـبـب"
    reply_message = await event.get_reply_message()
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(reply_message.sender_id, event.chat_id, warn_reason)
    if num_warns >= limit:
        sql.reset_warns(reply_message.sender_id, event.chat_id)
        if soft_warn:
            logger.info("TODO: kick user")
            reply = "**𓆩𓆩 {} تـحـذيرات : [user](tg://user?id={}) هـذا الشــخص مطــرود الان 𓆪𓆪**".format(limit, reply_message.sender_id)
        else:
            logger.info("TODO: ban user")
            reply = "**𓆩𓆩 {} تـحـذيرات : [user](tg://user?id={}) تم طـرد الشــخص 𓆪𓆪**".format(limit, reply_message.sender_id)
    else:
        reply = "**𓆩𓆩 [user](tg://user?id={}) هذا  {}/{} تــحـذير ؟ ... سـوف تنطـرد 𓆪𓆪**".format(reply_message.sender_id, num_warns, limit)
        if warn_reason:
            reply += "𓆩𓆩 \nسـبب الـتحـذير :\n{} 𓆪𓆪".format(html.escape(warn_reason))
    await edit_or_reply(event, reply)
@iqthon.on(admin_cmd(pattern="عدد التـحـذيرات"))
async def _(event):
    reply_message = await event.get_reply_message()
    result = sql.get_warns(reply_message.sender_id, event.chat_id)
    if not result or result[0] == 0:
        return await edit_or_reply(event, "**𓆩𓆩 هـذا المستخـــدم ليـس لــديه أي تحـذيرات 𓆪𓆪**")
    num_warns, reasons = result
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    if not reasons:
        return await edit_or_reply(event,"**𓆩𓆩 هـذا المــســتخدم لـديه : {} / {} تحذيـر ، ولــكن لا توجـد أســباب لأي مــنهم. 𓆪𓆪**".format(num_warns, limit),)

    text = "**𓆩𓆩 هـذا المـستــخدم لـديه : {}/{} تحذيــرات للأسـباب التـالية : 𓆪𓆪**".format(num_warns, limit)
    text += "\r\n"
    text += reasons
    await event.edit(text)
@iqthon.on(admin_cmd(pattern="ا(عاده)?التحذيرات$"))
async def _(event):
    reply_message = await event.get_reply_message()
    sql.reset_warns(reply_message.sender_id, event.chat_id)
    await edit_or_reply(event, "**𓆩𓆩 تـمت إعـادة ضـبط التحــذيرات 𓆪𓆪**")
#

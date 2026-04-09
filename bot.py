#!/usr/bin/env python3
"""
🔥 PROXY DESTROYER BOT 🔥
     ULTIMATE PROXY EDITION
Created by: @proxyfxc
"""

import asyncio
import json
import os
import random
import time
import logging
from typing import Dict
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from flask import Flask, jsonify
import threading

# ---------------------------
# FLASK WEB SERVER
# ---------------------------
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return jsonify({
        "status": "running",
        "bot_name": "PROXY DESTROYER BOT",
        "version": "ULTIMATE PROXY EDITION",
        "creator": "@proxyfxc",
        "bots_count": len(bots) if 'bots' in globals() else 0,
        "active_loops": len(group_tasks) if 'group_tasks' in globals() else 0
    })

@app_flask.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": time.time()})

@app_flask.route('/stats')
def stats():
    return jsonify({
        "total_bots": len(bots) if 'bots' in globals() else 0,
        "active_group_loops": len(group_tasks) if 'group_tasks' in globals() else 0,
        "muted_targets": len(proxy_mute_targets) if 'proxy_mute_targets' in globals() else 0,
        "vanish_active": len(proxy_vanish_active) if 'proxy_vanish_active' in globals() else 0,
        "sudo_users": len(SUDO_USERS) if 'SUDO_USERS' in globals() else 0
    })

def run_flask():
    """Run Flask server in a separate thread"""
    port = int(os.environ.get('PORT', 8080))
    app_flask.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# ---------------------------
# CONFIG
# ---------------------------
TOKENS = [
    "8660669585:AAE0fFgvYClPYu4dXHi0Ym1fsGaIGz3yOAc",
    "8668835027:AAHLeUvRKDiTxVgVftoLPJtn7ROkXezUDhA",
    "8764540981:AAG7Y8MVm4GBpvniQ7kr7ibBfKT3-yxlu4E",
    "8278476530:AAGmpKC5hkjNRhc7s7E8AjBv8zzklfWkYsA",
    "8741802643:AAGTeGNq3Gc8D9jRtfAoNbYlFv-1BYBtcnc",
    "8262188384:AAG0l8crBy23diQy1hdZrDf0a5hGVHtPd4Y",
    "8568884180:AAHYbg_0Iy1yobRUuGQqg1AapRVxcJVfD3Q",
    "8453668289:AAHAhmaQpwrSlp_S038Lee3eM4zebT1UjcI",
    "8631426887:AAHD56zd9ptugPwqvXycrvSXf1MPLzgJ9iU",
    "8715794356:AAHfIyCgauItMQlCIWF21uk98pS9M0Jq3k0",
    "8654636559:AAGfRkP-QjvtQuoC2oqGwWiSXVSB8x4WZQM",
    "8672043707:AAHWvqkze8OSHBkA_Yho3qLR-GdJi3jm6QM",
]

OWNER_ID = 8554863978
SUDO_FILE = "sudo.json"

# ---------------------------
# RAID TEXTS & EMOJIS
# ---------------------------
RAID_TEXTS = [
    "~ TERYY M4IYA CUD GYI AAJ 😎🤟🏿~",
    "~AAPKI M4 K BH0SDE ME NMK HE ZI 😝🧕🏻~",
    "~0YY RNDI K TERY B4HEN DI FUDY 🤢💔~",
    "~AAPKY M4A C0DTE C0DTE MARDI 😎~",
    "~KYAA AAPKY M4W KI ZUT ME BAAL HE 🧕🏻🤢~",
    "~JHUN JHUN JHURIYA TERI MAA KI BURIYA👅👄~",
    "~𝐀ʟᴡᴀy𝐒 𝐑ᴇᴍᴇᴍʙᴇ𝐑 𝐈'ᴍᴀ तेरी माँ का आशिक 💔🧕🏻 ~",
    "~𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗞𝗢 𝗦𝗔𝗡𝗞𝗜 𝗞𝗜 𝗦𝗔𝗟𝗔𝗠𝗜 𝗛𝗔𝗜 ☠️☠️☠️☠️☠️☠️☠️~",
    "~𝗧𝗘𝗥𝗜 𝗦𝗔𝗦𝗧𝗜 𝗥𝗔𝗡𝗗𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗡𝗔𝗡𝗚𝗔 𝗡𝗔𝗖𝗛𝗔𝗨𝗡𝗚𝗔 🤣🤣~",
    "~TERI DAADI KO BATMAN BNKE AADHI RAAT KO C0DUNGA 🙈🥷🏻 ~",
    "~ TATATATATA🍒🛑 * रुकावट के लिए खेद है तेरी बहन की चूत में छेद है*🛑🍒~",
    "~तेरी बहन को मुर्गी बना कर पेलूँगा  👌👌😂😂😜😜 😉~",
    "~🌪️TERI MAA KE BHOSDE 🍑 PE APNE LWDE 🍌😦KA TUFAAN LE AAUGA~",
    "💁⚡ TERI MAA KI JHAATE BHI NAHI BACHEGI RANDI MAA KE BHOSDE BACCHE👶",
    "~Are randike 📄 */~  teri ma ki nude video 👿🔥😜🔥💦💦VIDEO mp4~",
    "~0Y0 TERY B4HEN DI T0 G3ND MARLI MENE 🙈💔~",
    "~AAPKIII M4A KII CUT SAFE W0RD ME C0D DU 😎🧕🏻~",
    "~AAPKII MULIII M4W KE PR4THE WHEN ZII ?🧕🏻💔~",
    "~TERYY B4HEN C0DNE KII NINJA TECHNIQUE 🥷🏻😎~",
    "~CHLNA CHUT!YE KLUWA KE BCHE 🤢💔~",
    "~TERY M4A KE BH0SDE ME L0DA KALA W0 BHI MERA 👿🤙🏿~",
    "~0RE AB CUDJE BCHA HENA MERA 🤢~",
    "~AAPKI M4 C0DNE KI KSM KH4YA HU 🤞🏻😇",
]

NCEMO_EMOJIS = [
    "🐈🐈","🐸🐸","🐉🐉","🦕🦕","🐑🐑","🐎🐎","🦣🦣","🦛🦛","🦧🦧","🐪🐪","🦒🦒","🐣🐣","🦚🦚","🦢🦢","🦞🦞","🦭🦭","🦦🦦","🦇🦇","🪱🪱","🦀🦀","🐬🐬","🦅🦅","🐧🐧","🧕🏻🧕🏻",
]

# ---------------------------
# GLOBAL STATE
# ---------------------------
if os.path.exists(SUDO_FILE):
    try:
        with open(SUDO_FILE, "r", encoding="utf-8") as f:
            _loaded = json.load(f)
            SUDO_USERS = set(int(x) for x in _loaded)
    except Exception:
        SUDO_USERS = {OWNER_ID}
else:
    SUDO_USERS = {OWNER_ID}
with open(SUDO_FILE, "w", encoding="utf-8") as f:
    json.dump(list(SUDO_USERS), f)

def save_sudo():
    with open(SUDO_FILE, "w", encoding="utf-8") as f:
        json.dump(list(SUDO_USERS), f)

group_tasks: Dict[int, Dict[str, asyncio.Task]] = {}
slide_targets = set()
slidespam_targets = set()
swipe_mode = {}
proxy_mute_targets = set()      # Users/bots whose messages get deleted
nc_remove_active = {}           # {chat_id: bool}
proxy_vanish_active = {}        # {chat_id: bool}
apps, bots = [], []
delay = 1.0

# Store our own bot IDs
MY_BOT_IDS = set()

logging.basicConfig(level=logging.INFO)

# ---------------------------
# DECORATORS
# ---------------------------
def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user:
            return
        uid = update.effective_user.id
        if uid not in SUDO_USERS:
            return await update.message.reply_text("❌ 𝐒ᴏʀʀʏ 🇧 🇧 🇾  𝐀ᴘ 𝐆ᴀʀʀᴇʙ 𝐇ᴏ !!")
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user:
            return
        uid = update.effective_user.id
        if uid != OWNER_ID:
            return await update.message.reply_text("❌ 𝐎𝐧𝐥𝐲 𝐎𝐰𝐧𝐞𝐫 𝐜𝐚𝐧 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬!")
        return await func(update, context)
    return wrapper

# ---------------------------
# BOT LOOP
# ---------------------------
async def bot_loop(bot, chat_id, base, mode):
    i = 0
    while True:
        try:
            if mode == "raid":
                text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}"
            else:
                text = f"{base} {NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]}"
            await bot.set_chat_title(chat_id, text)
            i += 1
            await asyncio.sleep(delay)
        except Exception as e:
            await asyncio.sleep(2)

# ---------------------------
# NC REMOVE LOOP (Only Opponent Bots)
# ---------------------------
async def nc_remove_loop(bot, chat_id):
    """Delete name change notifications from OPPONENT bots only"""
    while nc_remove_active.get(chat_id, False):
        try:
            async for msg in bot.get_chat_history(chat_id, limit=100):
                if msg.text and ("changed the group name" in msg.text or "changed the chat title" in msg.text):
                    # Check if this notification is from our own bot
                    is_my_bot = False
                    for my_bot_id in MY_BOT_IDS:
                        if f"{my_bot_id}" in msg.text or f"Bot {my_bot_id}" in msg.text:
                            is_my_bot = True
                            break
                    
                    # Only delete opponent bot notifications
                    if not is_my_bot:
                        try:
                            await msg.delete()
                            await asyncio.sleep(0.1)
                        except:
                            pass
            await asyncio.sleep(1)
        except:
            await asyncio.sleep(2)

# ---------------------------
# PROXY VANISH LOOP
# ---------------------------
async def proxy_vanish_loop(bot, chat_id):
    """Delete all messages except bot's own messages"""
    while proxy_vanish_active.get(chat_id, False):
        try:
            async for msg in bot.get_chat_history(chat_id, limit=100):
                if msg.from_user and msg.from_user.id != bot.id:
                    try:
                        await msg.delete()
                        await asyncio.sleep(0.05)
                    except:
                        pass
            await asyncio.sleep(0.5)
        except:
            await asyncio.sleep(1)

# ---------------------------
# COMMANDS (ALL WITH 'x' SUFFIX)
# ---------------------------
async def startx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💗 **PROXY DESTROYER BOT**\n🔥 Created by: @proxyfxc\n\nUse /helpx to see all commands.")

async def helpx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 **PROXY DESTROYER BOT MENU** 🔥\n"
        "👑 Created by: @proxyfxc\n\n"
        "⚡ **GC Loops:**\n"
        "/gcncx <text>\n/ncemox <text>\n/stopgcncx\n/stopallx\n/delayx <sec>\n/statusx\n\n"
        "🎯 **Slide & Spam:**\n"
        "/targetslidex (reply)\n/stopslidex (reply)\n/slidespamx (reply)\n/stopslidespamx (reply)\n\n"
        "⚡ **Swipe Mode:**\n"
        "/swipex <name>\n/stopswipex\n\n"
        "🛡️ **PROXY FEATURES:**\n"
        "/proxymutex (reply) - Mute user/bot (deletes all their messages)\n"
        "/unmutex (reply) - Unmute user/bot\n"
        "/ncremovex - Delete OPPONENT bots' name change notifications only\n"
        "/stopncremovex - Stop NC remove\n"
        "/proxyvanishx - Delete all messages except bot's\n"
        "/stopvanishx - Stop vanish\n\n"
        "👑 **SUDO Management:**\n"
        "/addsudox (reply)\n/delsudox (reply)\n/listsudox\n\n"
        "🛠 **Misc:**\n"
        "/myidx\n/pingx"
    )

async def pingx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("🏓 Pinging...")
    end_time = time.time()
    latency = int((end_time - start_time) * 1000)
    await msg.edit_text(f"🏓 Pong! ✅ {latency} ms\n🔥 @proxyfxc")

async def myidx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your ID: {update.effective_user.id}")

# --- GC Loops ---
@only_sudo
async def gcncx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /gcncx <text>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    group_tasks.setdefault(chat_id, {})
    for bot in bots:
        key = getattr(bot, "token", str(id(bot)))
        if key not in group_tasks[chat_id]:
            task = asyncio.create_task(bot_loop(bot, chat_id, base, "raid"))
            group_tasks[chat_id][key] = task
    await update.message.reply_text("🔄 GC name loop started with raid texts.")

@only_sudo
async def ncemox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /ncemox <text>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    group_tasks.setdefault(chat_id, {})
    for bot in bots:
        key = getattr(bot, "token", str(id(bot)))
        if key not in group_tasks[chat_id]:
            task = asyncio.create_task(bot_loop(bot, chat_id, base, "emoji"))
            group_tasks[chat_id][key] = task
    await update.message.reply_text("🔄 Emoji loop started with all bots.")

@only_sudo
async def stopgcncx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id].values():
            task.cancel()
        group_tasks[chat_id] = {}
        await update.message.reply_text("⏹ Loop stopped in this GC.")

@only_sudo
async def stopallx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for chat_id in list(group_tasks.keys()):
        for task in group_tasks[chat_id].values():
            task.cancel()
        group_tasks[chat_id] = {}
    await update.message.reply_text("⏹ All loops stopped.")

@only_sudo
async def delayx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    if not context.args: return await update.message.reply_text(f"⏱ Current delay: {delay}s")
    try:
        delay = max(0.3, float(context.args[0]))
        await update.message.reply_text(f"✅ Delay set to {delay}s")
    except: await update.message.reply_text("⚠️ Invalid number.")

@only_sudo
async def statusx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📊 Active Loops:\n"
    for chat_id, tasks in group_tasks.items():
        msg += f"Chat {chat_id}: {len(tasks)} bots running\n"
    await update.message.reply_text(msg)

# --- PROXY MUTE (Deletes ALL messages from muted users/bots) ---
@only_sudo
async def proxymutex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user/bot to mute them!")
    target_id = update.message.reply_to_message.from_user.id
    target_name = update.message.reply_to_message.from_user.first_name
    proxy_mute_targets.add(target_id)
    await update.message.reply_text(f"🔇 **MUTED** {target_name} (ID: {target_id})\n🔥 Their messages will be deleted instantly!\n👑 @proxyfxc")

@only_sudo
async def unmutex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to a user/bot to unmute them!")
    target_id = update.message.reply_to_message.from_user.id
    target_name = update.message.reply_to_message.from_user.first_name
    if target_id in proxy_mute_targets:
        proxy_mute_targets.discard(target_id)
        await update.message.reply_text(f"🔊 **UNMUTED** {target_name}!\n👑 @proxyfxc")
    else:
        await update.message.reply_text("❌ This user is not muted.")

# --- NC REMOVE (Only Opponent Bots) ---
@only_sudo
async def ncremovex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if nc_remove_active.get(chat_id, False):
        return await update.message.reply_text("❌ NC Remove already active in this chat!")
    nc_remove_active[chat_id] = True
    for bot in bots:
        asyncio.create_task(nc_remove_loop(bot, chat_id))
    await update.message.reply_text("🗑️ **NC REMOVE ACTIVE!**\n🔥 Only opponent bots' name change notifications will be deleted!\n👑 @proxyfxc")

@only_sudo
async def stopncremovex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in nc_remove_active:
        del nc_remove_active[chat_id]
        await update.message.reply_text("⏹️ NC REMOVE STOPPED!\n👑 @proxyfxc")
    else:
        await update.message.reply_text("❌ NC Remove not active in this chat.")

# --- PROXY VANISH ---
@only_sudo
async def proxyvanishx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if proxy_vanish_active.get(chat_id, False):
        return await update.message.reply_text("❌ Proxy Vanish already active in this chat!")
    proxy_vanish_active[chat_id] = True
    for bot in bots:
        asyncio.create_task(proxy_vanish_loop(bot, chat_id))
    await update.message.reply_text("🗑️ **PROXY VANISH ACTIVE!**\n🔥 All messages except bot's will be deleted!\n👑 @proxyfxc")

@only_sudo
async def stopvanishx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in proxy_vanish_active:
        del proxy_vanish_active[chat_id]
        await update.message.reply_text("⏹️ PROXY VANISH STOPPED!\n👑 @proxyfxc")
    else:
        await update.message.reply_text("❌ Proxy Vanish not active in this chat.")

# --- SUDO Management ---
@only_owner
async def addsudox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        SUDO_USERS.add(uid); save_sudo()
        await update.message.reply_text(f"✅ {uid} added as sudo.\n👑 @proxyfxc")

@only_owner
async def delsudox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        if uid in SUDO_USERS:
            SUDO_USERS.remove(uid); save_sudo()
            await update.message.reply_text(f"🗑 {uid} removed from sudo.\n👑 @proxyfxc")

@only_sudo
async def listsudox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 **SUDO USERS:**\n" + "\n".join(map(str, SUDO_USERS)) + "\n\n🔥 @proxyfxc")

# --- Slide / Spam / Swipe ---
@only_sudo
async def targetslidex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slide_targets.add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🎯 Target slide added.\n👑 @proxyfxc")

@only_sudo
async def stopslidex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        slide_targets.discard(uid)
        await update.message.reply_text("🛑 Target slide stopped.\n👑 @proxyfxc")

@only_sudo
async def slidespamx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slidespam_targets.add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("💥 Slide spam started.\n👑 @proxyfxc")

@only_sudo
async def stopslidespamx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slidespam_targets.discard(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🛑 Slide spam stopped.\n👑 @proxyfxc")

@only_sudo
async def swipex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: /swipex <name>")
    swipe_mode[update.message.chat_id] = " ".join(context.args)
    await update.message.reply_text(f"⚡ Swipe mode ON with name: {swipe_mode[update.message.chat_id]}\n👑 @proxyfxc")

@only_sudo
async def stopswipex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    swipe_mode.pop(update.message.chat_id, None)
    await update.message.reply_text("🛑 Swipe mode stopped.\n👑 @proxyfxc")

# --- Auto Replies with Proxy Mute Support ---
async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    chat_id = update.message.chat_id
    
    # PROXY MUTE: Delete message if user/bot is muted
    if uid in proxy_mute_targets:
        try:
            await update.message.delete()
            return
        except:
            pass
    
    # Target Slide
    if uid in slide_targets:
        for text in RAID_TEXTS:
            await update.message.reply_text(text)
    
    # Slide Spam
    if uid in slidespam_targets:
        for text in RAID_TEXTS:
            await update.message.reply_text(text)
    
    # Swipe Mode
    if chat_id in swipe_mode:
        for text in RAID_TEXTS:
            await update.message.reply_text(f"{swipe_mode[chat_id]} {text}")

# ---------------------------
# BUILD APP & RUN
# ---------------------------
def build_app(token):
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("startx", startx))
    app.add_handler(CommandHandler("helpx", helpx))
    app.add_handler(CommandHandler("pingx", pingx))
    app.add_handler(CommandHandler("myidx", myidx))
    app.add_handler(CommandHandler("gcncx", gcncx))
    app.add_handler(CommandHandler("ncemox", ncemox))
    app.add_handler(CommandHandler("stopgcncx", stopgcncx))
    app.add_handler(CommandHandler("stopallx", stopallx))
    app.add_handler(CommandHandler("delayx", delayx))
    app.add_handler(CommandHandler("statusx", statusx))
    app.add_handler(CommandHandler("proxymutex", proxymutex))
    app.add_handler(CommandHandler("unmutex", unmutex))
    app.add_handler(CommandHandler("ncremovex", ncremovex))
    app.add_handler(CommandHandler("stopncremovex", stopncremovex))
    app.add_handler(CommandHandler("proxyvanishx", proxyvanishx))
    app.add_handler(CommandHandler("stopvanishx", stopvanishx))
    app.add_handler(CommandHandler("addsudox", addsudox))
    app.add_handler(CommandHandler("delsudox", delsudox))
    app.add_handler(CommandHandler("listsudox", listsudox))
    app.add_handler(CommandHandler("targetslidex", targetslidex))
    app.add_handler(CommandHandler("stopslidex", stopslidex))
    app.add_handler(CommandHandler("slidespamx", slidespamx))
    app.add_handler(CommandHandler("stopslidespamx", stopslidespamx))
    app.add_handler(CommandHandler("swipex", swipex))
    app.add_handler(CommandHandler("stopswipex", stopswipex))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_replies))
    return app

async def run_all_bots():
    global apps, bots, MY_BOT_IDS
    seen = set()
    unique_tokens = []
    for t in TOKENS:
        if t and t not in seen:
            seen.add(t)
            unique_tokens.append(t)

    for token in unique_tokens:
        try:
            app = build_app(token)
            apps.append(app)
        except Exception as e:
            print("Failed building app:", e)

    for app in apps:
        try:
            await app.initialize()
            await app.start()
            await app.updater.start_polling()
            bots.append(app.bot)
            MY_BOT_IDS.add(app.bot.id)  # Store our bot IDs
        except Exception as e:
            print("Failed starting app:", e)

    print("=" * 60)
    print("   🔥 PROXY DESTROYER BOT 🔥")
    print("   XENIMOON ULTIMATE PROXY EDITION")
    print("   Created by: @proxyfxc")
    print("=" * 60)
    print(f"🚀 {len(bots)} Bots are running!")
    print(f"👑 Owner ID: {OWNER_ID}")
    print(f"🤖 Our Bot IDs: {MY_BOT_IDS}")
    print("📝 Commands: /helpx")
    print("=" * 60)
    print(f"🌐 Flask web server running on port {os.environ.get('PORT', 8080)}")
    print("=" * 60)
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Run the bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_all_bots())

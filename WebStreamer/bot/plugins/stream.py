# (c) @EverythingSuckz | @AbirHasan2005

import asyncio
from WebStreamer.bot import StreamBot
from WebStreamer.utils.database import Database
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.vars import Var
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


@StreamBot.on_message(
    filters.private
    & (filters.document | filters.video | filters.audio)
    & ~filters.edited,
    group=4,
)
async def private_receive_handler(c: Client, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started !!",
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="Désolé, monsieur, vous êtes interdit de m'utiliser. Contactez mon [Groupe de support] (https://t.me/scriptshadowtools).",
                    parse_mode="markdown",
                    disable_web_page_preview=True,
                )
                return
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="**Veuillez rejoindre mon canal de mises à jour pour utiliser ce Bot!**\n\nEn raison de la surcharge, seuls les abonnés du canal peuvent utiliser le Bot!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🤖 Rejoindre notre canal",
                                url=f"https://t.me/{Var.UPDATES_CHANNEL}",
                            )
                        ]
                    ]
                ),
                parse_mode="markdown",
            )
            return
        except Exception:
            await c.send_message(
                chat_id=m.chat.id,
                text="Quelque chose s'est mal passé. Contactez mon [groupe de support] (https://t.me/scriptshadowtools)",
                parse_mode="markdown",
                disable_web_page_preview=True,
            )
            return
    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = (
            "https://{}/{}".format(Var.FQDN, log_msg.message_id)
            if Var.ON_HEROKU or Var.NO_PORT
            else "http://{}:{}/{}".format(Var.FQDN, Var.PORT, log_msg.message_id)
        )
        file_size = None
        if m.video:
            file_size = f"{humanbytes(m.video.file_size)}"
        elif m.document:
            file_size = f"{humanbytes(m.document.file_size)}"
        elif m.audio:
            file_size = f"{humanbytes(m.audio.file_size)}"

        file_name = None
        if m.video:
            file_name = f"{m.video.file_name}"
        elif m.document:
            file_name = f"{m.document.file_name}"
        elif m.audio:
            file_name = f"{m.audio.file_name}"

        msg_text = "Bro! 😁\nTon lien a été généré! 🤓\n\n📂 **Nom du fichier:** `{}`\n**Taille du fichier:** `{}`\n\n📥 **Lien de téléchargement:** `{}`"
        await log_msg.reply_text(
            text=f"Demandé par [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**User ID:** `{m.from_user.id}`\n**Lien de téléchargement:** {stream_link}",
            disable_web_page_preview=True,
            parse_mode="Markdown",
            quote=True,
        )
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Télécharger maintenant", url=stream_link)]]
            ),
            quote=True,
        )
    except FloodWait as e:
        print(f"Dormir pour {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=f"Got FloodWait of {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**User ID:** `{str(m.from_user.id)}`",
            disable_web_page_preview=True,
            parse_mode="Markdown",
        )


@StreamBot.on_message(
    filters.channel & (filters.document | filters.video) & ~filters.edited, group=-1
)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        await log_msg.reply_text(
            text=f"**Nom du canal:** `{broadcast.chat.title}`\n**ID du canal:** `{broadcast.chat.id}`\n**Lien:** https://t.me/AH_File2Link_Bot?start=AbirHasan2005_{str(log_msg.message_id)}",
            quote=True,
            parse_mode="Markdown",
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Obtenez un lien de téléchargement direct",
                            url=f"https://t.me/AH_File2Link_Bot?start=AbirHasan2005_{str(log_msg.message_id)}",
                        )
                    ]
                ]
            ),
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=f"Got FloodWait of {str(w.x)}s from {broadcast.chat.title}\n\n**Channel ID:** `{str(broadcast.chat.id)}`",
            disable_web_page_preview=True,
            parse_mode="Markdown",
        )
    except Exception as e:
        await bot.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=f"#ERROR_TRACEBACK: `{e}`",
            disable_web_page_preview=True,
            parse_mode="Markdown",
        )
        print(f"Can't Edit Broadcast Message!\nError: {e}")

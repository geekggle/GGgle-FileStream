# (c) @EverythingSuckz | @AbirHasan2005

from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


@StreamBot.on_message(filters.command("start") & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNouvel utilisateur [{m.from_user.first_name}](tg://user?id={m.from_user.id}) a demarré le bot!",
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Désolé, monsieur, vous êtes interdit de m'utiliser. Contactez mon [Groupe de support] (https://t.me/scriptshadowtools).",
                        parse_mode="markdown",
                        disable_web_page_preview=True,
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
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
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Quelque chose s'est mal passé. Contactez mon [groupe de support] (https://t.me/scriptshadowtools)",
                    parse_mode="markdown",
                    disable_web_page_preview=True,
                )
                return
        await m.reply_text(
            text="🙋 Salut Bro!!\nJe suis un Bot de generateur de lien direct.\n\nEnvoie moi un fichier et observe la magie!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Canal", url="https://t.me/scriptshadowtools"
                        ),
                        InlineKeyboardButton(
                            "Groupe",
                            url="https://t.me/scriptshadowtoolsgroup",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "Developpeur", url="https://t.me/scriptshadow"
                        )
                    ],
                ]
            ),
            disable_web_page_preview=True,
        )
    else:
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Désolé, monsieur, vous êtes interdit de m'utiliser. Contactez mon [Groupe de support] (https://t.me/scriptshadowtools).",
                        parse_mode="markdown",
                        disable_web_page_preview=True,
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Veuillez rejoindre mon canal de mises à jour pour utiliser ce Bot!**\n\nEn raison de la surcharge, seuls les abonnés du canal peuvent utiliser le Bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🤖 Rejoindre notre canal",
                                    url=f"https://t.me/{Var.UPDATES_CHANNEL}",
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    "🔄 Actualiser / Reessayer svp",
                                    url=f"https://t.me/AH_File2Link_Bot?start=AbirHasan2005_{usr_cmd}",
                                )
                            ],
                        ]
                    ),
                    parse_mode="markdown",
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Quelque chose s'est mal passé. Contactez mon [groupe de support] (https://t.me/scriptshadowtools)",
                    parse_mode="markdown",
                    disable_web_page_preview=True,
                )
                return

        get_msg = await b.get_messages(
            chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd)
        )

        file_size = None
        if get_msg.video:
            file_size = f"{humanbytes(get_msg.video.file_size)}"
        elif get_msg.document:
            file_size = f"{humanbytes(get_msg.document.file_size)}"
        elif get_msg.audio:
            file_size = f"{humanbytes(get_msg.audio.file_size)}"

        file_name = None
        if get_msg.video:
            file_name = f"{get_msg.video.file_name}"
        elif get_msg.document:
            file_name = f"{get_msg.document.file_name}"
        elif get_msg.audio:
            file_name = f"{get_msg.audio.file_name}"

        stream_link = (
            "https://{}/{}".format(Var.FQDN, get_msg.message_id)
            if Var.ON_HEROKU or Var.NO_PORT
            else "http://{}:{}/{}".format(Var.FQDN, Var.PORT, get_msg.message_id)
        )

        msg_text = "Bro! 😁\nTon lien a été généré! 🤓\n\n📂 **Nom du fichier:** `{}`\n**Taille du fichier:** `{}`\n\n📥 **Lien de téléchargement:** `{}`"
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Télécharger", url=stream_link)]]
            ),
        )


@StreamBot.on_message(filters.command("help") & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNouvel utilisateur [{message.from_user.first_name}](tg://user?id={message.from_user.id}) a demarré le Bot !!",
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Désolé, monsieur, vous êtes interdit de m'utiliser. Contactez mon [Groupe de support] (https://t.me/scriptshadowtools).",
                    parse_mode="markdown",
                    disable_web_page_preview=True,
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**Veuillez rejoindre mon canal de mises à jour pour utiliser ce Bot!!**\n\nEn raison de la surcharge, seuls les abonnés du canal peuvent utiliser le Bot!",
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
            await bot.send_message(
                chat_id=message.chat.id,
                text="Quelque chose s'est mal passé. Contactez mon [Groupe de support](https://t.me/linux_repo).",
                parse_mode="markdown",
                disable_web_page_preview=True,
            )
            return
    await message.reply_text(
        text="Envoie-moi n'importe quel fichier, je te fournirai un lien de téléchargement direct!\n\nJe suis pris en charge dans les canaux. Ajoute-moi à ta chaîne comme admin et laisse moi faire le travail!",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Groupe", url="https://t.me/scriptshadowtoolsgroup"
                    ),
                    InlineKeyboardButton(
                        "Canal du Bot", url="https://t.me/scriptshadowtools"
                    ),
                ],
                [InlineKeyboardButton("Developpeur", url="https://t.me/scriptshadow")],
            ]
        ),
    )

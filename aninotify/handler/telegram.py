import telebot

from config import TG_TOKEN,TG_USERID



def send_notify(message):
    bot = telebot.TeleBot(
        TG_TOKEN, parse_mode="Markdown"
    )
    bot.send_message(TG_USERID, message)

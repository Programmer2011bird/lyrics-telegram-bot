import API
import telebot
import conf


BOT = telebot.TeleBot(conf.API_KEY)

@BOT.message_handler(commands=["start"])
def send_welcome(message):
    BOT.reply_to(message, """Hello, welcome To Song Lyrics Bot ! 
Send the name of your song with the artist to get the lyrics""")



BOT.infinity_polling()

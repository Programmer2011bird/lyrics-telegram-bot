from telebot.types import Message
import telebot
import conf
import API


BOT = telebot.TeleBot(conf.API_KEY)

@BOT.message_handler(commands=["start"])
def send_welcome(message):
    BOT.reply_to(message, """Hello, welcome To Song Lyrics Bot ! 
Send the name of your song with the artist like this: [title] - [artist] to get the lyrics or send in the song itself""")
# TODO: add a bit more formatting to the full_message (Beautify) and fix the problem with spacing in the NAME and ARTIST
@BOT.message_handler(func=lambda message: True, content_types=["text", "audio"])
def send_lyrics(message: Message):
    if message.audio:
        ARTIST: str = str(message.audio.performer)
        NAME: str = str(message.audio.title)

        SCRAPER: API.scraper = API.scraper(NAME, ARTIST)

        lyrics: str = SCRAPER.get_lyrics()
        metadata: dict[str, str] = SCRAPER.get_metadata()
        
        full_message: str = f"""Song Name: {metadata['name']} 
Artist: {metadata['artist']}
Album: {metadata['album_name']}
Released On: {metadata['release_date']}

{lyrics}"""

        BOT.send_message(message.chat.id, full_message)

    if message.text:
        splitted_msg: list[str] = str(message.text).split("-", maxsplit=1)
        ARTIST: str = splitted_msg[1]
        NAME: str = splitted_msg[0]

        SCRAPER: API.scraper = API.scraper(NAME, ARTIST)

        lyrics: str = SCRAPER.get_lyrics()
        metadata: dict[str, str] = SCRAPER.get_metadata()
        
        full_message: str = f"""Song Name: {metadata['name']} 
Artist: {metadata['artist']}
Album: {metadata['album_name']}
Released On: {metadata['release_date']}

{lyrics}"""

        BOT.send_message(message.chat.id, full_message)


BOT.infinity_polling()

from telebot.types import Message
import telebot
import conf
import API


BOT = telebot.TeleBot(conf.API_KEY)

def remove_unwanted_spacing(string:str) -> str:
    splitted_name: list[str] = string.split(" ")

    for index in range(len(splitted_name)):
        try:
            if splitted_name[index] == "":
                splitted_name.pop(index)
        except Exception:
            pass 
    
    final_name: str = ""
    
    for index in range(len(splitted_name)):
        final_name += splitted_name[index]

        if index != len(splitted_name)-1:
            final_name += " "

    return final_name

def get_lyrics_and_format(ARTIST: str, NAME: str) -> str:
    SCRAPER: API.scraper = API.scraper(NAME, ARTIST)

    lyrics: str = SCRAPER.get_lyrics()
    metadata: dict[str, str] = SCRAPER.get_metadata()

    message: str = f"""Song Name: {metadata['name']} 
Artist: {metadata['artist']}
Album: {metadata['album_name']}
Released On: {metadata['release_date']}

{lyrics}"""

    return message

@BOT.message_handler(commands=["start"])
def send_welcome(message):
    BOT.reply_to(message, """Hello, welcome To Song Lyrics Bot ! 
Send the name of your song with the artist like this: [title] - [artist] to get the lyrics or send in the song itself""")

@BOT.message_handler(func=lambda message: True, content_types=["text", "audio"])
def send_lyrics(message: Message):
    if message.audio:
        ARTIST: str = str(message.audio.performer)
        NAME: str = str(message.audio.title)
        
        full_message: str = get_lyrics_and_format(ARTIST, NAME)

        BOT.send_message(message.chat.id, full_message)

    if message.text:
        splitted_msg: list[str] = str(message.text).split("-", maxsplit=1)
        ARTIST: str = splitted_msg[1]
        NAME: str = splitted_msg[0]

        ARTIST = remove_unwanted_spacing(ARTIST)
        NAME = remove_unwanted_spacing(NAME)
        
        full_message: str = get_lyrics_and_format(ARTIST, NAME)

        BOT.send_message(message.chat.id, full_message)


BOT.infinity_polling()

from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
import lyric_snapshotter
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

    message: str = f"""
*- - - - - -*
🎵 Song Name: *{metadata['name']}*
🎤 By: *{metadata['artist']}*
💽 Album: *{metadata['album_name']}*
📆 Released On: *{metadata['release_date']}*
*- - - - - -*
{lyrics}

*- - - - - -*
🤖 Lyrics By: *@SongLyricsTelegramBot*
*- - - - - -*
"""

    return message

def get_lyric_snapshot(song_name: str, artist_name: str, lyrics: str, png_name: str) -> str:
    lyric_snapshot: str = lyric_snapshotter.snapshot_lyrics(lyrics)
    html_content: str = lyric_snapshotter.add_to_html(song_name, artist_name, lyric_snapshot)
    out_img: str = lyric_snapshotter.turn_html_to_image(html_content, png_name)

    return out_img

def send_lyrics(message: Message):
    if message.audio:
        ARTIST: str = str(message.audio.performer)
        NAME: str = str(message.audio.title)
        
        full_message: str = get_lyrics_and_format(ARTIST, NAME)

        BOT.send_message(message.chat.id, full_message, parse_mode="Markdown")

    if message.text:
        print(message.text)
        splitted_msg: list[str] = str(message.text).split("-", maxsplit=1)
        ARTIST: str = splitted_msg[1]
        NAME: str = splitted_msg[0]

        ARTIST = remove_unwanted_spacing(ARTIST)
        NAME = remove_unwanted_spacing(NAME)
        
        full_message: str = get_lyrics_and_format(ARTIST, NAME)

        BOT.send_message(message.chat.id, full_message, parse_mode="Markdown")

def send_lyric_snapshot_img(message: Message):
    if message.audio:
        ARTIST: str = str(message.audio.performer)
        NAME: str = str(message.audio.title)

        SCRAPER: API.scraper = API.scraper(NAME, ARTIST)
        lyrics: str = SCRAPER.get_lyrics()

        img_path: str = get_lyric_snapshot(NAME, ARTIST, lyrics, str(message.chat.id))
        
        BOT.send_photo(message.chat.id, open(img_path, "rb"), timeout=180)
        
        lyric_snapshotter.delete_image(img_path)

    if message.text:
        splitted_msg: list[str] = str(message.text).split("-", maxsplit=1)
        ARTIST: str = splitted_msg[1]
        NAME: str = splitted_msg[0]

        ARTIST = remove_unwanted_spacing(ARTIST)
        NAME = remove_unwanted_spacing(NAME)
        
        SCRAPER: API.scraper = API.scraper(NAME, ARTIST)
        lyrics: str = SCRAPER.get_lyrics()

        img_path: str = get_lyric_snapshot(NAME, ARTIST, lyrics, str(message.chat.id))
        
        BOT.send_photo(message.chat.id, open(img_path, "rb"), timeout=180)

        lyric_snapshotter.delete_image(img_path)


@BOT.message_handler(commands=["start"])
def send_welcome(message):
    BOT.send_message(message.chat.id, """Hello, welcome To Song Lyrics Bot !
Send the name of your song with the artist like this: [title] - [artist] or send in the song itself to get the lyrics OR spotify-like lyric snapshot""")

@BOT.message_handler(func=lambda message: True, content_types=["text", "audio"])
def proceed(message: Message):
    global MESSAGE_OBJ
    KEYBOARD = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton(text="Lyrics", callback_data="lyrics")
    button2 = InlineKeyboardButton(text="Spotify-like Lyric Snapshot", callback_data="spotify")

    KEYBOARD.add(button1, button2)
    
    MESSAGE_OBJ = message

    BOT.send_message(message.chat.id, "Which action would you like to take ?", reply_markup=KEYBOARD)

@BOT.callback_query_handler(func=lambda call: True)
def handle_callback(call: CallbackQuery) -> None:
    if call.data == "lyrics":
        print("lyrics")
        send_lyrics(message=MESSAGE_OBJ)
    
    elif call.data == "spotify":
        print("spotify")
        send_lyric_snapshot_img(message=MESSAGE_OBJ)

BOT.infinity_polling()

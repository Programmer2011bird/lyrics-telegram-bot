TEST_LYRICS: str = """
Thought I almost died in my dream again (Baby, almost died)
Fightin' for my life, I couldn't breathe again
I'm fallin' in too deep (Oh, oh)
Without you, I can't sleep (Fallin' in)
'Cause my heart belongs to you
I'll risk it all for you
I want you next to me
This time, I'll never leave
I wanna share babies
Protection, we won't need
Your body next to me
Is just a memory
I'm fallin' in too deep, oh
Without you, I can't sleep
Insomnia relieve, oh
Talk to me, without you, I can't breathe
"""

def snapshot_lyrics(lyrics: str):
    splitted_lyrics: list[str] = lyrics.split("\n")
    
    for index in range(len(splitted_lyrics)):
        try:
            if splitted_lyrics[index] == "":
                splitted_lyrics.pop(index)

        except IndexError:
            pass

    snapshot_sentences: str = splitted_lyrics[0] + "\n" + splitted_lyrics[1]
    
    return snapshot_sentences

def add_to_html(content: str, html_file_name: str):
    # 1: Add the snapshotted lyrics to an html placeholder :
    # - just like spotify, but a nice, dark blue color
    # - On top, a big text showing the name of the song and another smaller one under it with the singer's name
    # - Fonts : Spotify Circular
    pass

def turn_html_to_image(html_file_name: str):
    # 2: turn the html to an image with imgkit
    pass


if __name__ == "__main__":
    snapshot_lyrics(TEST_LYRICS)

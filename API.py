from os import wait
from bs4 import BeautifulSoup
from lxml import etree, html
import requests


class scraper: 
    def __init__(self, song_name: str, artist_name: str) -> None:
        self.SONG_NAME: str = song_name.lower().replace(" ", "-")
        self.ARTIST_NAME: str = artist_name.lower().capitalize().replace(" ", "-")
        self.BASE_URL: str = f"https://genius.com/{self.ARTIST_NAME}-{self.SONG_NAME}-lyrics"

        self.headers = {
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br, zstd",   
            "Accept-Language" : "en-US,en;q=0.5",
            "Connection" : "keep-alive",
            "Cookie": "",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0"
        }

        self.response = requests.get(self.BASE_URL, headers=self.headers)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.dom = etree.HTML(str(self.soup))

    def get_lyrics(self) -> str:
        lyricsPreview = self.dom.xpath("/html/body/div[1]/main/div[2]/div[3]/div/div/div[1]/div")[0]
        lyricsPreview = str(BeautifulSoup(html.tostring(lyricsPreview), "html.parser").text)
        
        lyrics_containter = self.soup.find_all("div", attrs={"data-lyrics-container":"true"})        
        full_lyrics = ""

        for lyric in lyrics_containter:
            newlines = lyric.find_all("br")

            for newline in newlines:
                newline.replace_with("\n")

            lyric = str(lyric.text)
            lyric = lyric.replace(lyricsPreview, "")

            full_lyrics += lyric

        return full_lyrics

    def get_metadata(self) -> dict[str, str]:
        NAME: str = self.dom.xpath("/html/body/div[1]/main/div[1]/div[3]/div/div[1]/div[1]/h1")[0]
        ARTIST: str = self.dom.xpath("/html/body/div[1]/main/div[1]/div[3]/div/div[1]/div[1]/div[1]")[0]
        ALBUM_NAME: str = self.dom.xpath("/html/body/div[1]/main/div[1]/div[3]/div/div[1]/div[2]/div[1]/div")[0]
        RELEASE_DATE: str = self.dom.xpath("/html/body/div[1]/main/div[1]/div[3]/div/div[1]/div[2]/div[2]/span[1]")[0]
        
        self.METADATA: dict[str, str] = {
            "name": BeautifulSoup(html.tostring(NAME), "html.parser").text,
            "artist": BeautifulSoup(html.tostring(ARTIST), "html.parser").text,
            "album_name": BeautifulSoup(html.tostring(ALBUM_NAME), "html.parser").text,
            "release_date": BeautifulSoup(html.tostring(RELEASE_DATE), "html.parser").text
        }

        return self.METADATA


if __name__ == "__main__":
    SCRAPER: scraper = scraper("timeless", "the weeknd")
    print(SCRAPER.get_lyrics())
    print(SCRAPER.get_metadata())

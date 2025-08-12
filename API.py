from bs4 import BeautifulSoup
import requests

#TODO: Clean up the output
class scraper: 
    def __init__(self, song_name: str, artist_name: str) -> None:
        self.SONG_NAME: str = song_name.lower().replace(" ", "-")
        self.ARTIST_NAME: str = artist_name.lower().replace(" ", "-")
        self.BASE_URL: str = f"https://genius.com/{self.ARTIST_NAME}-{self.SONG_NAME}-lyrics"

        self.headers = {
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br, zstd",   
            "Accept-Language" : "en-US,en;q=0.5",
            "Connection" : "keep-alive",
            "Cookie": ""
        }

        self.response = requests.get(self.BASE_URL, headers=self.headers)
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def get_lyrics(self) -> str:
        lyricsPreview = self.soup.find("div", attrs={"class":"LyricsHeader__Container-sc-5e4b7146-1 hFsUgC"})
        lyricsPreview = str(lyricsPreview.text)
        
        lyrics = self.soup.find("div", attrs={"class":"Lyrics__Container-sc-39b434ea-1 gHGicG"})
        
        newlines = lyrics.find_all("br")
        
        for newline in newlines:
            newline.replace_with("\n")

        lyrics = str(lyrics.text)
        lyrics = lyrics.replace(lyricsPreview, "")

        return lyrics


if __name__ == "__main__":
    SCRAPER: scraper = scraper("Lovers Rock", "TV girl")
    SCRAPER.get_lyrics()

from bs4 import BeautifulSoup
import requests


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
            "Cookie": "",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0"
        }

        self.response = requests.get(self.BASE_URL, headers=self.headers)
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def get_lyrics(self) -> str:
        lyricsPreview = self.soup.find("div", attrs={"class":"LyricsHeader__Container-sc-5e4b7146-1 hFsUgC"})
        lyricsPreview = str(lyricsPreview.text)
        
        lyrics_containter = self.soup.find_all("div", attrs={"class":"Lyrics__Container-sc-39b434ea-1 gHGicG"})
        
        full_lyrics = ""

        for lyric in lyrics_containter:
            newlines = lyric.find_all("br")

            for newline in newlines:
                newline.replace_with("\n")

            lyric = str(lyric.text)
            lyric = lyric.replace(lyricsPreview, "")

            full_lyrics += lyric

        return full_lyrics

    def get_metadata(self):
        # Name - Artist - album picture - album name - release date
        metadata_header = self.soup.find("div", attrs={"class":"SongHeader-desktop__Information-sc-9f88acaa-5 coXjzV"})
        
        NAME: str = metadata_header.find(
            "h1", attrs={"class":"SongHeader-desktop__Title-sc-9f88acaa-9 fOveOw"}).text
        ARTIST: str = metadata_header.find(
            "div", attrs={"class":"SongHeader-desktop__CreditList-sc-9f88acaa-16 ghBjqh"}).text
        ALBUM_NAME: str = metadata_header.find_all(
            "div", attrs={"class":"HoverMarquee__InnerContainer-sc-9471fa5b-2 lnIdYT"})[1].text
        RELEASE_DATE: str = metadata_header.find(
            "span", attrs={"class":"LabelWithIcon__Container-sc-a1922d73-0 gYaIth MetadataStats__LabelWithIcon-sc-8a5f771a-3 izFOFo"}).text
        # IMAGE = self.soup.find("img", attrs={"class":"SizedImage__Image-sc-39a204ed-1 dycjBx SongHeader-desktop__SizedImage-sc-9f88acaa-15 bMLwec"})

        print(NAME)
        print(ARTIST)
        print(ALBUM_NAME)
        print(RELEASE_DATE)
        # print(IMAGE.attrs)
        # TODO: Fix the problem with getting the image src


if __name__ == "__main__":
    SCRAPER: scraper = scraper("Lovers rock", "TV girl")
    SCRAPER.get_metadata()

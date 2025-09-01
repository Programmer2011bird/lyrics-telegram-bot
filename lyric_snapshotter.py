import imgkit
import os


def snapshot_lyrics(lyrics: str) -> str:
    splitted_lyrics: list[str] = lyrics.split("\n")
    
    for index in range(len(splitted_lyrics)):
        try:
            if splitted_lyrics[index] == "":
                splitted_lyrics.pop(index)

        except IndexError:
            pass

    snapshot_sentences: str = f"""
<span>{splitted_lyrics[0]}</span>
</br>
</br>
<span>{splitted_lyrics[1]}</span> 
</br>
</br>
<span>{splitted_lyrics[2]}</span>"""
    
    return snapshot_sentences

def add_to_html(name: str, artist_name: str, lyrics: str) -> str:
    HTML_PLACEHOLDER: str = """
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Lyrics Snapshot</title>

<style>
  @font-face {
    font-family: 'SpotifyCircular';
    src: url('CircularStd-Book.woff2') format('woff2');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
  }
  @font-face {
    font-family: 'SpotifyCircular';
    src: url('CircularStd-Bold.woff2') format('woff2');
    font-weight: 700;
    font-style: normal;
    font-display: swap;
  }

  html,body { height:100%; margin:0; }
  body{
    background: #0a2746;
    font-family: 'SpotifyCircular', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    color:#e9f6ff;
    display:flex;
    align-items:center;
    justify-content:center;
  }

  .snapshot{
    width:900px;
    height:520px;
    padding:36px; box-sizing:border-box;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    box-shadow: 0 18px 40px rgba(3,10,30,0.65);
    position:relative;
    overflow:hidden;
    display:flex;
    gap:28px;
    align-items:flex-start;
    justify-content:flex-start;
  }

  .left{
    width:130px;
    height:130px;
    border-radius:18px;
    background: linear-gradient(135deg,#0b3b6b,#06314f);
    box-shadow: inset 0 -6px 18px rgba(0,0,0,0.25);
    display:flex;
    align-items:center;
    justify-content:center;
    flex: 0 0 130px;
    color: white;
  }

  .bi-logo {
    font-size:64px; /* size of the icon */
    line-height:1;
    width:64px;
    height:64px;
  }

  .content{
    flex:1 1 auto;
    min-width:0;
  }

  .meta{
    margin-bottom:18px;
  }
  .title{
    font-size:44px;
    font-weight:700;
    line-height:1;
    letter-spacing:-0.01em;
    color:#ffffff;
    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
  }
  .artist{
    margin-top:6px;
    font-size:18px;
    font-weight:400;
    color:#bfe6ff;
    opacity:0.95;
  }

  .lyrics{
    margin-top:14px;
    font-size:30px;
    font-weight:400;
    line-height:1.28;
    color:#dff5ff;
    max-width:100%;
  }

  .lyrics p{
    margin:0 0 10px 0;
    display:-webkit-box;
    -webkit-line-clamp:2;
    -webkit-box-orient:vertical;
    overflow:hidden;
    text-overflow:ellipsis;
  }

  .footer{
    position:absolute;
    right:28px;
    bottom:24px;
    font-size:12px;
    color:#9fc7e8;
    opacity:0.85;
  }
</style>
</head>
""" + f"""
<body>
  <div class="snapshot">
    <div class="content">
      <div class="meta">
        <div class="title">{name}</div>
        <div class="artist">{artist_name}</div>
      </div>
      <div class="lyrics">
        {lyrics}
      </div>
    </div>

    <div class="footer">Lyrics • Snapshot</div>
  </div>
</body>
</html>"""
    with open("test.html", "w+") as file:
        file.write(HTML_PLACEHOLDER)

    return HTML_PLACEHOLDER

def turn_html_to_image(content: str, out_image_name: str) -> str:
    options = {"format":"png","width":"900","height":"520","disable-smart-width":""}

    imgkit.from_string(content, f"./{out_image_name}.png", options)

    return f"./{out_image_name}.png"

def delete_image(image_path: str) -> None:
    os.remove(image_path)

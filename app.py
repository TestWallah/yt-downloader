import yt_dlp

link = input("Video Link Paste Karein: ")

options = {
    'format': 'best[height<=240]', 
    'outtmpl': '%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(options) as ydl:
    ydl.download([link])

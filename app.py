import streamlit as st
import yt_dlp
import os
import subprocess

st.title("🚀 Super Compressed 2x Downloader")

url = st.text_input("YouTube Link Dalein:")

if st.button("Download & Compress"):
    if url:
        with st.spinner('Pehle download ho raha hai, phir 2x speed aur compress hoga... Isme 1-2 minute lagenge.'):
            try:
                # 1. Download 240p Video
                ydl_opts = {
                    'format': 'best[height<=240]',
                    'outtmpl': 'input_video.mp4',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # 2. FFMPEG se 2x Speed aur Compression (CRF 28 se size kam hota hai)
                # Command: Video speed 2x, Audio speed 2x, Quality stable
                cmd = [
                    'ffmpeg', '-i', 'input_video.mp4',
                    '-filter_complex', "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]",
                    '-map', "[v]", '-map', "[a]",
                    '-vcodec', 'libx264', '-crf', '28', 
                    'output_2x.mp4'
                ]
                subprocess.run(cmd, check=True)

                # 3. Download Button
                with open("output_2x.mp4", "rb") as f:
                    st.success("Video 2x Speed aur Compress ho gayi!")
                    st.download_button("📲 Gallery Mein Save Karein", f, file_name="compressed_2x.mp4")
                
                # Safai (Files delete karna)
                os.remove("input_video.mp4")
                os.remove("output_2x.mp4")

            except Exception as e:
                st.error(f"Error: {e}. Shayad packages.txt setup nahi hua.")

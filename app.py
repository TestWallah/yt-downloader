import streamlit as st
import yt_dlp
import os

# Mobile UI setting
st.set_page_config(page_title="Mobile YT Downloader", layout="centered")

st.markdown("<h1 style='text-align: center; color: red;'>📲 Mobile YT Downloader</h1>", unsafe_allow_html=True)

url = st.text_input("YouTube Link Paste Karein:", placeholder="https://youtube.com/...")

if url:
    with st.spinner('Checking formats...'):
        try:
            # Browser ki tarah request bhejne ke liye options
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'video')
                formats = info.get('formats', [])

            # Professional Dropdown
            options = []
            for f in formats:
                # Sirf MP4 formats dikhayega
                if f.get('ext') == 'mp4' and f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    res = f.get('height')
                    size = f.get('filesize') or f.get('filesize_approx')
                    if size:
                        size_text = f"{round(size / (1024*1024), 1)} MB"
                        options.append({"label": f"🎬 {res}p ({size_text})", "url": f.get('url')})

            if options:
                # Quality choose karne ka option
                choice = st.selectbox("Quality Chuniye:", options, format_func=lambda x: x['label'])
                
                # Sabse bada badlav: Direct Link dena
                st.success("Download Link Taiyar Hai!")
                
                # Ye button seedha video file open karega browser mein
                st.markdown(f"""
                    <a href="{choice['url']}" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #FF0000; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; font-size: 18px;">
                            🚀 Download Start Karein
                        </div>
                    </a>
                    <p style="text-align: center; font-size: 12px; margin-top: 10px;">
                    Note: Link khulne ke baad 3-dots par click karke Download dabayein.
                    </p>
                """, unsafe_allow_html=True)
            else:
                st.error("Is video ke liye koi MP4 format nahi mila.")

        except Exception as e:
            st.error("YouTube block kar raha hai. Kuch der baad try karein ya dusri video link dalein.")


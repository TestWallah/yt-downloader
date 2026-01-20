import streamlit as st
import yt_dlp
import os

st.title("YouTube 240p Downloader")

# Link input
url = st.text_input("YouTube Video Link Yahan Paste Karein:")

if st.button("Download Video"):
    if url:
        with st.spinner('Processing...'):
            try:
                # Download settings
                ydl_opts = {
                    'format': 'best[height<=240]',
                    'outtmpl': 'video.mp4',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Download button for user
                with open("video.mp4", "rb") as file:
                    st.download_button(
                        label="Mobile Gallery Mein Save Karein",
                        data=file,
                        file_name="video_240p.mp4",
                        mime="video/mp4"
                    )
                os.remove("video.mp4") # Clean up
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Pehle link toh daalo!")

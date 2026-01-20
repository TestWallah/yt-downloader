import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Smart YT Downloader", page_icon="📥")
st.title("📥 Smart YouTube Downloader")

url = st.text_input("YouTube Video Link Yahan Paste Karein:")

if url:
    with st.spinner('Formats dhoond raha hoon...'):
        try:
            # Video details aur formats nikalne ke liye
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                video_title = info.get('title', 'video')

            # Sirf kaam ke formats filter karna (Video + Audio wale)
            options = []
            for f in formats:
                # Sirf wo formats jinme video aur audio dono ho aur extension mp4 ho
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('ext') == 'mp4':
                    res = f.get('height')
                    size = f.get('filesize')
                    if size:
                        size_mb = round(size / (1024 * 1024), 2)
                        label = f"{res}p - ({size_mb} MB)"
                    else:
                        label = f"{res}p - (Size Unknown)"
                    
                    options.append({"label": label, "id": f.get('format_id')})

            if options:
                # User ko choice dena
                selection = st.selectbox("Apni Quality Chuniye:", options, format_func=lambda x: x['label'])
                
                if st.button("Download Start Karein"):
                    with st.spinner('Server par download ho raha hai...'):
                        final_opts = {
                            'format': selection['id'],
                            'outtmpl': 'downloaded_video.mp4',
                        }
                        with yt_dlp.YoutubeDL(final_opts) as ydl:
                            ydl.download([url])
                        
                        # Mobile Download Button
                        with open("downloaded_video.mp4", "rb") as file:
                            st.download_button(
                                label="📲 Gallery Mein Save Karein",
                                data=file,
                                file_name=f"{video_title}.mp4",
                                mime="video/mp4"
                            )
                        os.remove("downloaded_video.mp4")
            else:
                st.error("Is video ke liye koi MP4 format nahi mila.")

        except Exception as e:
            st.error(f"Kuch galat hua: {e}")
else:
    st.info("Link daaliye upar, formats apne aap niche aa jayenge.")

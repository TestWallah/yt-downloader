import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Pro YT Downloader", page_icon="🚀", layout="centered")

# Custom CSS for professional look
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #FF0000; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Professional YouTube Downloader")
st.write("Video link dalein aur apni manpasand quality mein download karein.")

url = st.text_input("", placeholder="Paste YouTube link here...")

if url:
    with st.spinner('Scanning video formats...'):
        try:
            # Advanced options to bypass 403 Forbidden
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
                # Browser impersonation
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'video')
                video_thumbnail = info.get('thumbnail')
                formats = info.get('formats', [])

            # Video Preview
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(video_thumbnail, use_container_width=True)
            with col2:
                st.subheader(video_title)

            options = []
            for f in formats:
                # Sirf MP4 aur Video+Audio wale formats
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    res = f.get('height')
                    ext = f.get('ext')
                    
                    # File size calculate karna (agar unknown hai toh estimate lagana)
                    filesize = f.get('filesize') or f.get('filesize_approx')
                    
                    if filesize:
                        size_mb = round(filesize / (1024 * 1024), 2)
                        label = f"🎬 {res}p | {ext.upper()} | {size_mb} MB"
                    else:
                        label = f"🎬 {res}p | {ext.upper()} | Size: N/A"
                    
                    options.append({"label": label, "id": f.get('format_id')})

            if options:
                # Newest quality at the top
                options.reverse() 
                selection = st.selectbox("Select Quality & Size:", options, format_func=lambda x: x['label'])
                
                if st.button("Download to Server"):
                    with st.spinner('Downloading to server... Please wait.'):
                        final_filename = "pro_download.mp4"
                        final_opts = {
                            'format': selection['id'],
                            'outtmpl': final_filename,
                            'nocheckcertificate': True,
                            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                        }
                        
                        with yt_dlp.YoutubeDL(final_opts) as ydl:
                            ydl.download([url])
                        
                        with open(final_filename, "rb") as file:
                            st.success("Download Ready!")
                            st.download_button(
                                label="📥 Click to Save in Gallery",
                                data=file,
                                file_name=f"{video_title}.mp4",
                                mime="video/mp4"
                            )
                        os.remove(final_filename)
            else:
                st.error("No suitable MP4 formats found.")

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Tip: Kuch videos restricted hoti hain. Ek baar dusri video try karein.")

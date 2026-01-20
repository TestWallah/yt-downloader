import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Ultimate YT Downloader", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF0000;'>🎬 Ultimate Video Downloader</h1>", unsafe_allow_html=True)

url = st.text_input("YouTube Video Link Paste Karein:", placeholder="https://youtube.com/watch?v=...")

if url:
    with st.spinner('Fetching all available qualities...'):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'video')
                formats = info.get('formats', [])

            # Professional Formats Filtering
            unique_resolutions = {}
            for f in formats:
                res = f.get('height')
                if res and res not in unique_resolutions:
                    # MB calculate karna (approx ya exact)
                    size = f.get('filesize') or f.get('filesize_approx') or 0
                    size_mb = round(size / (1024 * 1024), 1)
                    ext = f.get('ext', 'mp4')
                    
                    label = f"⭐ {res}p | {ext.upper()} | ~{size_mb} MB"
                    unique_resolutions[res] = {"label": label, "id": f.get('format_id')}

            if unique_resolutions:
                # Resolutions ko sahi order mein lagana (High to Low)
                sorted_res = sorted(unique_resolutions.keys(), reverse=True)
                selection_list = [unique_resolutions[r] for r in sorted_res]
                
                choice = st.selectbox("Apni Quality Chuniye:", selection_list, format_func=lambda x: x['label'])
                
                if st.button("Download Video Now"):
                    with st.spinner('Downloading & Processing... (Mobile users wait for button)'):
                        output_name = "final_video.mp4"
                        
                        # Best Video + Best Audio ko merge karke MP4 banane ki setting
                        final_download_opts = {
                            'format': f"{choice['id']}+bestaudio/best",
                            'outtmpl': output_name,
                            'merge_output_format': 'mp4',
                            'postprocessors': [{'key': 'FFMPEGVideoConvertor', 'preferredformat': 'mp4'}],
                        }
                        
                        with yt_dlp.YoutubeDL(final_download_opts) as ydl:
                            ydl.download([url])
                        
                        if os.path.exists(output_name):
                            with open(output_name, "rb") as file:
                                st.success(f"✅ {video_title} Taiyar Hai!")
                                st.download_button(
                                    label="📲 Click to Save in Gallery",
                                    data=file,
                                    file_name=f"{video_title}.mp4",
                                    mime="video/mp4"
                                )
                            os.remove(output_name)
            else:
                st.error("Koi quality nahi mili. Link check karein.")

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Tip: Agar 403 Forbidden aaye toh 1-2 minute baad try karein.")

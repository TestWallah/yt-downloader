import streamlit as st
import yt_dlp

st.set_page_config(page_title="Ultimate YT Downloader", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF0000;'>🎬 Pro Video Downloader</h1>", unsafe_allow_html=True)

url = st.text_input("YouTube Link Paste Karein:", placeholder="https://youtube.com/...")

if url:
    with st.spinner('Checking all qualities...'):
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
                st.image(info.get('thumbnail'), width=300)

            options = []
            for f in formats:
                # Sirf wo formats jinme video aur audio dono pehle se ho
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    res = f.get('height')
                    ext = f.get('ext')
                    size = f.get('filesize') or f.get('filesize_approx')
                    
                    if res and size:
                        size_mb = f"{round(size / (1024 * 1024), 1)} MB"
                        label = f"🎬 {res}p | {ext.upper()} | {size_mb}"
                        options.append({"label": label, "url": f.get('url')})

            if options:
                # Sabse achi quality upar dikhane ke liye
                options.reverse()
                # Pehle se maujood list ko saaf dikhane ke liye dropdown
                choice = st.selectbox("Apni Quality Chuniye:", options, format_func=lambda x: x['label'])
                
                st.success("Download Link Taiyar Hai!")
                
                # Direct Download Button
                st.markdown(f"""
                    <a href="{choice['url']}" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #28a745; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; font-size: 18px; margin-top: 10px;">
                            📥 Save to Gallery (Direct)
                        </div>
                    </a>
                """, unsafe_allow_html=True)
                st.info("Tip: Link khulne par video par long press karein ya 3-dots se Download dabayein.")
            else:
                st.error("Is video ke liye koi direct format nahi mila.")

        except Exception as e:
            st.error(f"Kuch dikkat aayi: {e}")

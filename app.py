import streamlit as st
import yt_dlp

st.set_page_config(page_title="Pro YT Downloader", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF0000;'>🚀 Professional YT Downloader</h1>", unsafe_allow_html=True)
st.write("Link paste karein aur direct mobile gallery mein save karein.")

url = st.text_input("YouTube Link Yahan Dalein:", placeholder="https://youtube.com/...")

if url:
    with st.spinner('Scanning all qualities...'):
        try:
            # Bypass settings
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                # Thumbnail aur Title dikhana professional lagta hai
                st.image(info.get('thumbnail'), width=300)
                st.subheader(info.get('title'))

            options = []
            for f in formats:
                # Sirf wo formats jinme Video+Audio dono pehle se jude hon (Mobile safe)
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('ext') == 'mp4':
                    res = f.get('height')
                    size = f.get('filesize') or f.get('filesize_approx')
                    if size:
                        size_mb = f"{round(size / (1024 * 1024), 1)} MB"
                        options.append({"label": f"🎬 {res}p - ({size_mb})", "url": f.get('url')})

            if options:
                # High quality upar dikhane ke liye reverse
                options.reverse()
                choice = st.selectbox("Quality Chuniye:", options, format_func=lambda x: x['label'])
                
                st.success("Download Link Taiyar Hai!")
                
                # Professional Download Button
                st.markdown(f"""
                    <a href="{choice['url']}" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #25D366; color: white; padding: 15px; text-align: center; border-radius: 10px; font-weight: bold; font-size: 18px; margin-top: 10px;">
                            📥 Save to Gallery (Direct)
                        </div>
                    </a>
                    <p style='text-align: center; color: gray; font-size: 12px; margin-top: 5px;'>
                    Tip: Link khulne par 3-dots par click karke Download dabayein.
                    </p>
                """, unsafe_allow_html=True)
            else:
                st.error("Is video ke liye koi direct MP4 format nahi mila. Dusri video try karein.")

        except Exception as e:
            st.error("YouTube block kar raha hai. 1-2 minute baad refresh karke try karein.")
i

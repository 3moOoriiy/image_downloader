import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="تحميل الصور JPG", layout="centered")

# App title and description
st.title("🖼️ تحميل الصور مباشرة بصيغة JPG")
st.write("الصق روابط الصور أو ارفع ملف .txt يحتوي على الروابط (كل سطر = رابط).")

# Input options
urls_text = st.text_area("📋 الصق روابط الصور هنا:")
uploaded_file = st.file_uploader("📁 أو ارفع ملف روابط", type=["txt"])

# Load URLs from uploaded file
if uploaded_file is not None:
    urls_text = uploaded_file.read().decode("utf-8")

# Download button
if st.button("📥 جلب الصور"):
    if not urls_text.strip():
        st.warning("الرجاء إدخال روابط أولًا.")
    else:
        image_urls = [url.strip() for url in urls_text.strip().splitlines() if url.strip()]
        
        # Progress bar
        progress_bar = st.progress(0)
        total_images = len(image_urls)
        
        for i, url in enumerate(image_urls):
            try:
                # Update progress
                progress_bar.progress((i + 1) / total_images)
                
                # Custom headers to avoid blocking
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://www.google.com",
                    "DNT": "1",
                    "Connection": "keep-alive",
                }
                
                # Download image
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    # Open and convert image
                    image = Image.open(BytesIO(response.content)).convert("RGB")
                    
                    # Display image
                    st.image(image, caption=f"الصورة رقم {i+1}", use_column_width=True)
                    
                    # Prepare download button
                    img_buffer = BytesIO()
                    image.save(img_buffer, format="JPEG")
                    img_buffer.seek(0)
                    
                    # Add download button
                    st.download_button(
                        label=f"📸 تحميل الصورة {i+1} كـ JPG",
                        data=img_buffer,
                        file_name=f"image_{i+1}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error(f"❌ فشل تحميل الصورة {i+1} - الحالة: {response.status_code}")
            except Exception as e:
                st.error(f"⚠️ خطأ في تحميل الصورة رقم {i+1}: {e}")
        
        # Clear progress bar when done
        progress_bar.empty()

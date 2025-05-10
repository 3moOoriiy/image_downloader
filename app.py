import streamlit as st
import requests
import os
import zipfile
from io import BytesIO

st.set_page_config(page_title="تحميل الصور من روابط", layout="centered")

st.title("🖼️ أداة تحميل الصور من روابط")
st.write("قم بلصق روابط الصور (كل رابط في سطر) أو ارفع ملف .txt يحتوي على الروابط.")

# إدخال الروابط يدويًا أو من ملف
urls_text = st.text_area("📋 الصق روابط الصور هنا:")

uploaded_file = st.file_uploader("📁 أو ارفع ملف نصي يحتوي على روابط", type=["txt"])

# تحميل الروابط من الملف إذا تم رفعه
if uploaded_file is not None:
    urls_text = uploaded_file.read().decode("utf-8")

# زر التنفيذ
if st.button("🚀 تحميل الصور وضغطها"):
    if not urls_text.strip():
        st.warning("الرجاء إدخال روابط الصور أولاً.")
    else:
        image_urls = [url.strip() for url in urls_text.strip().splitlines() if url.strip()]
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for i, url in enumerate(image_urls):
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        filename = f"image_{i+1}.webp"
                        zip_file.writestr(filename, response.content)
                    else:
                        st.error(f"❌ فشل تحميل الصورة رقم {i+1}")
                except Exception as e:
                    st.error(f"⚠️ خطأ في تحميل الصورة رقم {i+1}: {e}")

        st.success("✅ تم تحميل الصور وضغطها!")
        st.download_button(
            label="📦 تحميل ملف ZIP",
            data=zip_buffer.getvalue(),
            file_name="downloaded_images.zip",
            mime="application/zip"
        )

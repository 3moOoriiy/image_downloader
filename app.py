import streamlit as st
import pandas as pd
import requests
import os
from zipfile import ZipFile
from io import BytesIO

st.set_page_config(page_title="تحميل الصور من Excel", layout="centered")
st.title("📥 تحميل الصور من ملف Excel وضغطها في ZIP")

uploaded_file = st.file_uploader("📁 ارفع ملف Excel يحتوي على روابط الصور (عمود اسمه url)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if "url" not in df.columns:
            st.error("❌ تأكد أن اسم العمود في ملف Excel هو 'url'")
        else:
            image_urls = df["url"].dropna().tolist()
            zip_buffer = BytesIO()

            with ZipFile(zip_buffer, "w") as zipf:
                for i, url in enumerate(image_urls):
                    try:
                        headers = {
                            "User-Agent": "Mozilla/5.0"
                        }
                        response = requests.get(url, headers=headers, timeout=20)
                        if response.status_code == 200:
                            zipf.writestr(f"image_{i+1}.jpg", response.content)
                        else:
                            st.warning(f"⚠️ فشل تحميل الصورة {i+1} - الحالة: {response.status_code}")
                    except Exception as e:
                        st.warning(f"⚠️ خطأ في تحميل الصورة {i+1}: {e}")

            st.success("✅ تم تحميل الصور وضغطها!")
            st.download_button(
                label="📦 تحميل ملف ZIP",
                data=zip_buffer.getvalue(),
                file_name="downloaded_images.zip",
                mime="application/zip"
            )
    except Exception as e:
        st.error(f"❌ خطأ في قراءة الملف: {e}")

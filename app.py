import streamlit as st
import requests
import zipfile
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="تحميل الصور من روابط", layout="centered")

st.title("🖼️ أداة تحميل الصور من روابط")
st.write("قم بلصق روابط الصور (كل رابط في سطر) أو ارفع ملف .txt يحتوي على الروابط.")

# إدخال الروابط يدويًا أو من ملف
urls_text = st.text_area("📋 الصق روابط الصور هنا:")

uploaded_file = st.file_uploader("📁 أو ارفع ملف نصي يحتوي على روابط", type=["txt"])

if uploaded_file is not None:
    urls_text = uploaded_file.read().decode("utf-8")

if st.button("🚀 تحميل الصور وتحويلها إلى JPG وضغطها"):
    if not urls_text.strip():
        st.warning("الرجاء إدخال روابط الصور أولاً.")
    else:
        image_urls = [url.strip() for url in urls_text.strip().splitlines() if url.strip()]
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for i, url in enumerate(image_urls):
                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    }
                    response = requests.get(url, headers=headers, timeout=20)
                    if response.status_code == 200:
                        # فتح الصورة ودعم الشفافية
                        image = Image.open(BytesIO(response.content)).convert("RGBA")
                        bg = Image.new("RGB", image.size, (255, 255, 255))  # خلفية بيضاء
                        image = Image.alpha_composite(bg.convert("RGBA"), image).convert("RGB")

                        img_bytes = BytesIO()
                        image.save(img_bytes, format="JPEG", quality=95)
                        img_bytes.seek(0)

                        zip_file.writestr(f"image_{i+1}.jpg", img_bytes.read())
                    else:
                        st.error(f"❌ فشل تحميل الصورة رقم {i+1} (رمز الحالة: {response.status_code})")
                except Exception as e:
                    st.error(f"⚠️ خطأ في تحميل الصورة رقم {i+1}: {e}")

        st.success("✅ تم تحميل الصور وتحويلها إلى JPG بخلفية بيضاء وضغطها!")
        st.download_button(
            label="📦 تحميل ملف ZIP",
            data=zip_buffer.getvalue(),
            file_name="downloaded_images_jpg.zip",
            mime="application/zip"
        )

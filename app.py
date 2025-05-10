import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="تحميل الصور JPG", layout="centered")

st.title("🖼️ تحميل الصور مباشرة بصيغة JPG")
st.write("الصق روابط الصور أو ارفع ملف .txt يحتوي على الروابط (كل سطر = رابط).")

urls_text = st.text_area("📋 الصق روابط الصور هنا:")

uploaded_file = st.file_uploader("📁 أو ارفع ملف روابط", type=["txt"])
if uploaded_file is not None:
    urls_text = uploaded_file.read().decode("utf-8")

if st.button("📥 جلب الصور"):
    if not urls_text.strip():
        st.warning("الرجاء إدخال روابط أولًا.")
    else:
        image_urls = [url.strip() for url in urls_text.strip().splitlines() if url.strip()]

        for i, url in enumerate(image_urls):
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=15)

                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content)).convert("RGB")
                    st.image(image, caption=f"الصورة رقم {i+1}", use_column_width=True)

                    # حفظ الصورة مؤقتًا بصيغة JPG
                    img_buffer = BytesIO()
                    image.save(img_buffer, format="JPEG")
                    img_buffer.seek(0)

                    st.download_button(
                        label=f"📸 تحميل الصورة {i+1} كـ JPG",
                        data=img_buffer,
                        file_name=f"image_{i+1}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error(f"❌ فشل تحميل الصورة {i+1} - الحالة: {response.status_code}")
            except Exception as e:
                st.error(f"⚠️ خطأ في تحميل الصورة {i+1}: {e}")

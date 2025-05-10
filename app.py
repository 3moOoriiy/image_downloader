import streamlit as st
import requests
import zipfile
from io import BytesIO
from PIL import Image

# Page configuration
st.set_page_config(page_title="Image Downloader from URLs", layout="centered")

# Title and description
st.title("🖼️ Image Downloader from URLs")
st.write("Paste image URLs (one per line) or upload a .txt file containing the URLs.")

# Input section
urls_text = st.text_area("📋 Paste image URLs here:")

uploaded_file = st.file_uploader("📁 Or upload a .txt file with image URLs", type=["txt"])

if uploaded_file is not None:
    urls_text = uploaded_file.read().decode("utf-8")

# Download button
if st.button("🚀 Download and Convert Images to JPG (ZIP)"):
    if not urls_text.strip():
        st.warning("Please enter image URLs first.")
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
                        # Open the image and convert to JPG with white background if transparent
                        image = Image.open(BytesIO(response.content)).convert("RGBA")
                        bg = Image.new("RGB", image.size, (255, 255, 255))  # White background
                        image = Image.alpha_composite(bg.convert("RGBA"), image).convert("RGB")

                        img_bytes = BytesIO()
                        image.save(img_bytes, format="JPEG", quality=95)
                        img_bytes.seek(0)

                        zip_file.writestr(f"image_{i+1}.jpg", img_bytes.read())
                    else:
                        st.error(f"❌ Failed to download image #{i+1} (Status code: {response.status_code})")
                except Exception as e:
                    st.error(f"⚠️ Error downloading image #{i+1}: {e}")

        st.success("✅ Images downloaded, converted to JPG, and zipped successfully!")
        st.download_button(
            label="📦 Download ZIP file",
            data=zip_buffer.getvalue(),
            file_name="downloaded_images_jpg.zip",
            mime="application/zip"
        )

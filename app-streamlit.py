import streamlit as st
from PIL import Image
import io
import zipfile

st.title("WebP Image Optimiser")

uploaded_files = st.file_uploader(
    "Upload one or more images (JPG, PNG, WEBP)", 
    type=["jpg", "jpeg", "png", "webp"], 
    accept_multiple_files=True
)

def optimize_image(image_file):
    image = Image.open(image_file).convert("RGB")  # Convertimos para evitar errores con algunos formatos

    max_width = 1920
    if image.width > max_width:
        ratio = max_width / image.width
        new_size = (max_width, int(image.height * ratio))
        image = image.resize(new_size, Image.LANCZOS)

    buffer = io.BytesIO()
    image.save(buffer, format="webp", quality=75, method=6)
    buffer.seek(0)
    return buffer

if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            optimized = optimize_image(uploaded_file)
            filename = uploaded_file.name.rsplit('.', 1)[0] + ".webp"

            # Mostrar imagen y botón individual
            st.image(optimized, caption=filename, use_container_width=True)
            st.download_button(
                label=f"Download {filename}",
                data=optimized,
                file_name=filename,
                mime="image/webp"
            )

            # Agregar al ZIP
            zip_file.writestr(filename, optimized.read())

    zip_buffer.seek(0)
    st.download_button(
        label="Download all as ZIP",
        data=zip_buffer,
        file_name="optimised_images.zip",
        mime="application/zip"
    )

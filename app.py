from PIL import Image
import os

# Configuración
input_folder = "individual_input"
output_folder = "individual_output"
MAX_WIDTH = 1920
QUALITY = 75

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Extensiones válidas
valid_extensions = [".jpg", ".jpeg", ".png"]

# Procesar imágenes
for filename in os.listdir(input_folder):
    file_lower = filename.lower()
    if any(file_lower.endswith(ext) for ext in valid_extensions):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".webp"
        output_path = os.path.join(output_folder, output_filename)

        try:
            with Image.open(input_path) as img:
                # Convertir a RGB si es PNG con transparencia
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                original_width, original_height = img.size

                # Redimensionar si es necesario
                if original_width > MAX_WIDTH:
                    new_height = int((MAX_WIDTH / original_width) * original_height)
                    img = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)
                    print(f"📐 Redimensionado: {filename} de {original_width}px → {MAX_WIDTH}px de ancho")

                # Guardar en formato WebP
                img.save(output_path, "webp", quality=QUALITY, method=6)
                print(f"✅ Convertido a WebP: {filename} → {output_filename}")

        except Exception as e:
            print(f"❌ Error con {filename}: {e}")

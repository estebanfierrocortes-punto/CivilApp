import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
from streamlit_paste_button import paste_image_button as pbutton

# Configuración de la interfaz
st.set_page_config(page_title="CIVIL-OS PRO", layout="wide")
st.title("🏗️ CIVIL-OS: Análisis de Producción (Motor GPT-4o)")

# Conexión con OpenAI
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("🔑 Error: No se encontró la clave 'OPENAI_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# Panel de control lateral
with st.sidebar:
    st.header("⚙️ Ajustes de Fábrica")
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Obra Civil", "Cocinas"])
    medida_ref = st.number_input("Escala de referencia (m)", value=1.0)

# Zona de carga de archivos
st.divider()
col1, col2 = st.columns(2)

archivo_para_analizar = None

with col1:
    st.subheader("📋 Opción A: Pegar")
    btn_pegar = pbutton("Haga clic aquí y presione Ctrl+V")
    if btn_pegar.image_data is not None:
        archivo_para_analizar = btn_pegar.image_data

with col2:
    st.subheader("📂 Opción B: Subir")
    subido = st.file_uploader("Subir plano (Imagen o PDF)", type=['png', 'jpg', 'jpeg', 'pdf'])
    if subido is not None:
        if subido.type == "application/pdf":
            st.warning("Nota: Los PDFs se procesan mejor si son capturas de pantalla claras.")
            # Por estabilidad, recomendamos al usuario subir imágenes si el PDF falla
            archivo_para_analizar = subido 
        else:
            archivo_para_analizar = Image.open(subido)

# Procesamiento y visualización
if archivo_para_analizar is not None:
    # Si es una imagen (objeto PIL), la mostramos
    if isinstance(archivo_para_analizar, Image.Image):
        st.image(archivo_para_analizar, caption="Plano listo para análisis", width=800)
    
    if st.button("🚀 INICIAR ANÁLISIS DE PRODUCCIÓN"):
        try:
            with st.spinner("Analizando con GPT-4o..."):
                # Preparación de la imagen para OpenAI
                if not isinstance(archivo_para_analizar, Image.Image):
                    # Si es un PDF o bytes, necesitamos convertirlo (Sugerencia: usar capturas)
                    st.error("Para este análisis profesional, por favor use la opción de Pegar o suba una imagen (PNG/JPG).")
                else:
                    buffered = io.BytesIO()
                    archivo_para_analizar.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    prompt = (f"Actúa como Production Manager en {especialidad}. Escala: {medida_ref}m. "
                             "Genera una TABLA técnica de producción con: Pieza, Medidas (Largo x Ancho) y Materiales.")

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}
                            ]
                        }]
                    )
                    st.success("✅ Análisis Completo")
                    st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error técnico: {e}")

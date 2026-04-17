import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
from streamlit_paste_button import paste_image_button as pbutton

# 1. CONFIGURACIÓN Y CONEXIÓN
st.set_page_config(page_title="CIVIL-OS PRO", layout="wide")
st.title("🏗️ CIVIL-OS: Análisis de Producción (Motor GPT-4o)")

# Conexión con OpenAI
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("🔑 Falta la clave 'OPENAI_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 2. PANEL DE CONTROL (Sidebar)
with st.sidebar:
    st.header("⚙️ Ajustes")
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Obra Civil", "Cocinas"])
    medida_ref = st.number_input("Escala de referencia (m)", value=1.0)

# 3. INTERFAZ DE CARGA (Restaurada)
st.divider()
col1, col2 = st.columns(2)

archivo_final = None
es_pdf = False

with col1:
    st.subheader("📋 Opción A: Pegar")
    btn_pegar = pbutton("Haz clic aquí y presiona Ctrl+V")
    if btn_pegar.image_data is not None:
        archivo_final = btn_pegar.image_data
        es_pdf = False

with col2:
    st.subheader("📂 Opción B: Subir")
    subido = st.file_uploader("Arrastra imagen o PDF", type=['png', 'jpg', 'jpeg', 'pdf'])
    if subido is not None:
        if subido.type == "application/pdf":
            archivo_final = subido.getvalue()
            es_pdf = True
        else:
            archivo_final = Image.open(subido)
            es_pdf = False

# 4. PROCESAMIENTO
if archivo_final is not None:
    if not es_pdf:
        st.image(archivo_final, caption="Plano listo", width=700)
    else:
        st.success("📄 Documento PDF cargado y listo para análisis.")

    if st.button("🚀 INICIAR ANÁLISIS DE PRODUCCIÓN"):
        try:
            with st.spinner("ChatGPT analizando..."):
                # Preparar contenido para OpenAI
                if es_pdf:
                    # Nota: Para PDFs complejos, es mejor convertirlos a imagen antes, 
                    # pero GPT-4o puede intentar leer texto de archivos pequeños.
                    st.warning("El análisis de PDF directo es experimental. Si falla, toma una captura y pégala.")
                    # Por simplicidad en esta versión, tratamos el PDF como texto/datos si es posible
                    prompt_tecnico = f"Analiza este documento de {especialidad} y genera una tabla de despiece."
                    # (Lógica simplificada para esta versión)
                else:
                    # Convertir imagen a Base64
                    buffered = io.BytesIO()
                    archivo_final.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    prompt = (f"Actúa como Production Manager en {especialidad}. Escala: {medida_ref}m. "
                             "Genera una TABLA de producción con: Pieza, Medidas y Materiales.")

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
                    st.success("✅ Análisis Finalizado")
                    st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")

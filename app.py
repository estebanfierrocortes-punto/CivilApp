import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

st.set_page_config(page_title="CIVIL-OS", layout="wide")

# FUERZA LA CONEXIÓN ESTABLE
if "GOOGLE_API_KEY" in st.secrets:
    # Usamos transport='rest' para evitar el error 404 de v1beta
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
else:
    st.error("🔑 Falta la clave API en Secrets.")

st.title("🏗️ CIVIL-OS: Análisis de Producción")

if 'img_buffer' not in st.session_state:
    st.session_state.img_buffer = None

with st.sidebar:
    st.header("⚙️ Ajustes")
    medida_ref = st.number_input("Escala (m)", value=1.0)
    tipo = st.selectbox("Área", ["Ebanistería/Muebles", "Construcción"])

col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Opción 1: Pegar")
    res_paste = pbutton("Clic y Ctrl+V")
    if res_paste.image_data is not None:
        st.session_state.img_buffer = res_paste.image_data

with col2:
    st.subheader("📂 Opción 2: Subir")
    archivo = st.file_uploader("Imagen o PDF", type=['png', 'jpg', 'jpeg', 'pdf'])
    if archivo:
        if archivo.type == "application/pdf":
            st.session_state.img_buffer = archivo.getvalue()
            st.session_state.tipo_archivo = "pdf"
        else:
            st.session_state.img_buffer = Image.open(archivo)
            st.session_state.tipo_archivo = "img"

if st.session_state.img_buffer:
    if st.button("🚀 EJECUTAR ANÁLISIS DE MATERIALES"):
        try:
            # Especificamos el modelo sin prefijos de versión para mayor compatibilidad
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("Calculando..."):
                if getattr(st.session_state, 'tipo_archivo', "") == "pdf":
                    contenido = [{"mime_type": "application/pdf", "data": st.session_state.img_buffer}]
                else:
                    contenido = [st.session_state.img_buffer]
                
                prompt = f"Actúa como un experto Production Manager. Escala {medida_ref}m. Genera una lista técnica de materiales para {tipo}."
                
                respuesta = model.generate_content([prompt] + contenido)
                st.markdown("---")
                st.markdown(respuesta.text)
                
        except Exception as e:
            st.error(f"Error técnico: {e}")

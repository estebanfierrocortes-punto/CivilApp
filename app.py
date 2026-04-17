import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# Configuración básica
st.set_page_config(page_title="CIVIL-OS FREE", layout="wide")
st.title("🏗️ CIVIL-OS: Análisis de Producción (Gratis)")

# Conexión Directa y Forzada
if "GOOGLE_API_KEY" in st.secrets:
    # Esta línea es la que evita el error 404 al no definir versiones externas
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la clave en Secrets.")
    st.stop()

# Interfaz simplificada
with st.sidebar:
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Obra Civil"])
    medida_ref = st.number_input("Escala (m)", value=1.0)

# Carga de archivos
st.subheader("📸 Cargue su plano")
col1, col2 = st.columns(2)
archivo_final = None

with col1:
    btn_pegar = pbutton("Clic aquí y Ctrl+V")
    if btn_pegar.image_data is not None:
        archivo_final = btn_pegar.image_data

with col2:
    subido = st.file_uploader("O suba una imagen", type=['png', 'jpg', 'jpeg'])
    if subido:
        archivo_final = Image.open(subido)

if archivo_final:
    st.image(archivo_final, width=700)
    
    if st.button("🚀 INICIAR ANÁLISIS GRATUITO"):
        try:
            # Usamos el nombre del modelo sin sufijos extras
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = (f"Actúa como Production Manager en {especialidad}. Escala: {medida_ref}m. "
                     "Extrae una tabla con: Pieza, Medidas y Material sugerido.")
            
            # Procesamiento
            with st.spinner("Analizando plano..."):
                response = model.generate_content([prompt, archivo_final])
                st.success("Análisis terminado")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Si el error persiste, pruebe generar una clave API nueva en un proyecto de Google distinto.")

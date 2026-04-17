import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# Configuración de página
st.set_page_config(page_title="CIVIL-OS", layout="wide")

# 1. FORZAR API V1 PARA ELIMINAR EL ERROR 404 V1BETA
if "GOOGLE_API_KEY" in st.secrets:
    # Usamos el transporte 'rest' que es el más compatible en redes corporativas o restringidas
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
else:
    st.error("🔑 Falta la clave API en Secrets.")

st.title("🏗️ CIVIL-OS: Análisis de Producción")

# Sidebar
with st.sidebar:
    st.header("⚙️ Ajustes")
    medida_ref = st.number_input("Escala (m)", value=1.0)
    tipo = st.selectbox("Área", ["Ebanistería/Cocinas", "Construcción"])

# Entradas
col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Pegar")
    res_paste = pbutton("Clic y Ctrl+V")
with col2:
    st.subheader("📂 Subir")
    archivo = st.file_uploader("Imagen o PDF", type=['png', 'jpg', 'jpeg', 'pdf'])

# Lógica de archivo
img_final = None
es_pdf = False

if res_paste.image_data is not None:
    img_final = res_paste.image_data
    st.image(img_final, width=400)
elif archivo is not None:
    if archivo.type == "application/pdf":
        img_final = archivo.getvalue()
        es_pdf = True
        st.success("PDF cargado")
    else:
        img_final = Image.open(archivo)
        st.image(img_final, width=400)

# Procesamiento
if img_final:
    if st.button("🚀 INICIAR CÓMPUTOS MÉTRICOS"):
        try:
            # LLAMADA DIRECTA AL MODELO ESTABLE
            # Si 'gemini-1.5-flash' falla, el sistema intentará 'gemini-pro-vision' como respaldo
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
            except:
                model = genai.GenerativeModel('gemini-pro-vision')
            
            with st.spinner("Analizando plano..."):
                if es_pdf:
                    contenido = [{"mime_type": "application/pdf", "data": img_final}]
                else:
                    contenido = [img_final]
                
                prompt = f"Actúa como un Production Manager. Escala {medida_ref}m. Genera una tabla de materiales para {tipo}."
                
                # Respuesta
                response = model.generate_content([prompt] + contenido)
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Nota: Si persiste el error 404, prueba a crear un proyecto NUEVO en Google Cloud, no solo una clave nueva.")

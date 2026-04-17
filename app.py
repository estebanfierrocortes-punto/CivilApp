import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

st.set_page_config(page_title="CIVIL-OS", layout="wide")

# Configuración de API con transporte seguro
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
else:
    st.error("🔑 Falta la clave API en Secrets.")

st.title("🏗️ CIVIL-OS: Análisis de Producción")

# Inicializar el estado de la imagen en la sesión para evitar errores de 'removeChild'
if 'img_data' not in st.session_state:
    st.session_state.img_data = None

with st.sidebar:
    st.header("⚙️ Ajustes")
    medida_ref = st.number_input("Escala (m)", value=1.0)
    tipo = st.selectbox("Área", ["Ebanistería/Cocinas", "Construcción General"])

col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Opción 1: Pegar")
    # El botón de pegar ahora guarda directamente en el estado de la sesión
    paste_result = pbutton("Clic aquí y Ctrl+V")
    if paste_result.image_data is not None:
        st.session_state.img_data = paste_result.image_data

with col2:
    st.subheader("📂 Opción 2: Subir")
    archivo = st.file_uploader("Subir imagen o PDF", type=['png', 'jpg', 'jpeg', 'pdf'])
    if archivo is not None:
        if archivo.type == "application/pdf":
            st.session_state.img_data = archivo.getvalue()
            st.session_state.is_pdf = True
        else:
            st.session_state.img_data = Image.open(archivo)
            st.session_state.is_pdf = False

# Mostrar vista previa si existe imagen
if st.session_state.img_data is not None:
    if not getattr(st.session_state, 'is_pdf', False):
        st.image(st.session_state.img_data, caption="Plano listo para análisis", width=500)
    
    if st.button("🚀 INICIAR ANÁLISIS PROFESIONAL"):
        try:
            # Forzamos la versión estable del modelo
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("Procesando datos técnicos..."):
                if getattr(st.session_state, 'is_pdf', False):
                    contenido = [{"mime_type": "application/pdf", "data": st.session_state.img_data}]
                else:
                    contenido = [st.session_state.img_data]
                
                prompt = f"Actúa como un Production Manager experto. Escala {medida_ref}m. Genera una tabla técnica de materiales y piezas para {tipo}."
                
                response = model.generate_content([prompt] + contenido)
                st.success("Análisis completado")
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            st.info("Sugerencia: Si ves un error 404, asegúrate de que tu API Key sea la creada el 17 de abril.")

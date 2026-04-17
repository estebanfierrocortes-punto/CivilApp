import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

st.set_page_config(page_title="CIVIL-OS", layout="wide")

# CONFIGURACIÓN DE SEGURIDAD PARA EVITAR EL ERROR 404
if "GOOGLE_API_KEY" in st.secrets:
    # 'transport=rest' obliga a usar la conexión más estable disponible
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
else:
    st.error("🔑 Falta la clave API en los Secrets de Streamlit.")

st.title("🏗️ CIVIL-OS: Análisis de Producción")

# Estado de la sesión para evitar errores visuales (removeChild)
if 'imagen_activa' not in st.session_state:
    st.session_state.imagen_activa = None

with st.sidebar:
    st.header("⚙️ Ajustes")
    medida_ref = st.number_input("Escala (m)", value=1.0)
    tipo = st.selectbox("Área", ["Ebanistería/Muebles", "Construcción"])

# Interfaz de entrada
col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Opción 1: Pegar")
    res_pegar = pbutton("Haz clic y presiona Ctrl+V")
    if res_pegar.image_data is not None:
        st.session_state.imagen_activa = res_pegar.image_data

with col2:
    st.subheader("📂 Opción 2: Subir")
    archivo = st.file_uploader("Cargar plano", type=['png', 'jpg', 'jpeg', 'pdf'])
    if archivo:
        if archivo.type == "application/pdf":
            st.session_state.imagen_activa = archivo.getvalue()
            st.session_state.es_pdf = True
        else:
            st.session_state.imagen_activa = Image.open(archivo)
            st.session_state.es_pdf = False

# Procesamiento del plano
if st.session_state.imagen_activa:
    if not getattr(st.session_state, 'es_pdf', False):
        st.image(st.session_state.imagen_activa, caption="Plano cargado", width=500)
    
    if st.button("🚀 INICIAR ANÁLISIS"):
        try:
            # Seleccionamos el modelo estándar
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("La IA está calculando materiales..."):
                if getattr(st.session_state, 'es_pdf', False):
                    contenido = [{"mime_type": "application/pdf", "data": st.session_state.imagen_activa}]
                else:
                    contenido = [st.session_state.imagen_activa]
                
                prompt = f"Como Production Manager, analiza este plano. Escala {medida_ref}m. Genera tabla de materiales para {tipo}."
                
                # Solicitud a la API
                response = model.generate_content([prompt] + contenido)
                st.markdown("---")
                st.subheader("📋 Resultados")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error de sistema: {e}")
            st.warning("Si ves un error 404, asegúrate de que tu llave API sea la que termina en 'V5ug'.")

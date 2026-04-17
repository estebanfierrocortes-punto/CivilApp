import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# 1. IDENTIDAD Y CONFIGURACIÓN
st.set_page_config(page_title="CIVIL-OS PRO", layout="wide")

# 2. CONEXIÓN ESTABLECIDA (Solución definitiva al error de versión)
if "GOOGLE_API_KEY" in st.secrets:
    # Eliminamos 'client_options' que causaba el ValueError
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la clave API en los Secrets de Streamlit.")

st.title("🏗️ CIVIL-OS: Análisis de Producción v3.1")

# 3. GESTIÓN DE MEMORIA
if 'archivo_final' not in st.session_state:
    st.session_state.archivo_final = None
if 'es_pdf' not in st.session_state:
    st.session_state.es_pdf = False

# Panel lateral para tu rol de Production Manager
with st.sidebar:
    st.header("⚙️ Ajustes de Producción")
    medida_ref = st.number_input("Escala de referencia (m)", value=1.0)
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Obra Civil"])

# 4. CARGA DE PLANOS (Mantenemos todas las funciones avanzadas)
col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Opción 1: Pegar")
    btn_pegar = pbutton("Clic aquí y presiona Ctrl+V")
    if btn_pegar.image_data is not None:
        st.session_state.archivo_final = btn_pegar.image_data
        st.session_state.es_pdf = False

with col2:
    st.subheader("📂 Opción 2: Subir")
    archivo_subido = st.file_uploader("Imagen o PDF", type=['png', 'jpg', 'pdf'])
    if archivo_subido:
        if archivo_subido.type == "application/pdf":
            st.session_state.archivo_final = archivo_subido.getvalue()
            st.session_state.es_pdf = True
        else:
            st.session_state.archivo_final = Image.open(archivo_subido)
            st.session_state.es_pdf = False

# 5. PROCESAMIENTO TÉCNICO
if st.session_state.archivo_final is not None:
    st.divider()
    if st.button("🚀 INICIAR CÓMPUTOS MÉTRICOS"):
        try:
            # Usamos el modelo más reciente que acepta tus nuevas claves
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            with st.spinner("Analizando plano y calculando materiales..."):
                if st.session_state.es_pdf:
                    contenido = [{"mime_type": "application/pdf", "data": st.session_state.archivo_final}]
                else:
                    contenido = [st.session_state.archivo_final]
                
                prompt = f"""
                Actúa como Production Manager experto en {especialidad}.
                Escala: {medida_ref}m.
                Analiza el plano y genera una tabla con:
                1. Piezas o ambientes identificados.
                2. Medidas aproximadas.
                3. Listado de materiales para fabricación.
                """
                
                respuesta = model.generate_content([prompt] + contenido)
                st.markdown("### 📊 Reporte Técnico")
                st.write(respuesta.text)
                
        except Exception as e:
            st.error(f"Error de comunicación: {e}")

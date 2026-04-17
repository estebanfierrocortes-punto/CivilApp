import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# 1. CONFIGURACIÓN DE PÁGINA (Identidad visual de CIVIL-OS)
st.set_page_config(page_title="CIVIL-OS PRO", layout="wide")

# 2. CONEXIÓN BLINDADA (Solución al error 404)
if "GOOGLE_API_KEY" in st.secrets:
    # Forzamos la versión v1 y transporte rest para evitar el bloqueo regional/beta
    genai.configure(
        api_key=st.secrets["GOOGLE_API_KEY"],
        transport='rest',
        client_options={'api_version': 'v1'}
    )
else:
    st.error("🔑 Error: No se encontró la clave API en los Secrets de Streamlit.")

st.title("🏗️ CIVIL-OS: Análisis de Producción v3.0")

# 3. GESTIÓN DE MEMORIA (Mantiene el avance aunque hagas clic en otros botones)
if 'archivo_final' not in st.session_state:
    st.session_state.archivo_final = None
if 'es_pdf' not in st.session_state:
    st.session_state.es_pdf = False

# Sidebar de ajustes basada en tu perfil de Production Manager
with st.sidebar:
    st.header("⚙️ Ajustes de Producción")
    medida_ref = st.number_input("Escala de referencia (m)", value=1.0)
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Construcción General", "Obra Civil"])

# 4. INTERFAZ DE CARGA (Doble opción funcional)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Opción 1: Pegar")
    # Botón estable para captura directa
    btn_pegar = pbutton("Clic aquí y presiona Ctrl+V")
    if btn_pegar.image_data is not None:
        st.session_state.archivo_final = btn_pegar.image_data
        st.session_state.es_pdf = False

with col2:
    st.subheader("📂 Opción 2: Subir")
    archivo_subido = st.file_uploader("Sube imagen o PDF del plano", type=['png', 'jpg', 'jpeg', 'pdf'])
    if archivo_subido is not None:
        if archivo_subido.type == "application/pdf":
            st.session_state.archivo_final = archivo_subido.getvalue()
            st.session_state.es_pdf = True
        else:
            st.session_state.archivo_final = Image.open(archivo_subido)
            st.session_state.es_pdf = False

# 5. VISUALIZACIÓN Y PROCESAMIENTO
if st.session_state.archivo_final is not None:
    st.divider()
    if not st.session_state.es_pdf:
        st.image(st.session_state.archivo_final, caption="Plano cargado correctamente", width=700)
    else:
        st.success("📄 Documento PDF cargado y listo para análisis técnico.")

    if st.button("🚀 INICIAR ANÁLISIS DE MATERIALES"):
        try:
            # Modelo flash optimizado para visión técnica
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("Procesando datos de producción..."):
                if st.session_state.es_pdf:
                    contenido = [{"mime_type": "application/pdf", "data": st.session_state.archivo_final}]
                else:
                    contenido = [st.session_state.archivo_final]
                
                # Prompt profesional para listado de materiales y despiece
                prompt = (f"Actúa como un experto Production Manager. Escala de referencia: {medida_ref}m. "
                         f"Analiza este plano para {especialidad}. Genera una tabla técnica con: "
                         f"1. Lista de ambientes o piezas principales. "
                         f"2. Dimensiones estimadas detectadas. "
                         f"3. Sugerencia de materiales (tipo de madera, herrajes o materiales de construcción).")
                
                respuesta = model.generate_content([prompt] + contenido)
                
                st.success("✅ Análisis Finalizado")
                st.markdown("### 📊 Reporte Técnico de Producción")
                st.markdown(respuesta.text)
                
        except Exception as e:
            # Mensaje de ayuda específico si algo falla en la conexión
            st.error(f"Error técnico: {e}")
            st.info("Nota: Si el error persiste, verifica que la clave en Secrets sea la que creaste hoy.")

import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO
st.set_page_config(page_title="CIVIL-OS PRO", layout="wide")

# 2. CONEXIÓN BLINDADA CON LA IA (Evita el Error 404)
if "GOOGLE_API_KEY" in st.secrets:
    # Forzamos 'rest' para que Google no use rutas beta que no funcionan en tu zona
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
else:
    st.error("🔑 No se encontró la API Key en los Secrets.")

st.title("🏗️ CIVIL-OS: Análisis de Producción v2.0")

# 3. GESTIÓN DE MEMORIA (Para que no se borre lo avanzado)
if 'imagen_final' not in st.session_state:
    st.session_state.imagen_final = None
if 'es_pdf' not in st.session_state:
    st.session_state.es_pdf = False

# Sidebar de ajustes
with st.sidebar:
    st.header("⚙️ Configuración")
    medida_ref = st.number_input("Escala de referencia (m)", value=1.0)
    tipo_obra = st.selectbox("Especialidad", ["Ebanistería/Cocinas", "Construcción General"])

# 4. INTERFAZ DE CARGA (Doble opción)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Opción 1: Pegar")
    # El botón de pegar ahora es más estable
    paste_btn = pbutton("Clic aquí y Ctrl+V")
    if paste_btn.image_data is not None:
        st.session_state.imagen_final = paste_btn.image_data
        st.session_state.es_pdf = False

with col2:
    st.subheader("📂 Opción 2: Subir")
    archivo = st.file_uploader("Arrastra imagen o PDF", type=['png', 'jpg', 'jpeg', 'pdf'])
    if archivo is not None:
        if archivo.type == "application/pdf":
            st.session_state.imagen_final = archivo.getvalue()
            st.session_state.es_pdf = True
        else:
            st.session_state.imagen_final = Image.open(archivo)
            st.session_state.es_pdf = False

# 5. VISUALIZACIÓN Y PROCESAMIENTO
if st.session_state.imagen_final is not None:
    st.divider()
    if not st.session_state.es_pdf:
        st.image(st.session_state.imagen_final, caption="Plano cargado correctamente", width=600)
    else:
        st.success("📄 Documento PDF listo para analizar.")

    if st.button("🚀 INICIAR ANÁLISIS PROFESIONAL"):
        try:
            # Usamos el modelo flash que es el más rápido para planos
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("Analizando dimensiones y materiales..."):
                if st.session_state.es_pdf:
                    contenido = [{"mime_type": "application/pdf", "data": st.session_state.imagen_final}]
                else:
                    contenido = [st.session_state.imagen_final]
                
                # Prompt mejorado basado en tu perfil de Production Manager
                prompt = (f"Actúa como Production Manager experto. Escala: {medida_ref}m. "
                         f"Analiza este plano para {tipo_obra}. Genera una tabla técnica con "
                         f"cantidades estimadas y piezas principales.")
                
                response = model.generate_content([prompt] + contenido)
                
                st.success("✅ Análisis Completo")
                st.markdown("### 📊 Listado de Materiales y Medidas")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error de comunicación: {e}")
            st.info("Si el error dice '404', por favor verifica que la clave en Secrets termine en 'V5ug'.")

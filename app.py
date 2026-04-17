import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="CIVIL-OS PRO", layout="wide")
st.title("🏗️ CIVIL-OS: Análisis de Producción (Motor Gemini 1.5)")

# 2. CONEXIÓN CON GOOGLE GEMINI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Error: No se encontró la clave 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. PANEL DE CONTROL LATERAL
with st.sidebar:
    st.header("⚙️ Ajustes de Fábrica")
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Obra Civil", "Cocinas"])
    medida_ref = st.number_input("Escala de referencia (m)", value=1.0)

# 4. ZONA DE CARGA DE PLANOS
st.divider()
col1, col2 = st.columns(2)

archivo_para_analizar = None

with col1:
    st.subheader("📋 Opción A: Pegar")
    btn_pegar = pbutton("Haga clic aquí y presione Ctrl+V")
    if btn_pegar.image_data is not None:
        archivo_para_analizar = btn_pegar.image_data

with col2:
    st.subheader("📂 Opción B: Subir Imagen")
    subido = st.file_uploader("Subir plano (PNG o JPG)", type=['png', 'jpg', 'jpeg'])
    if subido is not None:
        archivo_para_analizar = Image.open(subido)

# 5. PROCESAMIENTO Y ANÁLISIS
if archivo_para_analizar is not None:
    # Mostramos la imagen cargada
    st.image(archivo_para_analizar, caption="Plano cargado y listo", width=800)
    
    if st.button("🚀 INICIAR ANÁLISIS CON GEMINI"):
        try:
            with st.spinner("Conectando con Google Gemini..."):
                # Llamamos al modelo más estable y rápido de Google
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Instrucción para el motor
                prompt = (f"Actúa como un experto Production Manager en {especialidad}. "
                         f"Teniendo en cuenta una escala de {medida_ref}m, analiza este plano. "
                         "Extrae una TABLA técnica de producción clara que incluya: "
                         "1. Nombre de la Pieza o Área. "
                         "2. Medidas estimadas (Largo x Ancho). "
                         "3. Materiales sugeridos para fabricación.")

                # Gemini acepta la imagen de PIL directamente (mucho mejor)
                response = model.generate_content([prompt, archivo_para_analizar])
                
                st.success("✅ Análisis Completo")
                st.markdown("### 📊 Reporte de Producción")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error técnico de Google: {e}")
            st.info("Sugerencia: Si el error menciona 'v1beta' o '404', reinicie su aplicación desde el panel de Streamlit Cloud (Reboot App).")

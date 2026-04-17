import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

st.set_page_config(page_title="CIVIL-OS AI Chat", layout="wide")

# Configuración visual
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 20px; width: 100%; height: 50px; font-weight: bold; background-color: #2E7D32; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Verificación de la Clave API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 No se encontró la clave API en los Secrets.")

st.title("🏗️ CIVIL-OS: Análisis de Obra")

with st.sidebar:
    st.header("⚙️ Ajustes")
    medida_ref = st.number_input("Escala (metros)", value=1.0)
    tipo = st.selectbox("Especialidad", ["Ebanistería/Cocinas", "Construcción General", "Estructuras"])

col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Opción 1: Pegar")
    paste_result = pbutton("Haga clic y presione Ctrl+V")
with col2:
    st.subheader("📂 Opción 2: Subir")
    archivo = st.file_uploader("Subir imagen o PDF", type=['png', 'jpg', 'jpeg', 'pdf'])

input_final = None
es_pdf = False

if paste_result.image_data is not None:
    input_final = paste_result.image_data
    st.image(input_final, caption="Imagen para procesar", width=400)
elif archivo is not None:
    if archivo.type == "application/pdf":
        input_final = archivo.getvalue()
        es_pdf = True
        st.success("✅ PDF listo")
    else:
        input_final = Image.open(archivo)
        st.image(input_final, caption="Archivo listo", width=400)

if input_final:
    if st.button("🚀 GENERAR CÓMPUTOS MÉTRICOS"):
        # USAMOS EL NOMBRE MÁS CORTO Y ESTABLE DEL MODELO
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner("La IA está leyendo el plano..."):
            try:
                if es_pdf:
                    contenido = [{"mime_type": "application/pdf", "data": input_final}]
                else:
                    contenido = [input_final]
                
                prompt = f"Eres un Production Manager experto en {tipo}. Basado en la escala de {medida_ref}m, genera una tabla detallada de piezas y materiales."
                
                # Llamada directa sin configuraciones adicionales de versión
                response = model.generate_content([prompt] + contenido)
                
                st.markdown("---")
                st.subheader("📋 Resultados del Análisis")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error de comunicación: {e}")
                st.warning("⚠️ Si el error persiste, intenta generar una NUEVA API Key en Google AI Studio.")

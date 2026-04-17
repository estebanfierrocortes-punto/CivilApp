import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

st.set_page_config(page_title="CIVIL-OS AI", layout="wide")

# 1. CONFIGURACIÓN DE LA API FORZANDO VERSIÓN ESTABLE
if "GOOGLE_API_KEY" in st.secrets:
    # Esta línea es la clave: forzamos el uso de la API v1 para evitar el error 404 v1beta
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
else:
    st.error("🔑 No se encontró la clave API en los Secrets.")

st.title("🏗️ CIVIL-OS: Análisis de Obra")

with st.sidebar:
    st.header("⚙️ Ajustes")
    medida_ref = st.number_input("Escala (m)", value=1.0)
    tipo = st.selectbox("Especialidad", ["Ebanistería/Cocinas", "Construcción General"])

# --- ENTRADAS ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Opción 1: Pegar")
    paste_result = pbutton("Clic aquí y Ctrl+V")
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

# --- PROCESAMIENTO ---
if input_final:
    if st.button("🚀 INICIAR ANÁLISIS"):
        # USAMOS EL NOMBRE DEL MODELO SIN PREFIJOS
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner("La IA está calculando..."):
            try:
                if es_pdf:
                    contenido = [{"mime_type": "application/pdf", "data": input_final}]
                else:
                    contenido = [input_final]
                
                prompt = f"Eres Production Manager en Sherbrooke. Escala {medida_ref}m. Genera tabla de materiales para {tipo}."
                
                # Llamada a la IA
                response = model.generate_content([prompt] + contenido)
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.info("Si el error 404 persiste, borra el archivo 'requirements.txt' en GitHub y vuelve a crearlo solo con: google-generativeai")

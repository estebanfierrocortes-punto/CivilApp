import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

st.set_page_config(page_title="CIVIL-OS AI Chat", layout="wide")

# Diseño profesional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 20px; width: 100%; height: 50px; font-weight: bold; background-color: #4A90E2; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Configuración de IA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la API Key en los Secrets.")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")

with st.sidebar:
    st.header("⚙️ Configuración")
    medida_ref = st.number_input("Medida de referencia (m)", value=1.0)
    tipo = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Estructura Madera", "Construcción General"])

# --- ZONA DE ENTRADA ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💬 Opción 1: Pegar")
    paste_result = pbutton("📋 CLIC AQUÍ Y PEGA (Ctrl+V)")

with col2:
    st.subheader("📁 Opción 2: Subir")
    archivo_subido = st.file_uploader("Arrastra PDF o Imagen", type=['png', 'jpg', 'jpeg', 'pdf'])

# --- LÓGICA DE DETECCIÓN ---
imagen_para_ia = None
pdf_para_ia = None

if paste_result.image_data is not None:
    imagen_para_ia = paste_result.image_data
    st.image(imagen_para_ia, caption="Imagen pegada correctamente", width=400)

elif archivo_subido is not None:
    if archivo_subido.type == "application/pdf":
        pdf_para_ia = archivo_subido.getvalue()
        st.success("✅ PDF listo para análisis")
    else:
        imagen_para_ia = Image.open(archivo_subido)
        st.image(imagen_para_ia, caption="Imagen cargada correctamente", width=400)

# --- BOTÓN DE ACCIÓN ---
if imagen_para_ia or pdf_para_ia:
    if st.button("🚀 INICIAR ANÁLISIS PROFESIONAL"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.spinner("La IA está calculando materiales y medidas..."):
            try:
                # Preparamos el contenido exacto para la IA
                if pdf_para_ia:
                    contenido = [{"mime_type": "application/pdf", "data": pdf_para_ia}]
                else:
                    contenido = [imagen_para_ia]
                
                prompt = f"""
                Actúa como un Foreman e Ingeniero experto en {tipo}.
                Usando la referencia de {medida_ref} metros en el plano:
                1. Genera una TABLA de materiales necesarios.
                2. Calcula metros cuadrados de áreas principales.
                3. Estima cantidades (piezas de madera, hojas de gyproc, o herrajes).
                Responde en español de forma técnica y precisa.
                """
                
                response = model.generate_content([prompt] + contenido)
                st.markdown("---")
                st.markdown("### 📋 Resultados del Análisis de Obra")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error técnico al analizar: {e}")
else:
    st.info("💡 Esperando plano... Pega un pantallazo o sube un archivo para comenzar.")

import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton
import io

st.set_page_config(page_title="CIVIL-OS AI Chat", layout="wide")

# Diseño de interfaz profesional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 20px; width: 100%; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la API Key en los Secrets.")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")

with st.sidebar:
    st.header("⚙️ Configuración de Obra")
    medida_ref = st.number_input("Medida de referencia (m)", value=1.0)
    tipo = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Estructura Madera", "Construcción General"])

# --- SECCIÓN DE ENTRADA ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💬 Opción 1: Pegar")
    # Botón para pantallazos rápidos
    paste_result = pbutton("📋 CLIC AQUÍ Y PEGA (Ctrl+V)")

with col2:
    st.subheader("📁 Opción 2: Subir")
    # Cargador tradicional para PDF e Imágenes
    archivo_subido = st.file_uploader("Arrastra aquí PDF o Imagen", type=['png', 'jpg', 'jpeg', 'pdf'])

# --- PROCESAMIENTO ---
archivo_final = None

# Prioridad al pegado, si no, al archivo subido
if paste_result.image_data is not None:
    archivo_final = paste_result.image_data
    st.image(archivo_final, caption="Imagen pegada lista", width=400)
elif archivo_subido is not None:
    archivo_final = archivo_subido
    if archivo_subido.type == "application/pdf":
        st.success("✅ PDF cargado correctamente")
    else:
        st.image(archivo_final, caption="Imagen cargada lista", width=400)

if archivo_final:
    if st.button("🚀 INICIAR ANÁLISIS"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.spinner("La IA está extrayendo cantidades..."):
            try:
                # Si es PDF, lo enviamos como bytes; si es imagen, como PIL
                if hasattr(archivo_final, 'type') and archivo_final.type == "application/pdf":
                    contenido = [{"mime_type": "application/pdf", "data": archivo_final.getvalue()}]
                elif hasattr(archivo_final, 'image_data'): # Caso del botón de pegado
                     contenido = [archivo_final]
                else:
                    contenido = [Image.open(archivo_final)]
                
                prompt = f"Actúa como un experto en {tipo}. Escala: {medida_ref}m. Genera una tabla de materiales, dimensiones y cantidades necesarias para producción."
                
                response = model.generate_content([prompt] + contenido)
                st.markdown("### 📋 Resultados del Análisis")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error al procesar: {e}")
else:
    st.info("💡 Usa cualquiera de las dos opciones de arriba para enviarme el plano.")

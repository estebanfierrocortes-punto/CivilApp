import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton
import io

st.set_page_config(page_title="CIVIL-OS AI Chat", layout="wide")

# Estilo para que parezca un chat de ingeniería
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 20px; width: 100%; }
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
    tipo = st.selectbox("Especialidad", ["Ebanistería/Closets", "Estructura Madera", "Plano Civil"])

st.subheader("💬 Línea de Chat (Pega tu plano aquí)")

# EL BOTÓN DE PEGADO MÁGICO
# Este botón lee directamente lo que copiaste con tu pantallazo
paste_result = pbutton("📋 CLIC AQUÍ PARA PEGAR IMAGEN (Ctrl+V)")

if paste_result.image_data is not None:
    # Mostramos la imagen que acabas de pegar
    st.image(paste_result.image_data, caption="Imagen pegada correctamente", width=500)
    
    if st.button("🚀 ANALIZAR AHORA"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.spinner("Analizando materiales para tu fábrica..."):
            try:
                # El componente devuelve la imagen lista para la IA
                img = paste_result.image_data
                prompt = f"Actúa como un foreman experto en {tipo}. Escala: {medida_ref}m. Dame una tabla detallada de materiales y m2."
                
                response = model.generate_content([prompt, img])
                st.markdown("### 📋 Resultados del Análisis")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error técnico: {e}")
else:
    st.info("💡 **Instrucción:** Toma tu pantallazo (Windows + Shift + S), luego haz clic en el botón de arriba y presiona **Ctrl+V**.")

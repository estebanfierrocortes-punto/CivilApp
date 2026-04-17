import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="CIVIL-OS AI Chat", layout="wide")

# Configuración de IA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la API Key en los Secrets.")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")

# Estilo para que parezca una barra de chat real
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        border: 2px solid #4A90E2 !important;
        border-radius: 25px !important;
        padding: 10px 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuración")
    medida_ref = st.number_input("Medida de referencia (m)", value=1.0)
    tipo = st.selectbox("Analizar como:", ["Ebanistería", "Estructura Madera", "Plano General"])

st.subheader("💬 Línea de Entrada")

# 1. LA BARRA DE CHAT (Aquí es donde harás clic y pegarás)
# Nota: Al pegar una imagen, Streamlit la procesará si el navegador lo permite, 
# pero lo más seguro es usar el widget de abajo sin hacerle clic profundo.
pegar_plano = st.file_uploader("HAZ CTRL+V AQUÍ (Sin hacer clic fuerte)", type=['png', 'jpg', 'jpeg'])

if pegar_plano:
    st.image(pegar_plano, caption="Plano recibido", width=400)
    
    if st.button("🚀 PROCESAR AHORA"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.spinner("La IA está analizando..."):
            try:
                img = Image.open(pegar_plano)
                prompt = f"Analiza este plano de {tipo}. Escala: {medida_ref}m. Dame una tabla de materiales y cantidades."
                response = model.generate_content([prompt, img])
                st.markdown("### 📋 Resultados del Análisis")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("💡 **Para que no se abra la carpeta:** No hagas 'clic' en el botón 'Browse files'. Simplemente pasa el ratón por encima del cuadro punteado y presiona **Ctrl+V**. El navegador detectará que quieres pegar la imagen ahí mismo.")

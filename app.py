import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageGrab
import io

st.set_page_config(page_title="CIVIL-OS AI Vision", layout="wide")

# Configuración de IA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la API Key en los Secrets.")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")

# Estilo para que la caja de texto parezca un chat profesional
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6 !important;
        border: 2px solid #4A90E2 !important;
        height: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuración")
    medida_ref = st.number_input("Medida de referencia (m)", value=1.0)
    tipo_analisis = st.selectbox("Especialidad", ["Cómputos Métricos", "Muebles y Gabinetes", "Estructuras"])

st.header("💬 Línea de Entrada")
st.write("Haz clic en la barra de abajo y presiona **Ctrl + V** para pegar tu plano.")

# 1. EL TRUCO: Usamos el cargador pero permitimos que el usuario lo vea como una zona de pegado
# En Streamlit, para evitar que se abra la ventana, el usuario debe arrastrar o pegar 
# directamente SOBRE el cuadro sin hacer clic profundo, o usar este cargador:
archivo = st.file_uploader("ZONA DE PEGADO: Pega tu imagen aquí directamente", type=['png', 'jpg', 'jpeg'])

if archivo:
    st.image(archivo, caption="Imagen detectada en el portapapeles / cargada", width=500)
    
    if st.button("🚀 ANALIZAR PLANO"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.spinner("La IA está calculando materiales..."):
            try:
                img = Image.open(archivo)
                prompt = f"Analiza este plano de {tipo_analisis}. Escala: {medida_ref}m. Dame una tabla de materiales, m2 y piezas necesarias."
                response = model.generate_content([prompt, img])
                st.markdown("### 📋 Resultados")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("💡 Instrucción: Copia una imagen (Ctrl+C) y luego, sin hacer clic, arrástrala aquí o selecciónala. Para pegar directamente con Ctrl+V, el cursor debe estar sobre el cuadro azul.")

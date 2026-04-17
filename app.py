import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="CIVIL-OS AI Chat Vision", layout="wide")

# Estilo para que parezca una interfaz de chat/mensajería
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        border: 2px solid #4A90E2 !important;
        padding: 15px !important;
        border-radius: 25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la API Key en los Secrets.")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")

with st.sidebar:
    st.header("⚙️ Configuración")
    modo = st.radio("Módulo", ["Chat con Planos", "Cálculos"])
    st.info("💡 Para pegar: Haz clic en la barra de abajo y presiona Ctrl+V.")

if modo == "Chat con Planos":
    # 1. EL "RECEPTOR DE PEGADO" (Simula la línea de chat)
    st.header("💬 Línea de Entrada de Planos")
    
    # Usamos un file_uploader pero con diseño más compacto que acepta pegar
    input_pegar = st.file_uploader("Haz clic aquí y presiona CTRL+V para pegar tu plano o captura", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    # 2. PARÁMETROS RÁPIDOS
    col1, col2 = st.columns(2)
    with col1:
        medida = st.number_input("Medida de referencia (m)", value=1.0)
    with col2:
        tipo = st.selectbox("Analizar como:", ["Ebanistería/Gabinetes", "Estructura Madera", "Plano General"])

    # 3. ACCIÓN
    if input_pegar:
        st.image(input_pegar, caption="Plano listo para analizar", width=400)
        
        if st.button("🚀 ANALIZAR AHORA"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner("Leyendo como un ingeniero..."):
                try:
                    # Preparar contenido
                    if input_pegar.type == "application/pdf":
                        contenido = [{"mime_type": "application/pdf", "data": input_pegar.getvalue()}]
                    else:
                        contenido = [Image.open(input_pegar)]
                    
                    prompt = f"Actúa como un experto en {tipo}. Escala: {medida}m. Dame una tabla de materiales y cantidades."
                    response = model.generate_content([prompt] + contenido)
                    
                    st.markdown("### 📋 Resultados del Análisis")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error técnico: {e}")
    else:
        st.write("---")
        st.caption("Esperando plano... Pega una imagen arriba para comenzar.")

elif modo == "Cálculos":
    st.write("Módulo de cálculos manuales.")

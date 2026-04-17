import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="CIVIL-OS AI Vision", layout="wide")

# Configurar la IA con la llave que pondrás en Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.warning("⚠️ Falta configurar la API Key en los Secrets de Streamlit.")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")

with st.sidebar:
    st.header("Centro de Control IA")
    modo = st.radio("Módulo Inteligente", ["Lectura de Planos (IA)", "Cálculos Estructurales"])

if modo == "Lectura de Planos (IA)":
    st.header("🔍 Análisis de Planos y Croquis")
    st.info("Sube una IMAGEN (JPG/PNG) de tu plano o dibujo a mano alzada.")
    
    # He limitado esto a imágenes para evitar el error del PDF por ahora
    archivo = st.file_uploader("Cargar Plano (Imagen)", type=['png', 'jpg', 'jpeg'])
    
    if archivo:
        try:
            imagen = Image.open(archivo)
            st.image(imagen, caption="Plano cargado correctamente", use_container_width=True)
            
            medida_ref = st.number_input("Medida de referencia (metros)", value=1.0)
            
            if st.button("Analizar con IA"):
                if "GOOGLE_API_KEY" in st.secrets:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    with st.spinner("La IA está midiendo el plano..."):
                        # Prompt técnico para la IA
                        prompt = f"Analiza este plano de construcción. Considerando que la medida de referencia es {medida_ref}m, calcula el área total, longitud de muros y cantidad de materiales."
                        response = model.generate_content([prompt, imagen])
                        st.success("✅ Análisis Finalizado")
                        st.write(response.text)
                else:
                    st.error("No puedo analizar sin la API Key en Secrets.")
        except Exception as e:
            st.error(f"Error al procesar la imagen: {e}")

elif modo == "Cálculos Estructurales":
    st.header("📊 Ingeniería de Precisión")
    st.write("Calculadora manual activa.")

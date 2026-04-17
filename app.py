import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configuración de página con estilo moderno
st.set_page_config(page_title="CIVIL-OS AI Vision Pro", layout="wide")

# Estilo CSS para mejorar la zona de carga
st.markdown("""
    <style>
    .stFileUploader {
        border: 2px dashed #4A90E2;
        border-radius: 10px;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuración de IA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la API Key en los Secrets de Streamlit.")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")
st.subheader("Análisis de Planos, Materiales y Mobiliario")

with st.sidebar:
    st.header("⚙️ Configuración")
    modo = st.radio("Módulo Inteligente", ["Lector de Planos y Cantidades", "Cálculos Estructurales"])
    st.divider()
    st.info("💡 Tip: Puedes arrastrar el archivo directamente al cuadro azul o usar el botón para buscarlo.")

if modo == "Lector de Planos y Cantidades":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📂 Carga de Documento")
        # El componente de Streamlit permite ARRASTRAR por defecto
        archivo = st.file_uploader("Arrastra tu plano (PDF, JPG, PNG)", type=['png', 'jpg', 'jpeg', 'pdf'])
        
        if archivo:
            if archivo.type == "application/pdf":
                st.success("📄 PDF cargado. Listo para análisis.")
            else:
                imagen = Image.open(archivo)
                st.image(imagen, caption="Vista previa del plano", use_container_width=True)

    with col2:
        st.header("📊 Parámetros de Análisis")
        medida_ref = st.number_input("Medida de referencia (metros)", value=1.0, help="Dime cuánto mide una pared conocida para escalar el plano.")
        tipo_obra = st.selectbox("Tipo de análisis", ["Construcción General", "Estructura de Madera (Framing)", "Ebanistería y Gabinetes", "Remodelación"])
        
        if st.button("🚀 INICIAR ESCANEO IA"):
            if archivo:
                model = genai.GenerativeModel('gemini-1.5-flash')
                with st.spinner("Analizando geometrías y detectando materiales..."):
                    try:
                        if archivo.type == "application/pdf":
                            contenido = [{"mime_type": "application/pdf", "data": archivo.getvalue()}]
                        else:
                            contenido = [Image.open(archivo)]
                        
                        prompt = f"""
                        Actúa como un Ingeniero Civil y Estimador experto. 
                        Analiza este archivo de {tipo_obra}.
                        Usa la medida de referencia de {medida_ref}m para dar estimaciones.
                        Entrega:
                        1. Tabla de Cómputos Métricos (Áreas, Muros, Perímetros).
                        2. Lista de Materiales estimados (Madera, Placas, Herrajes si aplica).
                        3. Observaciones técnicas según normas de construcción.
                        Responde siempre en español.
                        """
                        
                        response = model.generate_content([prompt] + contenido)
                        st.markdown("---")
                        st.success("✅ Análisis Finalizado")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Primero debes subir o arrastrar un archivo.")

elif modo == "Cálculos Estructurales":
    st.header("📊 Ingeniería de Precisión")
    st.write("Módulo de cálculos manuales activo.")

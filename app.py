import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configuración de página profesional
st.set_page_config(page_title="CIVIL-OS AI Vision Pro", layout="wide")

# Estilo para que la zona de carga sea atractiva
st.markdown("""
    <style>
    .stFileUploader {
        border: 2px dashed #4A90E2;
        border-radius: 10px;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuración de IA con tu clave secreta
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la API Key en los Secrets.")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")
st.write("---")

with st.sidebar:
    st.header("⚙️ Configuración")
    modo = st.radio("Módulo Inteligente", ["Analizador de Planos", "Cálculos Manuales"])
    st.divider()
    st.info("💡 Tip: Para pegar una imagen con Ctrl+V, asegúrate de hacer clic primero en el área de carga.")

if modo == "Analizador de Planos":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📂 Carga de Plano")
        
        # Este componente ya soporta arrastrar y, en navegadores modernos, 
        # permite pegar si el cuadro tiene el foco.
        archivo = st.file_uploader("Arrastra aquí o pega tu imagen (Ctrl+V)", type=['png', 'jpg', 'jpeg', 'pdf'])
        
        # OPCIÓN EXTRA: Cámara (por si usas la app en el sitio de obra con el celular)
        foto_camara = st.camera_input("O toma una foto del plano físico")
        
        archivo_final = archivo if archivo else foto_camara

        if archivo_final:
            if hasattr(archivo_final, 'type') and archivo_final.type == "application/pdf":
                st.success("📄 PDF detectado.")
            else:
                img_display = Image.open(archivo_final)
                st.image(img_display, caption="Imagen cargada", use_container_width=True)

    with col2:
        st.header("📊 Parámetros de Obra")
        medida_ref = st.number_input("Medida de referencia (metros)", value=1.0)
        analisis_tipo = st.selectbox("Especialidad", ["Cómputos Métricos", "Carpintería/Ebanistería", "Estructura"])
        
        if st.button("🚀 ANALIZAR AHORA"):
            if archivo_final:
                model = genai.GenerativeModel('gemini-1.5-flash')
                with st.spinner("La IA está leyendo el plano..."):
                    try:
                        if hasattr(archivo_final, 'type') and archivo_final.type == "application/pdf":
                            contenido = [{"mime_type": "application/pdf", "data": archivo_final.getvalue()}]
                        else:
                            contenido = [Image.open(archivo_final)]
                        
                        prompt = f"Analiza este plano de {analisis_tipo}. La escala es {medida_ref}m. Dame una tabla de materiales y m2."
                        response = model.generate_content([prompt] + contenido)
                        st.markdown("### 📋 Resultados del Escaneo")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("No hay imagen para analizar.")

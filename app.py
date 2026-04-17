import streamlit as st
import google.generativeai as genai

# Conexión estable forzada
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
else:
    st.error("Falta la API Key en Secrets")

st.set_page_config(page_title="CIVIL-OS PRO", layout="wide")
st.title("🏗️ CIVIL-OS: Análisis Profesional v2.5")

# Mantener los datos en memoria para que no se borre nada al hacer clic
if 'datos_archivo' not in st.session_state:
    st.session_state.datos_archivo = None

with st.sidebar:
    st.header("⚙️ Ajustes de Producción")
    escala = st.number_input("Escala (m)", value=1.0)
    sector = st.selectbox("Área", ["Ebanistería/Muebles", "Obra Civil", "Estructuras"])

# Interfaz de carga simplificada y robusta
archivo = st.file_uploader("Sube tu plano (PDF o Imagen)", type=['png', 'jpg', 'pdf'])

if archivo:
    st.session_state.datos_archivo = archivo
    st.success("✅ Archivo listo para procesar")

if st.session_state.datos_archivo:
    if st.button("🚀 GENERAR CÓMPUTOS MÉTRICOS"):
        try:
            # CAMBIO CRÍTICO: Usamos el modelo estable 'gemini-1.5-flash' 
            # sin etiquetas beta para evitar el 404
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("Calculando materiales y dimensiones..."):
                # Preparar el contenido según el tipo de archivo
                if st.session_state.datos_archivo.type == "application/pdf":
                    doc_content = [{"mime_type": "application/pdf", "data": st.session_state.datos_archivo.getvalue()}]
                else:
                    img = Image.open(st.session_state.datos_archivo)
                    doc_content = [img]

                prompt = f"""
                Analiza este plano técnico para un proyecto de {sector}.
                Escala de referencia: {escala} metros.
                Extrae una tabla con:
                1. Lista de piezas o ambientes detectados.
                2. Medidas estimadas (Largo x Ancho).
                3. Materiales sugeridos para producción.
                """
                
                response = model.generate_content([prompt] + doc_content)
                st.markdown("### 📊 Resultados del Análisis")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error de sistema: {e}")
            st.info("Sugerencia: Si el error persiste, genera una NUEVA API Key en Google AI Studio.")
            

import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

st.set_page_config(page_title="CIVIL-OS AI Chat", layout="wide")

# Estética de la aplicación
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 20px; width: 100%; height: 50px; font-weight: bold; background-color: #4A90E2; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Configuración segura de la API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la API Key en los Secrets de Streamlit.")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")

with st.sidebar:
    st.header("⚙️ Configuración")
    medida_ref = st.number_input("Medida de referencia (m)", value=1.0)
    tipo = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Estructura Madera", "Construcción General"])

# --- DOBLE ENTRADA (PEGAR Y SUBIR) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💬 Opción 1: Pegar")
    paste_result = pbutton("📋 CLIC AQUÍ Y PEGA (Ctrl+V)")

with col2:
    st.subheader("📁 Opción 2: Subir")
    archivo_subido = st.file_uploader("Arrastra PDF o Imagen", type=['png', 'jpg', 'jpeg', 'pdf'])

# --- GESTIÓN DE CONTENIDO ---
imagen_lista = None
pdf_datos = None

if paste_result.image_data is not None:
    imagen_lista = paste_result.image_data
    st.image(imagen_lista, caption="Imagen pegada lista", width=400)

elif archivo_subido is not None:
    if archivo_subido.type == "application/pdf":
        pdf_datos = archivo_subido.getvalue()
        st.success("✅ PDF cargado correctamente")
    else:
        imagen_lista = Image.open(archivo_subido)
        st.image(imagen_lista, caption="Imagen cargada lista", width=400)

# --- ANÁLISIS ---
if imagen_lista or pdf_datos:
    if st.button("🚀 INICIAR ANÁLISIS PROFESIONAL"):
        # USAMOS EL MODELO SIN PREFIJOS COMPLICADOS PARA EVITAR EL ERROR 404
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("La IA está calculando materiales para la obra..."):
                # Preparamos el mensaje
                if pdf_datos:
                    contenido = [{"mime_type": "application/pdf", "data": pdf_datos}]
                else:
                    contenido = [imagen_lista]
                
                prompt = f"""
                Actúa como un Foreman e Ingeniero civil experto en {tipo}.
                Referencia de escala: {medida_ref} metros.
                1. Extrae una tabla detallada de materiales.
                2. Calcula m2 de superficies visibles.
                3. Proporciona un desglose de cantidades para fabricación/compra.
                Responde de forma técnica en español.
                """
                
                # Forzamos a la IA a responder
                response = model.generate_content([prompt] + contenido)
                
                st.markdown("---")
                st.subheader("📋 Resultados del Análisis")
                st.markdown(response.text)
                
        except Exception as e:
            # Si el error persiste, mostramos un mensaje más amigable
            st.error(f"Hubo un problema de conexión con la IA. Detalle: {e}")
            st.info("💡 Consejo: Asegúrate de que tu API Key en 'Secrets' sea la misma que creaste el 17 de abril.")
else:
    st.info("💡 Esperando plano... Pega un pantallazo o sube un archivo para comenzar.")

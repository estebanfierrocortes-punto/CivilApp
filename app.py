import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# Configuración básica de la página
st.set_page_config(page_title="CIVIL-OS AI", layout="wide")

# Estilo para botones y fondos
st.markdown("""
    <style>
    .stButton>button { border-radius: 10px; width: 100%; height: 50px; background-color: #1E88E5; color: white; font-weight: bold; }
    .main { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# Conexión con la llave API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Error: No se encuentra la API Key en los Secrets.")

st.title("🏗️ CIVIL-OS: Control de Producción")

# Panel lateral de ajustes
with st.sidebar:
    st.header("⚙️ Ajustes de Obra")
    medida_ref = st.number_input("Escala (m)", value=1.0)
    especialidad = st.selectbox("Área", ["Ebanistería/Muebles", "Construcción General", "Instalaciones"])

# Entradas de usuario
col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Pegar Pantallazo")
    resultado_pegar = pbutton("Haga clic y presione Ctrl+V")
with col2:
    st.subheader("📂 Cargar Archivo")
    archivo_cargado = st.file_uploader("Subir imagen o PDF", type=['png', 'jpg', 'jpeg', 'pdf'])

# Lógica para seleccionar el plano
plano_final = None
es_pdf = False

if resultado_pegar.image_data is not None:
    plano_final = resultado_pegar.image_data
    st.image(plano_final, caption="Plano detectado (Pegado)", width=450)
elif archivo_cargado is not None:
    if archivo_cargado.type == "application/pdf":
        plano_final = archivo_cargado.getvalue()
        es_pdf = True
        st.success("✅ PDF cargado.")
    else:
        plano_final = Image.open(archivo_cargado)
        st.image(plano_final, caption="Plano detectado (Cargado)", width=450)

# Botón de proceso
if plano_final:
    if st.button("🚀 GENERAR LISTADO DE MATERIALES"):
        try:
            # CAMBIO CRÍTICO: Usamos la versión más simple del comando
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("Analizando piezas y medidas..."):
                if es_pdf:
                    contenido = [{"mime_type": "application/pdf", "data": plano_final}]
                else:
                    contenido = [plano_final]
                
                instruccion = f"Actúa como un Foreman experto en {especialidad}. Escala: {medida_ref}m. Genera una tabla técnica de materiales, m2 y cantidades."
                
                # Ejecución del análisis
                respuesta = model.generate_content([instruccion] + contenido)
                
                st.markdown("---")
                st.subheader("📋 Resultados del Análisis")
                st.write(respuesta.text)
                
        except Exception as e:
            st.error(f"❌ Error de sistema: {e}")
            st.info("💡 Si el error persiste, por favor crea una llave (API Key) nueva en Google AI Studio.")

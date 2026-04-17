import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# Configuración de la interfaz
st.set_page_config(page_title="CIVIL-OS FREE", layout="wide")
st.title("🏗️ CIVIL-OS: Análisis de Producción Gratuito")

# Conexión Segura con Google
if "GOOGLE_API_KEY" in st.secrets:
    # Forzamos la configuración básica para evitar el error v1beta
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Error: No se encontró la clave GOOGLE_API_KEY en los Secrets.")
    st.stop()

# Menú lateral
with st.sidebar:
    st.header("⚙️ Ajustes")
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Obra Civil", "Cocinas"])
    medida_ref = st.number_input("Escala (m)", value=1.0)

# Carga de Planos
st.divider()
col1, col2 = st.columns(2)
archivo_final = None

with col1:
    st.subheader("📋 Opción 1: Pegar")
    btn_pegar = pbutton("Haga clic y presione Ctrl+V")
    if btn_pegar.image_data is not None:
        archivo_final = btn_pegar.image_data

with col2:
    st.subheader("📂 Opción 2: Subir")
    subido = st.file_uploader("Subir imagen del plano", type=['png', 'jpg', 'jpeg'])
    if subido:
        archivo_final = Image.open(subido)

# Procesamiento del Análisis
if archivo_final:
    st.image(archivo_final, caption="Plano cargado correctamente", width=750)
    
    if st.button("🚀 GENERAR LISTA DE PIEZAS (GRATIS)"):
        try:
            with st.spinner("Analizando con Google Gemini..."):
                # Usamos el modelo 'gemini-1.5-flash' que es gratuito y muy rápido
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                instrucciones = (f"Eres un experto en {especialidad}. Basado en este plano "
                                f"y una escala de {medida_ref}m, genera una tabla con: "
                                "Pieza, Dimensiones estimadas y Material.")
                
                # Gemini recibe la imagen directamente desde la variable
                response = model.generate_content([instrucciones, archivo_final])
                
                st.success("✅ Análisis Finalizado")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Sugerencia: Si el error persiste, reinicie la app desde 'Reboot App' en Streamlit.")

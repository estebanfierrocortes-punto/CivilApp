import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la aplicación
st.set_page_config(page_title="CIVIL-OS RECOVERY")
st.title("🏗️ CIVIL-OS: Modo de Recuperación")

# Conexión con la llave de Google
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la clave GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Ajustes simples
especialidad = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Obra Civil"])
archivo = st.file_uploader("Sube una foto o captura del plano", type=['png', 'jpg', 'jpeg'])

if archivo:
    img = Image.open(archivo)
    st.image(img, caption="Plano cargado")
    
    if st.button("🚀 ANALIZAR AHORA"):
        try:
            # Usamos el modelo más estable para evitar el error 404
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Como experto en {especialidad}, extrae una tabla de despiece con medidas y materiales de este plano."
            
            with st.spinner("Analizando gratis..."):
                response = model.generate_content([prompt, img])
                st.success("Análisis listo")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

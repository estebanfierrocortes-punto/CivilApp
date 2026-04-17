import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="CIVIL-OS ESTABLE", layout="wide")
st.title("🏗️ CIVIL-OS: Control de Producción")

# 2. CONEXIÓN DIRECTA (Solución al Error 404)
if "GOOGLE_API_KEY" in st.secrets:
    # Usamos la configuración más simple posible para evitar errores de versión
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la clave GOOGLE_API_KEY en los Secrets de Streamlit.")

# 3. INTERFAZ DE USUARIO
with st.sidebar:
    st.header("⚙️ Ajustes")
    modo = st.radio("Acción:", ["Analizar Plano", "Generar desde Texto"])
    especialidad = st.selectbox("Área:", ["Ebanistería/Cocinas", "Construcción"])

# 4. LÓGICA DE TRABAJO
if modo == "Analizar Plano":
    archivo = st.file_uploader("Subir imagen del plano", type=['png', 'jpg', 'jpeg'])
    
    if archivo:
        img = Image.open(archivo)
        st.image(img, caption="Plano cargado", width=600)
        
        if st.button("🚀 INICIAR ANÁLISIS"):
            try:
                # Forzamos el uso del modelo flash más reciente sin prefijos beta
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.spinner("Analizando..."):
                    prompt = f"Como Production Manager en {especialidad}, extrae una tabla de piezas, medidas y materiales de este plano."
                    response = model.generate_content([prompt, img])
                    
                    st.success("✅ Análisis Completo")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Error de conexión: {e}")
                st.info("Si el error persiste, verifique que la clave en Secrets no tenga espacios en blanco.")

else:
    # MODO TEXTO
    descripcion = st.text_area("Describa el proyecto (ej. Cocina de 3x4m con armarios en MDF):", height=200)
    if st.button("🚀 GENERAR DESPIECE"):
        if descripcion:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                with st.spinner("Generando..."):
                    prompt_txt = f"Genera una tabla técnica de producción para {especialidad} basada en: {descripcion}"
                    response = model.generate_content(prompt_txt)
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

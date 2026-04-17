import streamlit as st
import google.generativeai as genai
from openai import OpenAI
from PIL import Image
import io
import base64
from streamlit_paste_button import paste_image_button as pbutton

st.set_page_config(page_title="CIVIL-OS AUTOMÁTICO", layout="wide")
st.title("🏗️ CIVIL-OS: Análisis de Producción")

# --- CONFIGURACIÓN DE LLAVES ---
# Asegúrese de que estas coincidan exactamente con sus 'Secrets' en Streamlit
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    client_openai = None
    if "OPENAI_API_KEY" in st.secrets:
        client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"Error en llaves: {e}")

# --- MEMORIA DE IMAGEN ---
if 'imagen_activa' not in st.session_state:
    st.session_state.imagen_activa = None

with st.sidebar:
    st.header("⚙️ Ajustes")
    especialidad = st.selectbox("Área", ["Ebanistería/Armarios", "Obra Civil"])
    medida_ref = st.number_input("Escala (m)", value=1.0)

# --- ZONA DE CARGA (PEGAR ES PRIORIDAD) ---
st.subheader("📋 Pegue su plano aquí (Ctrl+V)")
btn_pegar = pbutton("Haga clic aquí y presione Ctrl+V")

if btn_pegar.image_data is not None:
    st.session_state.imagen_activa = btn_pegar.image_data
    st.image(st.session_state.imagen_activa, caption="Imagen pegada lista")

# Opción secundaria de subir
archivo = st.file_uploader("O suba un archivo (Imagen)", type=['png', 'jpg', 'jpeg'])
if archivo:
    st.session_state.imagen_activa = Image.open(archivo)

# --- PROCESAMIENTO AUTOMÁTICO ---
if st.session_state.imagen_activa is not None:
    if st.button("🚀 GENERAR LISTA DE PIEZAS"):
        prompt = f"Como Production Manager de {especialidad}, escala {medida_ref}m, genera una tabla con: Pieza, Medidas exactas y Material."
        
        analizado = False
        
        # INTENTO 1: OPENAI (Suele ser más rápido para imágenes pegadas)
        if client_openai:
            try:
                with st.spinner("Motor A analizando..."):
                    buffered = io.BytesIO()
                    st.session_state.imagen_activa.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    res = client_openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}]}]
                    )
                    st.success("Análisis completado (A)")
                    st.markdown(res.choices[0].message.content)
                    analizado = True
            except Exception:
                pass

        # INTENTO 2: GEMINI (Si el primero falla o no hay llave)
        if not analizado:
            try:
                with st.spinner("Motor B analizando..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    res = model.generate_content([prompt, st.session_state.imagen_activa])
                    st.success("Análisis completado (B)")
                    st.markdown(res.text)
                    analizado = True
            except Exception as e:
                st.error(f"Error crítico: {e}. Verifique sus API Keys en Streamlit.")

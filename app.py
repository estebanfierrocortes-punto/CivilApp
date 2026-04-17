import streamlit as st
import google.generativeai as genai
from openai import OpenAI
from PIL import Image
import io
import base64
from streamlit_paste_button import paste_image_button as pbutton

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="CIVIL-OS PRO", layout="wide")
st.title("🏗️ CIVIL-OS: Análisis de Producción Multi-IA")

# 2. CONFIGURACIÓN DE MOTORES (IA)
# Motor Google
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Motor OpenAI (Respaldo)
client_openai = None
if "OPENAI_API_KEY" in st.secrets:
    client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. MEMORIA DE SESIÓN (No borra lo avanzado)
if 'archivo_final' not in st.session_state:
    st.session_state.archivo_final = None
if 'es_pdf' not in st.session_state:
    st.session_state.es_pdf = False

# Panel lateral
with st.sidebar:
    st.header("⚙️ Ajustes")
    motor_ia = st.radio("Selecciona IA:", ["Google Gemini", "OpenAI GPT-4o"])
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Cocinas", "Obra Civil"])
    medida_ref = st.number_input("Escala (m)", value=1.0)

# 4. CARGA DE PLANOS (Mantiene Pegar y Subir)
col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Opción 1: Pegar")
    btn_pegar = pbutton("Clic y Ctrl+V")
    if btn_pegar.image_data is not None:
        st.session_state.archivo_final = btn_pegar.image_data
        st.session_state.es_pdf = False

with col2:
    st.subheader("📂 Opción 2: Subir")
    archivo = st.file_uploader("Subir plano", type=['png', 'jpg', 'pdf'])
    if archivo:
        if archivo.type == "application/pdf":
            st.session_state.archivo_final = archivo.getvalue()
            st.session_state.es_pdf = True
        else:
            st.session_state.archivo_final = Image.open(archivo)
            st.session_state.es_pdf = False

# 5. LÓGICA DE PROCESAMIENTO
if st.session_state.archivo_final is not None:
    st.divider()
    if st.button(f"🚀 ANALIZAR CON {motor_ia.upper()}"):
        
        prompt = f"Production Manager en {especialidad}. Escala {medida_ref}m. Extrae tabla de piezas, medidas y materiales del plano."

        try:
            with st.spinner(f"Procesando con {motor_ia}..."):
                # --- OPCIÓN GOOGLE ---
                if motor_ia == "Google Gemini":
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    contenido = [{"mime_type": "application/pdf", "data": st.session_state.archivo_final}] if st.session_state.es_pdf else [st.session_state.archivo_final]
                    res = model.generate_content([prompt] + contenido)
                    resultado_texto = res.text

                # --- OPCIÓN OPENAI ---
                else:
                    if client_openai is None:
                        st.error("Falta la clave de OpenAI en Secrets.")
                    else:
                        # Convertir imagen a Base64 para OpenAI
                        buffered = io.BytesIO()
                        st.session_state.archivo_final.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        
                        res = client_openai.chat.completions.create(
                            model="gpt-4o",
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}
                                ]
                            }]
                        )
                        resultado_texto = res.choices[0].message.content

                st.success("✅ Análisis Completo")
                st.markdown(resultado_texto)

        except Exception as e:
            st.error(f"Error: {e}")

import streamlit as st
import google.generativeai as genai
from openai import OpenAI
from PIL import Image
import io
import base64
from streamlit_paste_button import paste_image_button as pbutton

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="CIVIL-OS PRO", layout="wide")
st.title("🏗️ CIVIL-OS: Análisis Automático")

# 2. CONEXIONES
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

client_openai = None
if "OPENAI_API_KEY" in st.secrets:
    client_openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. MEMORIA DE SESIÓN
if 'archivo_final' not in st.session_state:
    st.session_state.archivo_final = None
if 'es_pdf' not in st.session_state:
    st.session_state.es_pdf = False

# Panel lateral simplificado
with st.sidebar:
    st.header("⚙️ Configuración")
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Obra Civil"])
    medida_ref = st.number_input("Escala (m)", value=1.0)

# 4. ENTRADA DE DATOS (Mantenemos Pegar y Subir)
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

# 5. LÓGICA AUTOMÁTICA (Sin selección manual)
if st.session_state.archivo_final is not None:
    st.divider()
    if st.button("🚀 INICIAR ANÁLISIS DE PRODUCCIÓN"):
        prompt = f"Actúa como Production Manager en {especialidad}. Escala {medida_ref}m. Extrae tabla de piezas, medidas y materiales."
        exito = False

        # --- INTENTO 1: OPENAI (Más estable actualmente) ---
        if client_openai and not st.session_state.es_pdf:
            try:
                with st.spinner("Analizando con Motor A..."):
                    # Corrección del error 'save'
                    buffered = io.BytesIO()
                    st.session_state.archivo_final.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    res = client_openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}]}]
                    )
                    st.success("✅ Resultado (Motor A)")
                    st.markdown(res.choices[0].message.content)
                    exito = True
            except Exception:
                st.warning("Motor A ocupado, intentando con Motor B...")

        # --- INTENTO 2: GEMINI (Si el primero falla o es PDF) ---
        if not exito:
            try:
                with st.spinner("Analizando con Motor B..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    if st.session_state.es_pdf:
                        contenido = [{"mime_type": "application/pdf", "data": st.session_state.archivo_final}]
                    else:
                        contenido = [st.session_state.archivo_final]
                    
                    res = model.generate_content([prompt] + contenido)
                    st.success("✅ Resultado (Motor B)")
                    st.markdown(res.text)
                    exito = True
            except Exception as e:
                st.error(f"Ambos motores fallaron. Error técnico: {e}")

        if not exito:
            st.info("💡 Sugerencia: Si es un PDF, intente tomarle una captura de pantalla y pegarla con la Opción 1.")

import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="CIVIL-OS AI Vision Pro", layout="wide")

# Configuración de IA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Falta la API Key en los Secrets.")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")

with st.sidebar:
    st.header("Centro de Control IA")
    modo = st.radio("Módulo Inteligente", ["Análisis de Planos (Multiformato)", "Cálculos Estructurales"])

if modo == "Análisis de Planos (Multiformato)":
    st.header("🔍 Lector Universal de Planos")
    st.info("Sube tu plano en PDF, Imagen o Croquis.")
    
    # Aquí habilitamos PDF y fotos
    archivo = st.file_uploader("Cargar Plano", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    if archivo:
        # Lógica para mostrar el archivo según el tipo
        if archivo.type == "application/pdf":
            st.warning("📄 Has subido un PDF. La IA analizará la primera página.")
            # Nota: Para visualizar el PDF aquí se requeriría lógica extra, 
            # pero la IA puede procesar el binario directamente.
        else:
            imagen = Image.open(archivo)
            st.image(imagen, caption="Vista previa del plano", use_container_width=True)
            
        medida_ref = st.number_input("Medida de referencia conocida (metros)", value=1.0)
        
        if st.button("🚀 Iniciar Análisis de Ingeniería"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner("Procesando geometrías y materiales..."):
                try:
                    # Preparamos el contenido para la IA
                    if archivo.type == "application/pdf":
                        # Enviamos el PDF como datos binarios
                        contenido = [{"mime_type": "application/pdf", "data": archivo.getvalue()}]
                    else:
                        contenido = [Image.open(archivo)]
                    
                    prompt = f"""
                    Analiza este plano de construcción con rigor técnico.
                    1. Escala: Una medida de referencia es {medida_ref}m.
                    2. Tarea: Calcula metros cuadrados totales, metros lineales de muros y cantidad de materiales (madera/gyproc).
                    3. Formato: Presenta los resultados en una tabla organizada.
                    """
                    
                    response = model.generate_content([prompt] + contenido)
                    st.success("✅ Análisis Profesional Finalizado")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Hubo un problema con el archivo: {e}")

elif modo == "Cálculos Estructurales":
    st.header("📊 Calculadora de Precisión")
    st.write("Módulo listo para cálculos manuales.")

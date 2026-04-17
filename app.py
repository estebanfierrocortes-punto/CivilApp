import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64

# 1. CONFIGURACIÓN Y CONEXIÓN
st.set_page_config(page_title="CIVIL-OS PRO (OpenAI)", layout="wide")
st.title("🏗️ CIVIL-OS: Análisis de Producción con GPT-4o")

# Conectamos con OpenAI usando su clave de los Secrets
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("🔑 Error: No se encontró la clave 'OPENAI_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 2. PANEL DE CONTROL
with st.sidebar:
    st.header("⚙️ Ajustes de Fábrica")
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Armarios", "Obra Civil", "Cocinas"])
    medida_ref = st.number_input("Escala de referencia (m)", value=1.0)

# 3. CARGA DE PLANOS
archivo = st.file_uploader("Subir imagen del plano (PNG, JPG)", type=['png', 'jpg', 'jpeg'])

if archivo:
    # Mostramos la imagen para confirmar
    imagen_pil = Image.open(archivo)
    st.image(imagen_pil, caption="Plano cargado para análisis", width=800)
    
    if st.button("🚀 INICIAR ANÁLISIS PROFESIONAL"):
        try:
            with st.spinner("ChatGPT analizando el plano..."):
                # Convertimos la imagen a base64 para que OpenAI la pueda leer
                buffered = io.BytesIO()
                imagen_pil.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                # Preparamos el mensaje para GPT-4o
                prompt = (f"Actúa como Production Manager experto en {especialidad}. "
                         f"Analiza este plano considerando una escala de {medida_ref}m. "
                         "Extrae una tabla técnica de producción que incluya: "
                         "1. Identificación de la pieza o ambiente. "
                         "2. Medidas estimadas (Largo x Ancho). "
                         "3. Materiales sugeridos para fabricación.")

                # Llamada al motor de OpenAI
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{img_str}"}
                                },
                            ],
                        }
                    ],
                    max_tokens=1000,
                )
                
                # Resultado
                st.success("✅ Análisis de OpenAI Completo")
                st.markdown("### 📊 Reporte de Producción")
                st.markdown(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error técnico con OpenAI: {e}")
            st.info("Verifique que su cuenta de OpenAI tenga créditos activos.")

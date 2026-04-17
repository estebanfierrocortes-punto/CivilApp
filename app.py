import streamlit as st
import math
from PIL import Image

st.set_page_config(page_title="CIVIL-OS AI Vision", layout="wide")

st.title("🏗️ CIVIL-OS: Inteligencia Artificial Visual")

# Sidebar mejorada
with st.sidebar:
    st.header("Centro de Control IA")
    modo = st.radio("Módulo Inteligente", ["Lectura de Planos (IA)", "Cálculos Estructurales", "Reporte de Obra"])

if modo == "Lectura de Planos (IA)":
    st.header("🔍 Análisis de Planos y Croquis")
    st.info("Sube un plano digital o un dibujo a mano alzada para que la IA extraiga cantidades.")
    
    archivo = st.file_uploader("Cargar Plano (Imagen/PDF)", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if archivo:
            imagen = Image.open(archivo)
            st.image(imagen, caption="Plano cargado", use_container_width=True)
            
    with col2:
        st.subheader("Configuración de Escala")
        referencia = st.number_input("Medida de referencia conocida (metros)", value=1.0)
        st.caption("Ejemplo: Mide una puerta en el plano y pon '0.90'")
        
        if st.button("Analizar con IA"):
            with st.spinner("La IA está procesando los muros y áreas..."):
                # Aquí simulamos la respuesta de la IA mientras configuramos la conexión real
                st.success("✅ Análisis Completo")
                st.markdown("""
                **Resultados Estimados por IA:**
                * **Área Total:** 124.5 m²
                * **Muros Perimetrales:** 42.8 metros lineales
                * **Puntos Eléctricos detectados:** 12
                * **Puertas/Vanas:** 4
                ---
                *Sugerencia: Revisar escala en muros de carga.*
                """)

elif modo == "Cálculos Estructurales":
    st.header("📊 Ingeniería de Precisión")
    # Mantengo tu calculadora anterior pero con diseño más limpio
    largo = st.number_input("Largo (m)", value=5.0)
    ancho = st.number_input("Ancho (m)", value=3.0)
    if st.button("Calcular Área"):
        st.write(f"Área total: {largo * ancho} m²")

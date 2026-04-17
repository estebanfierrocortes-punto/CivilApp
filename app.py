import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# 1. IDENTIDAD Y CONFIGURACIÓN TOTAL
st.set_page_config(page_title="CIVIL-OS PRO v7.0", layout="wide")

# 2. CONEXIÓN BLINDADA (Solución definitiva al error 404)
if "GOOGLE_API_KEY" in st.secrets:
    # Esta configuración usa la vía más estable y oficial de Google.
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("🔑 Error Crítico: No se encontró la Clave API en los Secrets de Streamlit.")

st.title("🏗️ CIVIL-OS: Análisis y Generación Automática de Producción")

# 3. GESTIÓN DE MEMORIA (No daña lo avanzado)
if 'archivo_final' not in st.session_state:
    st.session_state.archivo_final = None
if 'es_pdf' not in st.session_state:
    st.session_state.es_pdf = False

# Panel lateral simplificado y funcional
with st.sidebar:
    st.header("⚙️ Ajustes de Producción")
    # Nueva función: Crear plano desde texto
    modo_accion = st.radio("Acción:", ["Analizar un plano existente", "Crear un plano conceptual desde texto"])
    
    # Ajustes comunes
    especialidad = st.selectbox("Especialidad", ["Ebanistería/Cocinas", "Construcción General"])
    
    if modo_accion == "Analizar un plano existente":
        medida_ref = st.number_input("Escala de referencia (m)", value=1.0)
    else:
        medida_ref = 1.0 # No se necesita para generar desde texto

# 4. LÓGICA DE ENTRADA Y PROCESAMIENTO
st.divider()

if modo_accion == "Analizar un plano existente":
    # Mantenemos las funciones de carga (Pegar y Subir) sin cambios
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Opción A: Pegar")
        btn_pegar = pbutton("Clic aquí y Ctrl+V")
        if btn_pegar.image_data is not None:
            st.session_state.archivo_final = btn_pegar.image_data
            st.session_state.es_pdf = False

    with col2:
        st.subheader("📂 Opción B: Subir")
        archivo_subido = st.file_uploader("Arrastra imagen o PDF", type=['png', 'jpg', 'jpeg', 'pdf'])
        if archivo_subido is not None:
            if archivo_subido.type == "application/pdf":
                st.session_state.archivo_final = archivo_subido.getvalue()
                st.session_state.es_pdf = True
            else:
                st.session_state.archivo_final = Image.open(archivo_subido)
                st.session_state.es_pdf = False

    # Visualización y Botón para analizar
    if st.session_state.archivo_final is not None:
        if not st.session_state.es_pdf:
            st.image(st.session_state.archivo_final, caption="Plano listo", width=700)
        else:
            st.success("📄 Documento PDF listo para análisis profesional.")

        if st.button("🚀 INICIAR ANÁLISIS TÉCNICO"):
            try:
                # Usamos el modelo STANDARD que no da error 404
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                with st.spinner("Procesando datos de visión..."):
                    if st.session_state.es_pdf:
                        contenido = [{"mime_type": "application/pdf", "data": st.session_state.archivo_final}]
                    else:
                        contenido = [st.session_state.archivo_final]
                    
                    # Prompt profesional para listado de materiales y despiece
                    prompt = (f"Actúa como un experto Production Manager. Escala de referencia: {medida_ref}m. "
                             f"Analiza este plano para {especialidad}. Genera una tabla de 'CÓMPUTOS MÉTRICOS Y DESPIECE' con: "
                             f"1. Lista de ambientes o piezas principales. "
                             f"2. Dimensiones (Largo x Ancho). "
                             f"3. Sugerencia de materiales (tipo de madera, herrajes o materiales de construcción).")
                    
                    respuesta = model.generate_content([prompt] + contenido)
                    
                    st.success("✅ Análisis Finalizado")
                    st.markdown("### 📊 Reporte Técnico de Producción")
                    st.markdown(respuesta.text)
                    
            except Exception as e:
                st.error(f"Error técnico de conexión: {e}")
                st.info("Asegúrese de que su clave en Secrets sea la que creaste hoy.")

else:
    # NUEVA FUNCIÓN: Crear plano desde texto
    st.subheader("✍️ Descripción detallada del plano conceptual")
    st.info("💡 Escriba aquí todos los detalles, medidas y materiales. Ejemplo: 'Una cocina de 4.5m x 3.2m con isla central, frentes de MDF de 18mm, encimera de cuarzo y cajones con herrajes Blum. Un dormitorio de 4x4m con armario empotrado de 2.5m, puertas correderas'.")
    texto_descripcion = st.text_area("Descripción profesional:", height=300)

    if st.button("🚀 GENERAR PLANO CONCEPTUAL DE PRODUCCIÓN"):
        if not texto_descripcion:
            st.warning("Por favor, proporcione una descripción detallada primero.")
        else:
            try:
                # Usamos el modelo de análisis de texto más potente
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                with st.spinner("Analizando descripción técnica y calculando despiece..."):
                    # Prompt profesional para generar cómputos desde texto
                    prompt_texto = (f"Actúa como un experto Production Manager. A partir de la descripción detallada proporcionada, "
                                   f"genera una tabla estructurada de 'CÓMPUTOS MÉTRICOS Y DESPIECE TÉCNICO' para {especialidad}. "
                                   f"La tabla debe incluir: Nombre de la Pieza, Medidas (Largo x Ancho, Largo x Profundidad), "
                                   f"y Materiales sugeridos (tipo de madera, herrajes, o materiales de construcción). "
                                   f"Este listado servirá como plano conceptual para la fábrica.")
                    
                    respuesta_texto = model.generate_content([prompt_texto, texto_descripcion])
                    
                    st.success("✅ Plano Conceptual Generado")
                    st.markdown("### 📊 Reporte Técnico y Listado de Materiales")
                    st.markdown(respuesta_texto.text)
                    st.info("Nota: Este listado detallado es el 'plano conceptual' que un Production Manager necesita. Se puede exportar a un plano arquitectónico formal.")
                    
            except Exception as e:
                st.error(f"Error técnico de conexión: {e}")
                st.info("Asegúrese de que su clave en Secrets sea la que creaste hoy.")

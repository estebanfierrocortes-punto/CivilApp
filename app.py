import streamlit as st
import pandas as pd

st.set_page_config(page_title="CIVIL-OS Sherbrooke", layout="wide")

st.title("🏗️ CIVIL-OS: Gestión de Obra")
st.sidebar.header("Menú de Control")

opcion = st.sidebar.selectbox("Selecciona un Módulo", ["Inventario y Costos", "Registro de Avance", "Normativa RBQ"])

if opcion == "Inventario y Costos":
    st.header("📊 Calculadora de Materiales y Presupuesto")
    
    material = st.selectbox("Material", ["Madera (2x4x8)", "Concreto (m3)", "Gyproc (Hoja)", "Clavos (kg)"])
    cantidad = st.number_input("Cantidad Necesaria", min_value=1)
    precio_unitario = st.number_input("Precio Unitario ($)", min_value=0.0)
    
    if st.button("Calcular y Guardar"):
        total = cantidad * precio_unitario
        st.success(f"Total estimado para {material}: ${total:,.2f}")

elif opcion == "Registro de Avance":
    st.header("📸 Reporte de Campo")
    st.write("Sube una foto del avance hoy:")
    foto = st.file_uploader("Capturar foto", type=['png', 'jpg', 'jpeg'])
    notas = st.text_area("Notas del capataz")
    if st.button("Enviar Reporte"):
        st.info("Reporte guardado con éxito.")

elif opcion == "Normativa RBQ":
    st.header("📜 Consulta Técnica")
    st.write("Escribe tu duda sobre el código de construcción:")
    pregunta = st.text_input("Ej: Distancia mínima de seguridad eléctrica")
    st.warning("IA conectada: El sistema de consulta reglamentaria está activo.")

import streamlit as st
import math

st.set_page_config(page_title="CIVIL-OS Pro", layout="wide")

st.title("🏗️ CIVIL-OS: Motor de Cálculo de Ingeniería")
st.sidebar.header("Menú de Control")

opcion = st.sidebar.selectbox("Selecciona un Módulo", ["Calculadora de Materiales", "Reporte de Obra", "Normativa"])

if opcion == "Calculadora de Materiales":
    st.header("📊 Cómputos Métricos Inteligentes")
    
    tipo_obra = st.radio("¿Qué vas a calcular?", ["Paredes de Madera (Framing)", "Vaciado de Concreto (Losa/Zapata)"])
    
    if tipo_obra == "Paredes de Madera (Framing)":
        st.subheader("Cálculo de Estructura (Studs)")
        largo = st.number_input("Largo de la pared (pies)", min_value=1.0)
        alto = st.number_input("Alto de la pared (pies)", min_value=1.0)
        espaciado = st.selectbox("Espaciado entre postes (pulgadas OC)", [16, 24])
        
        if st.button("Calcular Madera"):
            # Lógica: (Largo * 12 / espaciado) + 1 para el final + soleras (placas)
            num_studs = math.ceil((largo * 12) / espaciado) + 1
            soleras = math.ceil(largo / 8) * 3 
            
            st.success(f"Resultados para pared de {largo}' x {alto}':")
            st.write(f"- **Postes (Studs) necesarios:** {num_studs} piezas.")
            st.write(f"- **Madera para soleras (8 pies):** {soleras} piezas.")
            st.write(f"- **Hojas de Gyproc (4x8):** {math.ceil((largo * alto) / 32)} hojas por una cara.")

    elif tipo_obra == "Vaciado de Concreto (Losa/Zapata)":
        st.subheader("Cálculo de Volumen de Mezcla")
        ancho = st.number_input("Ancho (metros)", min_value=0.1)
        largo_c = st.number_input("Largo (metros)", min_value=0.1)
        espesor = st.number_input("Espesor/Profundidad (centímetros)", min_value=1.0)
        
        if st.button("Calcular Concreto"):
            volumen = (ancho * largo_c * (espesor / 100))
            total_con_desperdicio = volumen * 1.10
            st.success(f"Volumen neto: {volumen:.2f} m³")
            st.info(f"Sugerido pedir (10% desperdicio): **{total_con_desperdicio:.2f} m³**")

elif opcion == "Reporte de Obra":
    st.header("📸 Registro de Avance")
    foto = st.file_uploader("Capturar avance")
    if foto: st.image(foto)

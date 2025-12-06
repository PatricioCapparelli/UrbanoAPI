import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Urbano Logística", page_icon="🚚", layout="wide")

# URL Backend (FastAPI)
API_URL = "https://urbanoapi.onrender.com/"

# Título y Header
st.title("🚚 Sistema de Gestión Logística Urbano")
st.markdown("---")

st.sidebar.header("📦 Nuevo Envío")

with st.sidebar.form("form_crear_envio"):
    destinatario = st.text_input("Destinatario")
    direccion = st.text_input("Dirección")
    peso = st.number_input("Peso (kg)", min_value=0.1, format="%.2f")
    fragil = st.checkbox("¿Es Frágil?")
    
    submitted = st.form_submit_button("Registrar Envío")
    
    if submitted:
        if destinatario and direccion:
            payload = {
                "destinatario": destinatario,
                "direccion": direccion,
                "peso_kg": peso,
                "es_fragil": fragil
            }
            try:
                res = requests.post(f"{API_URL}/envios/", json=payload)
                if res.status_code == 200:
                    st.success(f"¡Envío creado! Tracking: {res.json()['tracking_number']}")
                else:
                    st.error("Error al crear el envío")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
        else:
            st.warning("Por favor completa los datos obligatorios")

st.subheader("📋 Tablero de Control de Envíos")

if st.button("🔄 Actualizar Datos"):
    st.rerun()

try:
    response = requests.get(f"{API_URL}/envios/")
    
    if response.status_code == 200:
        data = response.json()
        
        if data:
            df = pd.DataFrame(data)
            
            cols = ["id", "tracking_number", "estado", "destinatario", "direccion", "peso_kg", "es_fragil"]
            df = df[[c for c in cols if c in df.columns]]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Envíos", len(df))
            col2.metric("Envíos Frágiles", len(df[df["es_fragil"] == True]))
            col3.metric("Peso Total (kg)", f"{df['peso_kg'].sum():.2f}")
            
        else:
            st.info("No hay envíos registrados aún.")
    else:
        st.error("Error al conectar con el servidor.")

except Exception as e:
    st.error(f"No se pudo conectar con la API. ¿Está corriendo uvicorn? \n\nError: {e}")
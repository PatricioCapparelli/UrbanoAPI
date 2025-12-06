import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Urbano Logística", page_icon="🚚", layout="wide")

BASE_URL = "https://urbanoapi.onrender.com".rstrip("/")
API_URL = f"{BASE_URL}/envios"

def crear_envio(payload):
    """Envía la petición POST al backend"""
    try:
        res = requests.post(f"{API_URL}/", json=payload)
        return res
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

def eliminar_envio_api(id_envio):
    """Envía la petición DELETE al backend"""
    try:
        res = requests.delete(f"{API_URL}/{id_envio}")
        return res
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

def cargar_datos():
    """Obtiene los datos del backend y devuelve un DataFrame limpio"""
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al obtener datos del servidor.")
            return []
    except Exception as e:
        st.error(f"No se pudo conectar con la API: {e}")
        return []

def mostrar_sidebar():
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
                res = crear_envio(payload)
                if res and res.status_code == 201:
                    st.success(f"¡Creado! Tracking: {res.json()['tracking_number']}")
                elif res:
                    st.error("Error al crear.")
            else:
                st.warning("Completa los datos obligatorios.")

    st.sidebar.markdown("---")
    
    st.sidebar.header("🗑️ Eliminar Envío")
    with st.sidebar.form("form_borrar"):
        id_borrar = st.number_input("ID a eliminar", min_value=1, step=1)
        btn_borrar = st.form_submit_button("Eliminar")
        
        if btn_borrar:
            res = eliminar_envio_api(id_borrar)
            if res and res.status_code == 204:
                st.success(f"Envío {id_borrar} eliminado.")
                st.rerun()
            elif res and res.status_code == 404:
                st.error("ID no encontrado.")

def mostrar_dashboard():
    st.title("🚚 Sistema de Gestión Logística Urbano")
    st.markdown("---")
    
    if st.button("🔄 Actualizar Datos"):
        st.rerun()

    data = cargar_datos()
    
    if data:
        df = pd.DataFrame(data)
        
        cols_deseadas = ["id", "tracking_number", "estado", "destinatario", "direccion", "peso_kg", "es_fragil"]
        cols_finales = [c for c in cols_deseadas if c in df.columns]
        df = df[cols_finales]

        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("### Métricas en Tiempo Real")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Envíos", len(df))
        c2.metric("Envíos Frágiles", len(df[df["es_fragil"] == True]))
        c3.metric("Peso Total (kg)", f"{df['peso_kg'].sum():.2f}")
    else:
        st.info("No hay envíos registrados o no hay conexión.")

if __name__ == "__main__":
    mostrar_sidebar()
    mostrar_dashboard()
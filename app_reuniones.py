import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Registro de Reuniones", layout="centered")

st.title("Registro de Reuniones")

# Horas disponibles en formato de 30 minutos
horas = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]
salas = ["Auditorio A", "Auditorio B", "Sala de Conferencias", "Sala de Juntas"]
herramientas_opciones = ["TV", "Proyector", "Cable HDMI"]

# Cargar datos
@st.cache_data
def cargar_datos():
    try:
        return pd.read_csv("reuniones.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Fecha", "Inicio", "Fin", "Sala", "Asistentes", "Tema", "Herramientas"])

reuniones = cargar_datos()

with st.form("formulario_reunion"):
    col1, col2 = st.columns(2)

    with col1:
        fecha = st.date_input("Fecha")
        hora_inicio = st.selectbox("Hora de inicio", horas)
    with col2:
        sala = st.selectbox("Sala", salas)
        hora_fin = st.selectbox("Hora final", horas)

    asistentes = st.text_input("Asistentes")
    tema = st.text_input("Tema")
    herramientas = st.multiselect("Herramientas tecnológicas", herramientas_opciones)

    submitted = st.form_submit_button("Registrar Reunión")

    if submitted:
        if hora_fin <= hora_inicio:
            st.error("La hora final debe ser mayor a la hora de inicio.")
        elif not (fecha and hora_inicio and hora_fin and sala and asistentes and tema):
            st.error("Todos los campos son obligatorios.")
        else:
            conflicto = reuniones[(reuniones["Fecha"] == str(fecha)) & (reuniones["Sala"] == sala) & ~((reuniones["Fin"] <= hora_inicio) | (reuniones["Inicio"] >= hora_fin))]
            if not conflicto.empty:
                st.error(f"La sala '{sala}' ya está ocupada el {fecha} entre {hora_inicio} y {hora_fin}.")
            else:
                nueva_reunion = pd.DataFrame([{
                    "Fecha": fecha,
                    "Inicio": hora_inicio,
                    "Fin": hora_fin,
                    "Sala": sala,
                    "Asistentes": asistentes,
                    "Tema": tema,
                    "Herramientas": ", ".join(herramientas)
                }])
                reuniones = pd.concat([reuniones, nueva_reunion], ignore_index=True)
                reuniones.to_csv("reuniones.csv", index=False)
                st.success("Reunión registrada con éxito.")

st.subheader("Reuniones Registradas")

filtro_fecha = st.date_input("Filtrar por fecha", value=None, key="filtro_fecha")
if filtro_fecha:
    datos_filtrados = reuniones[reuniones["Fecha"] == str(filtro_fecha)]
else:
    datos_filtrados = reuniones

st.dataframe(datos_filtrados, use_container_width=True)

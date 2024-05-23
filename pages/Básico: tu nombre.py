import streamlit as st
import paho.mqtt.publish as publish
import json

# Título y Subtítulo
st.title("¡Aprende lenguaje de señas colombiano!")
st.subheader("Básico: tu nombre")

# Cuerpo de Texto
st.write("""
En la comunidad de personas sordas, la presentación de los nombres se realiza mediante el uso del alfabeto manual del lenguaje de señas, que vimos en el módulo anterior. Al presentarse, las personas sordas deletrean su nombre letra por letra utilizando cualquiera de sus dos manos. Este método de deletreo permite una comunicación clara y precisa, asegurando que el nombre sea entendido.

Por ejemplo: si una persona se llama "Ana" y quiere presentarse, deletreará "A-N-A" en lenguaje de señas.
""")

# Imagen
st.image("ejemplodeletreo.png")

st.write("""
A continuación, encontrarás un video muy corto que enseña cómo saludar, decir "mi nombre es" y el ejemplo de cómo deletrear un nombre.
""")

# Video
st.video("deletreonombre.mp4")

# Subtítulo y Texto
st.subheader("¡Ponlo en práctica!")

st.write("""
Escribe tu nombre y luego verás unas imágenes en desorden que corresponden a las señas de cada una de las letras de tu nombre. Con tus conocimientos previos del abecedario, identifica cada seña y elige el color correspondiente:
""")

# Input para escribir el nombre
nombre = st.text_input("Escribe solo tu primer nombre (sin tildes)", key="nombre").upper()

if nombre:
    options = ["green", "red"]
    selected_color = st.selectbox("Selecciona un color para enviar al dispositivo:", options)
    message = {"value": selected_color}
    publish.single("nombre", json.dumps(message), hostname="broker.mqttdashboard.com")

    st.write("Mensaje enviado al dispositivo ESP32:", message)




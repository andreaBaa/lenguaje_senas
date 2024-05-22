import paho.mqtt.client as paho
import time
import json
import streamlit as st
import numpy as np
from PIL import Image
from keras.models import load_model

# Callback functions for MQTT
def on_publish(client, userdata, result):
    print("El dato ha sido publicado \n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# MQTT setup
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("LenguManos")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

# Load the model
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Streamlit app
st.title("¡Aprende lenguaje de señas colombiano!")
st.header("Básico: el abecedario")
st.subheader("¿Qué aprenderás?")
st.markdown("""
En esta sección te enseñaremos el abecedario de LSC por medio de un video e imágenes para que luego puedas replicarlo y poder practicar el nuevo conocimiento adquirido.
""")
st.subheader("El abecedario")
st.markdown("""
El Lenguaje de Señas Colombiano (LSC) está conformado por varios elementos y características que lo hacen un sistema de comunicación completo y estructurado. La configuración de la mano (Quirémica) se refiere a las formas que adoptan las manos al realizar diferentes señas. Existen configuraciones básicas que se utilizan como base para formar las señas, y cada una tiene su propia estructura y posición de los dedos. La orientación puede variar hacia adelante, hacia atrás, hacia arriba, hacia abajo, hacia los lados, etc. Los movimientos pueden ser lineales, circulares, repetitivos, y pueden variar en velocidad e intensidad.
""")
st.image("1.png", width=500)
st.image("2.png", width=500)
st.image("3.png", width=500)
st.video("https://www.youtube.com/watch?v=SKeBZpjWTko")
st.subheader("¡Ponlo en práctica!")
st.markdown("""
Antes de empezar, asegúrate de que Streamlit tenga acceso a tu cámara. Te daremos algunas letras para que practiques la posición de la mano. Identifica la letra que estamos pidiendo y posiciona tu mano a 15 cm de la cámara. Por favor, asegúrate de que solo se muestre tu mano, preferiblemente con un fondo blanco (puedes posicionar tu mano enfrente de una pared o de un pedazo de papel). Cuando estés listo, haz clic en “Tomar foto” y espera a tu resultado. Si hiciste la seña correctamente, se encenderá un LED de color verde y se escuchará un sonido indicando que lo has logrado. Si lo has hecho de manera incorrecta, aparecerá en pantalla la palabra “Incorrecto”. Puedes tomar la foto cuantas veces quieras y practicar múltiples veces.
""")

letters = ["A", "B", "C", "D", "I", "K", "L", "N", "O"]
thresholds = [0.4, 0.4, 0.4, 0.4, 0.3, 0.4, 0.4, 0.3, 0.4]

for i, letter in enumerate(letters):
    st.title(letter)
    camera_input_key = f"camera_input_{letter}"
    img_file_buffer = st.camera_input(f"Toma una Foto de {letter}", key=camera_input_key)
    
    if img_file_buffer is not None:
        img = Image.open(img_file_buffer)
        img = img.resize((224, 224))
        img_array = np.array(img)
        normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        
        prediction = model.predict(data)
        print(prediction)
        
        if prediction[0][i] > thresholds[i]:
            st.header(letter)
            st.image(f"{letter}.png", width=500)
            payload = json.dumps({'abc': letter})
            client1.publish("LengSenas", payload, qos=0, retain=False)
            time.sleep(0.2)
        else:
            st.text("Incorrecto")
            st.image(f"{letter}.png", width=500)


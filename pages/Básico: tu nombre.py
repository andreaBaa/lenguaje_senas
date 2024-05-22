#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "your_wifi_ssid";  // Cambia esto a tu SSID de WiFi
const char* password = "your_wifi_password";  // Cambia esto a tu contraseña de WiFi
const char* mqtt_server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient client(espClient);

const int ledRojo = 2;  // GPIO2
const int ledVerde = 4; // GPIO4

void setup() {
  pinMode(ledRojo, OUTPUT);
  pinMode(ledVerde, OUTPUT);

  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe("streamlit/led");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(5000);
    }
  }
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(message);

  if (message == "red") {
    digitalWrite(ledRojo, HIGH);
    digitalWrite(ledVerde, LOW);
  } else if (message == "green") {
    digitalWrite(ledRojo, LOW);
    digitalWrite(ledVerde, HIGH);
  }
}

void loop() {
  client.loop();
}



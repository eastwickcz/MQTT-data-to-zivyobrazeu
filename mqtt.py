import paho.mqtt.client as mqtt
import requests
import json
import time

# Konfigurace MQTT
MQTT_BROKER = "192.168.0.1"
MQTT_PORT = 1883
MQTT_USER = "user"
MQTT_PASSWORD = "password"
MQTT_TOPICS = ["zigbee2mqtt/Teploměr xxx", "zigbee2mqtt/Teploměr yyy", "zigbee2mqtt/Teploměr zzz", "zigbee2mqtt/Teploměr aaa", "zigbee2mqtt/Teploměr bbb"]

# HTTP endpoint
HTTP_ENDPOINT = "http://in.zivyobraz.eu/"
IMPORT_KEY = "XXXxxxXXXxxxXXX"

# Inicializace slovníku pro sledování času posledního odeslání dat
last_sent = {topic: 0 for topic in MQTT_TOPICS}

# Funkce pro zpracování přijatých zpráv z MQTT
def on_message(client, userdata, message):
    current_time = time.time()
    if last_sent[message.topic] + 60 <= current_time:  # Kontrola, zda uplynula alespoň minuta
        try:
            data = json.loads(message.payload.decode("utf-8"))
            room = message.topic.split('/')[-1]
            temperature = data.get('temperature')
            humidity = data.get('humidity')

            if temperature is not None and humidity is not None:
                params = {
                    'import_key': IMPORT_KEY,
                    f'teplota_{room}': temperature,
                    f'vlhkost_{room}': humidity
                }
                response = requests.get(HTTP_ENDPOINT, params=params)
                print(f"Odesláno na HTTP: {response.url}")

                # Aktualizace času posledního odeslání
                last_sent[message.topic] = current_time
            else:
                print(f"Data teploty nebo vlhkosti nejsou dostupná pro místnost {room}.")
        except Exception as e:
            print(f"Chyba při zpracování zprávy: {e}")

# Nastavení MQTT klienta
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = on_message

# Připojení k MQTT brokerovi
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Přihlášení k odběru pro každý topic
for topic in MQTT_TOPICS:
    client.subscribe(topic)

# Neustálé zpracování zpráv
client.loop_forever()

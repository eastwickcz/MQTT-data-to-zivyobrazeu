import paho.mqtt.client as mqtt
import requests
import json
import time

# Konfigurace MQTT
MQTT_BROKER = "192.168.0.1" # Nastavení IP adresy mqtt serveru
MQTT_PORT = 1883 # Port MQTT (1883 bývá nejčastější)
MQTT_USER = "user" # Uživatel pro MQTT
MQTT_PASSWORD = "password" # Heslo pro MQTT
MQTT_TOPICS = ["zigbee2mqtt/Teploměr xxx", "zigbee2mqtt/Teploměr yyy", "zigbee2mqtt/Teploměr zzz", "zigbee2mqtt/Teploměr aaa", "zigbee2mqtt/Teploměr bbb"] #Topics z MQTT, které chceme odesílat na zivyobraz.eu

# HTTP endpoint
HTTP_ENDPOINT = "http://in.zivyobraz.eu/"
IMPORT_KEY = "XXXxxxXXXxxxXXX" # key vygenerovaný od zivyobraz.eu

# Funkce pro zpracování přijatých zpráv z MQTT
def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        room = message.topic.split('/')[-1]  # Získá název místnosti z topicu
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
        else:
            print(f"Data teploty nebo vlhkosti nejsou dostupná pro místnost {room}.")
    except Exception as e:
        print(f"Chyba při zpracování zprávy: {e}")

# Funkce volaná při odpojení od MQTT serveru
def on_disconnect(client, userdata, rc):
    print("Odpojeno od MQTT serveru s kódem: ", rc)
    while True:
        # Pokus o opětovné připojení
        try:
            print("Pokus o opětovné připojení k MQTT serveru...")
            client.reconnect()
            break  # Připojení bylo úspěšné, ukončíme smyčku
        except:
            print("Pokus o připojení selhal, zkouším znovu za 5 sekund...")
            time.sleep(5)  # Počkáme 5 sekund před dalším pokusem

# Nastavení MQTT klienta
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = on_message
client.on_disconnect = on_disconnect  # Přidání handleru pro odpojení

# Připojení k MQTT brokerovi
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Přihlášení k odběru pro každý topic
for topic in MQTT_TOPICS:
    client.subscribe(topic)

# Neustálé zpracování zpráv
client.loop_forever()

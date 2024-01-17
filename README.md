MQTT Teploměr - Integrace s ŽivýObraz.eu
Popis

Tento skript je určen pro sběr teplotních a vlhkostních dat z různých MQTT teploměrů a jejich následné odeslání na HTTP endpoint ŽivýObraz.eu. Skript se připojuje k MQTT brokerovi, přihlašuje se k odběru specifických topics a posílá získaná data na konfigurovaný HTTP server.
Požadavky

    Python 3
    Knihovny: paho-mqtt, requests, json

Instalace

    Nainstalujte potřebné Python knihovny:

    pip install paho-mqtt requests

    Uložte tento skript do souboru a upravte konfiguraci dle vašeho prostředí.

Konfigurace

    MQTT_BROKER: IP adresa MQTT brokeru.
    MQTT_PORT: Port MQTT brokeru (standardně 1883).
    MQTT_USER: Uživatelské jméno pro MQTT.
    MQTT_PASSWORD: Heslo pro MQTT.
    MQTT_TOPICS: Seznam MQTT topics, ze kterých se mají sbírat data.
    HTTP_ENDPOINT: HTTP endpoint pro odeslání dat.
    IMPORT_KEY: Klíč pro autentizaci u HTTP endpointu.

Použití

Spusťte skript a nechte jej běžet. Skript bude neustále naslouchat MQTT zprávám a odesílat data na HTTP server.
Nastavení jako systemd služba

Pro nastavení skriptu jako služby v systému s použitím systemd, proveďte následující kroky:

    Vytvořte nový systemd service soubor. Například mqtt-thermometer.service:

    bash

sudo nano /etc/systemd/system/mqtt-thermometer.service

Vložte do něj následující konfiguraci, přičemž upravte cesty dle vašeho prostředí:

makefile

[Unit]
Description=MQTT Thermometer Service
After=network.target

[Service]
Type=simple
User=<username>
ExecStart=/usr/bin/python3 /cesta/k/vašemu/skriptu.py

[Install]
WantedBy=multi-user.target

Nahraďte <username> uživatelským jménem, pod kterým chcete službu spouštět, a /cesta/k/vašemu/skriptu.py cestou k vašemu skriptu.

Povolte a spusťte službu:

bash

sudo systemctl enable mqtt-thermometer.service
sudo systemctl start mqtt-thermometer.service

Zkontrolujte stav služby:

lua

    sudo systemctl status mqtt-thermometer.service

Tímto způsobem se skript spustí při každém startu systému a bude běžet na pozadí.
Poznámky

    Ujistěte se, že MQTT broker je spuštěn a dostupný.
    Zkontrolujte, zda jsou správně nastaveny topics pro vaše teploměry.
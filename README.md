# MQTT Teploměr - Integrace s ŽivýObraz.eu
## Popis

Tento skript je určen pro sběr teplotních a vlhkostních dat z různých MQTT teploměrů a jejich následné odeslání na HTTP endpoint ŽivýObraz.eu. Skript se připojuje k MQTT brokerovi, přihlašuje se k odběru specifických topics a posílá získaná data na konfigurovaný HTTP server.

Požadavky

    Python3
    Knihovny: paho-mqtt, requests, json

Instalace:

1. Nainstalujte potřebné Python knihovny:

        pip install -r requirements.txt

2. Uložte tento skript do souboru a upravte konfiguraci dle vašeho prostředí.

## Konfigurace

Upravte v souboru mqtt.py následující

        MQTT_BROKER: IP adresa MQTT brokeru.
        MQTT_PORT: Port MQTT brokeru (standardně 1883).
        MQTT_USER: Uživatelské jméno pro MQTT.
        MQTT_PASSWORD: Heslo pro MQTT.
        MQTT_TOPICS: Seznam MQTT topics, ze kterých se mají sbírat data.
        HTTP_ENDPOINT: HTTP endpoint pro odeslání dat.
        IMPORT_KEY: Klíč pro autentizaci u HTTP endpointu.

## Použití

Spusťte skript a nechte jej běžet. Skript bude neustále naslouchat MQTT zprávám a odesílat data na HTTP server.

### Nastavení jako systemd služba

Pro nastavení skriptu jako služby v systému s použitím systemd, proveďte následující kroky:

1. Vytvořte nový systemd service soubor. Například mqtt-thermometer.service:

        sudo nano /etc/systemd/system/mqtt-thermometer.service

2. Vložte do něj následující konfiguraci, přičemž upravte cesty dle vašeho prostředí:

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

3. Povolte a spusťte službu:

        sudo systemctl enable mqtt-thermometer.service
        sudo systemctl start mqtt-thermometer.service

4. Zkontrolujte stav služby:

        sudo systemctl status mqtt-thermometer.service

Tímto způsobem se skript spustí při každém startu systému a bude běžet na pozadí.
Poznámky

    Ujistěte se, že MQTT broker je spuštěn a dostupný.
    Zkontrolujte, zda jsou správně nastaveny topics pro vaše teploměry.
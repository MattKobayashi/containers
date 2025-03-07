# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "paho-mqtt==2.1.0",
#     "tuya-connector-python==0.1.2",
# ]
# ///

#!/usr/bin/env python3
import os
import sys
import json
import paho.mqtt.client as mqtt
from tuya_connector import TuyaOpenAPI

# Check that env vars are set
if (
    "SOLAR_WATTS_ON" in os.environ
    and "SOLAR_WATTS_OFF" in os.environ
    and "MQTT_SERVER" in os.environ
    and "MQTT_TOPIC" in os.environ
    and "MQTT_USER" in os.environ
    and "MQTT_PASS" in os.environ
    and "TUYA_CLIENT_ID" in os.environ
    and "TUYA_CLIENT_SECRET" in os.environ
    and "TUYA_DEVICE_ID" in os.environ
):
    pass
else:
    print(
        "growatt-ev: One or more environment variables are missing.",
        "Please check that all required variables are set!",
    )
    sys.exit()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, reason_code):
    print(
        f"growatt-ev: Connected to MQTT broker with result code: {reason_code}"
    )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(os.environ["MQTT_TOPIC"])


# The callback for when a PUBLISH message is received from the server.
def on_message(msg):
    inverter_data = json.loads(msg.payload.decode("utf-8"))
    inverter_watts = inverter_data["values"]["pvpowerout"] / 10
    print(
        "growatt-ev: Solar system is currently producing",
        round(inverter_watts, 2),
        "W"
    )
    # Connect to Tuya API
    openapi = TuyaOpenAPI(
        "https://openapi.tuyaeu.com",
        os.environ["TUYA_CLIENT_ID"],
        os.environ["TUYA_CLIENT_SECRET"]
    )
    if not openapi.is_connect():
        openapi.connect()

    # Get EV charger status
    ev_charger_props = openapi.get(
        f"/v2.0/cloud/thing/{os.environ['TUYA_DEVICE_ID']}/shadow/properties",
        {"device_id": os.environ["TUYA_DEVICE_ID"]},
    )
    if ev_charger_props["success"] is True:
        ev_charger_status = next(
            (
                props["value"]
                for props
                in ev_charger_props["result"]["properties"]
                if props["code"] == "switch_1"
            ),
            True
        )
    else:
        print("growatt-ev: Cannot get status of EV charger...")
        ev_charger_status = False

    # Switch EV charger on if solar array is producing at least SOLAR_WATTS
    if inverter_watts >= int(os.environ["SOLAR_WATTS_ON"]):
        if ev_charger_status is False:
            print("growatt-ev: Enabling the EV charger...")
            req = openapi.post(
                f"/v2.0/cloud/thing/{os.environ['TUYA_DEVICE_ID']}/shadow/properties/issue",
                {"properties": '{"switch_1": true}'},
            )
            if req["success"] is True:
                print("growatt-ev: EV charger has been enabled!")
            else:
                print("growatt-ev: An error occurred while enabling the EV charger.")
        else:
            print("growatt-ev: EV charger is already enabled, nothing to do!")
    if inverter_watts < int(os.environ["SOLAR_WATTS_OFF"]):
        if ev_charger_status is True:
            print("growatt-ev: Disabling the EV charger...")
            req = openapi.post(
                f"/v2.0/cloud/thing/{os.environ['TUYA_DEVICE_ID']}/shadow/properties/issue",
                {"properties": '{"switch_1": false}'},
            )
            if req["success"] is True:
                print("growatt-ev: EV charger has been disabled!")
            else:
                print("growatt-ev: An error occurred while disabling the EV charger.")
        else:
            print("growatt-ev: EV charger is already disabled, nothing to do!")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set(os.environ["MQTT_USER"], os.environ["MQTT_PASS"])
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(os.environ["MQTT_SERVER"], 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()

#! /usr/bin/env python3
import os
import sys
import growattServer
from tuya_connector import TuyaOpenAPI

# Connect to Growatt API
api = growattServer.GrowattApi(False, "GAGF")
api.server_url = 'https://server.growatt.com/'
login_response = api.login(
    os.environ['GROWATT_USER'],
    os.environ['GROWATT_PASS']
)

# Get current inverter power output
inverter_watts = api.tlx_detail("HMG2A340SM")['data']['pac']
print(
    "growatt-ev: Solar system is currently producing",
    round(inverter_watts, 2),
    "W"
    )

# Connect to Tuya API
openapi = TuyaOpenAPI(
    "https://openapi.tuyaeu.com",
    os.environ['TUYA_CLIENT_ID'],
    os.environ['TUYA_CLIENT_SECRET']
    )
if not openapi.is_connect():
    openapi.connect()

# Get EV charger status
ev_charger_props = openapi.get(
        f"/v2.0/cloud/thing/{os.environ['TUYA_DEVICE_ID']}/shadow/properties",
        {"device_id": os.environ['TUYA_DEVICE_ID']}
        )
if ev_charger_props['success'] is True:
    ev_charger_status = [
        props['value'] for props
        in ev_charger_props['result']['properties']
        if props['code'] == 'switch_1'
        ]
else:
    print("growatt-ev: Cannot get status of EV charger. Exiting...")
    sys.exit()

# Switch EV charger on if solar array is producing at least 1.5kW
if inverter_watts >= 1500:
    if ev_charger_status is False:
        print("growatt-ev: Enabling the EV charger...")
        req = openapi.post(
            f"/v2.0/cloud/thing/{os.environ['TUYA_DEVICE_ID']}/shadow/properties/issue",
            {"properties": "{\"switch_1\": true}"}
        )
        if req['success'] is True:
            print("growatt-ev: EV charger has been enabled!")
        else:
            print(
                "growatt-ev: An error occurred while enabling the EV charger."
            )
    else:
        print("growatt-ev: EV charger is already enabled, nothing to do!")
else:
    if ev_charger_status is True:
        print("growatt-ev: Disabling the EV charger...")
        req = openapi.post(
            f"/v2.0/cloud/thing/{os.environ['TUYA_DEVICE_ID']}/shadow/properties/issue",
            {"properties": "{\"switch_1\": true}"}
        )
        if req['success'] is True:
            print("growatt-ev: EV charger has been disabled!")
        else:
            print(
                "growatt-ev: An error occurred while disabling the EV charger."
            )
    else:
        print("growatt-ev: EV charger is already disabled, nothing to do!")

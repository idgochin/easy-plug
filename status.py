import paho.mqtt.client as mqtt
import json
import time
import psutil
THINGSBOARD_HOST = "iservice.thddns.net"  # Change if using self-hosted
ACCESS_TOKEN = "EZP0001"

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 2222, 60)

# while True:
#     payload = {
#         "temperature": 25.5,
#         "humidity": 60
#     }
#     client.publish("v1/devices/me/telemetry", json.dumps(payload))
#     print(f"Sent: {payload}")
#     time.sleep(5)




while True:
    payload = {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
    client.publish("v1/devices/me/telemetry", json.dumps(payload))
    print(f"Sent: {payload}")
    time.sleep(5)

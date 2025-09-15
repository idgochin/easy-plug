# import paho.mqtt.client as mqtt
# import json
# import time
# import psutil
# THINGSBOARD_HOST = "iservice.thddns.net"  # Change if using self-hosted
# ACCESS_TOKEN = "EZP0001"

# client = mqtt.Client()
# client.username_pw_set(ACCESS_TOKEN)
# client.connect(THINGSBOARD_HOST, 2222, 60)

# while True:
#     payload = {
#         "cpu_usage": psutil.cpu_percent(),
#         "memory_usage": psutil.virtual_memory().percent,
#         "disk_usage": psutil.disk_usage('/').percent
#     }
#     client.publish("v1/devices/me/telemetry", json.dumps(payload))
#     print(f"Sent: {payload}")
#     time.sleep(5)

# import paho.mqtt.client as mqtt
# import json
# import time
# import psutil

# THINGSBOARD_HOST = "iservice.thddns.net"
# ACCESS_TOKEN = "EZP0001"

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Connected to ThingsBoard")
#     else:
#         print(f"Failed to connect, return code {rc}")

# def on_disconnect(client, userdata, rc):
#     print(f"Disconnected with result code {rc}")

# def on_publish(client, userdata, mid):
#     print(f"Message {mid} published")

# client = mqtt.Client()
# client.username_pw_set(ACCESS_TOKEN)
# client.on_connect = on_connect
# client.on_disconnect = on_disconnect
# client.on_publish = on_publish

# client.connect(THINGSBOARD_HOST, 2222, 60)
# client.loop_start()

# while True:
#     if client.is_connected():
#         payload = {
#             "cpu_usage": psutil.cpu_percent(),
#             "memory_usage": psutil.virtual_memory().percent,
#             "disk_usage": psutil.disk_usage('/').percent
#         }
#         result = client.publish("v1/devices/me/telemetry", json.dumps(payload))
#         print(f"Sent: {payload}, Result: {result.rc}")
#     else:
#         print("Not connected, attempting to reconnect...")
#         client.reconnect()
    
#     time.sleep(5)

import paho.mqtt.client as mqtt
import json
import time
import psutil

def get_cpu_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = int(f.read()) / 1000.0
            return round(temp, 2)
    except:
        return None

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code {rc}")

THINGSBOARD_HOST = "iservice.thddns.net"
ACCESS_TOKEN = "EZP0001"

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(THINGSBOARD_HOST, 2222, 30)
client.loop_start()

while True:
    if client.is_connected():
        payload = {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "cpu_temperature": get_cpu_temperature()
        }
        
        result = client.publish("v1/devices/me/telemetry", json.dumps(payload))
        if result.rc == 0:
            print(f"Sent: {payload}")
        else:
            print(f"Failed to send, error: {result.rc}")
    else:
        print("Reconnecting...")
        client.reconnect()
    
    time.sleep(5)
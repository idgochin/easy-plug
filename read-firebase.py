import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess
import time
import icecream as ic

# Path to your service account key
service_account_key_path = "firebase/serviceAccountKey.json"

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://easy-plug-bc6ca-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Define the database reference
ref = db.reference('plugs')

# Read data and take action
def monitor_plugs():
    try:
        while True:
            data = ref.get()
            # print("Data from Realtime Database:", data)
            ic(data)

            if data:
                # Check EZP000101 status
                plug1 = data.get('EZP000101', {})
                if plug1.get('status') == 'active':
                    print("Activating Relay 1 and LED 1 for EZP000101")
                    subprocess.run(['python3', 'plug1.py'])

                # Check EZP000102 status
                plug2 = data.get('EZP000102', {})
                if plug2.get('status') == 'active':
                    print("Activating Relay 2 and LED 2 for EZP000102")
                    subprocess.run(['python3', 'plug2.py'])

            time.sleep(5)  # Check every 5 seconds

    except Exception as e:
        print("Error monitoring plugs:", e)

if __name__ == "__main__":
    monitor_plugs()

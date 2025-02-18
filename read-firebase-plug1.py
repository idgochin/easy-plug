import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess
import time
import json
import psutil


# Path to your service account key
service_account_key_path = "firebase/serviceAccountKey.json"

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://easy-plug-bc6ca-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Define the database reference
ref = db.reference('plugs')

# Balance file path
BALANCE_FILE_PATH = "balance-plug1.json"

# Function to read balance from the JSON file
def read_balance_from_file():
    try:
        with open(BALANCE_FILE_PATH, "r") as file:
            data = json.load(file)
            return data.get("balance", 0.0)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file not found or corrupted, create a default balance
        write_balance_to_file(0.0)
        return 0.0

# Function to write balance to the JSON file
def write_balance_to_file(balance):
    with open(BALANCE_FILE_PATH, "w") as file:
        json.dump({"balance": balance}, file)

# Function to check if plug1.py is already running
def is_plug1_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and "plug1.py" in proc.info['cmdline']:
                print(f"plug1.py is already running with PID: {proc.info['pid']}")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


# Read data and take action
def monitor_plugs():
    try:
        inactive_start_time = None
        while True:
            data = ref.get()
            print("Data from Realtime Database:", data)
            
            if data:
                plug1 = data.get('EZP000101', {})
                if plug1.get('status') == 'active':
                    write_balance_to_file(float(plug1.get('balance', 0.0)))
                    inactive_start_time = None  # Reset timer if active
                    break
                else:
                    if inactive_start_time is None:
                        inactive_start_time = time.time()
                        print(inactive_start_time)
                    elif time.time() - inactive_start_time > 600:  # 300 seconds = 5 minutes
                        print(inactive_start_time)
                        print("Plug1 has been inactive for 10 minutes. Ending script.")
                        return
                    print(time.time() - inactive_start_time)
            time.sleep(5)

                
        print("Activating Relay 1 and LED 1 for EZP000101")
        subprocess.run(['python3', 'delete-pay.py'])

        # Check if plug1.py is already running before starting it
        if not is_plug1_running():
            subprocess.run(['python3', 'plug1.py'])
        else:
            print("Skipping plug1.py execution as it is already running.")

        #subprocess.run(['python3', 'plug1.py'])

    except Exception as e:
        print("Error monitoring plugs:", e)


    

if __name__ == "__main__":
    monitor_plugs()

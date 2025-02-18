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

# Balance file paths
BALANCE_FILES = {
    "EZP000101": "balance-plug1.json",
    "EZP000102": "balance-plug2.json",
}

# Function to read balance from the JSON file
def read_balance_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return float(data.get("balance", 0.0))
    except (FileNotFoundError, json.JSONDecodeError):
        write_balance_to_file(file_path, 0.0)
        return 0.0

# Function to write balance to the JSON file
def write_balance_to_file(file_path, balance):
    with open(file_path, "w") as file:
        json.dump({"balance": balance}, file)

# Function to check if a script is already running
def is_script_running(script_name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and any(script_name in cmd for cmd in proc.info['cmdline']):
                print(f"{script_name} is already running with PID: {proc.info['pid']}")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

# Monitor plugs
def monitor_plugs():
    try:
        inactive_start_time = {}

        while True:
            data = ref.get()
            print("Data from Realtime Database:", data)

            if data:
                for plug_id, plug_data in data.items():
                    if plug_id not in BALANCE_FILES:
                        print(f"Unknown plug_id: {plug_id}, skipping...")
                        continue

                    balance_file = BALANCE_FILES[plug_id]
                    plug_status = plug_data.get('status', 'inactive')

                    if plug_status == 'active':
                        # Update balance
                        write_balance_to_file(balance_file, float(plug_data.get('balance', 0.0)))
                        inactive_start_time[plug_id] = None  # Reset timer if active

                        # Activate relay and LED
                        print(f"Activating Relay and LED for {plug_id}")

                        # Run delete-pay.py to update balance
                        subprocess.run(['python3', 'delete-pay.py', plug_id])

                        # Run corresponding plug script
                        script_name = f"plug{plug_id[-1]}.py"  # plug1.py for EZP000101, plug2.py for EZP000102
                        if not is_script_running(script_name):
                            subprocess.run(['python3', script_name])
                        else:
                            print(f"Skipping {script_name} execution as it is already running.")
                        return

                    else:
                        if plug_id not in inactive_start_time:
                            inactive_start_time[plug_id] = time.time()
                        elif time.time() - inactive_start_time[plug_id] > 600:
                            print(f"{plug_id} has been inactive for 10 minutes. Ending script.")
                            return

            time.sleep(5)

    except Exception as e:
        print("Error monitoring plugs:", e)


if __name__ == "__main__":
    monitor_plugs()

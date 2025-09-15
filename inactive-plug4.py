import firebase_admin
from firebase_admin import credentials, db

# Path to your service account key JSON file
service_account_key_path = "firebase/serviceAccountKey.json"

# Initialize the Firebase app with the service account and database URL
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://easy-plug-bc6ca-default-rtdb.asia-southeast1.firebasedatabase.app'
})

# Create a reference to the specific node you want to update
ref = db.reference("plugs/EZP000104")

# Data to be put at this node
data = {
    "key": "easyplug@12345",
    "status": "inactive",
    "balance": "0",
    "plugId": "EZP000104"
}

# Put (overwrite) the data at the given node
# ref.set(data)

# Patch (update) only the specified fields at the given node
ref.update(data)

print("Data has been updated.")

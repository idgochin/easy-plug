import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Path to your service account key
service_account_key_path = "firebase/serviceAccountKey.json"

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://easy-plug-bc6ca-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Define the database reference
ref = db.reference('plugs')

# Read data
def get_data():
    try:
        data = ref.get()
        print("Data from Realtime Database:", data)
        return data
    except Exception as e:
        print("Error reading data:", e)

if __name__ == "__main__":
    get_data()

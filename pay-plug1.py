import requests
import json
import math
import os
# Balance file paths
BALANCE_FILES = {
    "EZP000101": "balance-plug1.json",
    "EZP000102": "balance-plug2.json",
}

# Function to read balance from the JSON file
def read_data_from_file(plug_id):
    file_path = BALANCE_FILES.get(plug_id, "balance-plug1.json")  # Default to plug1.json if unknown
    try:
        with open(file_path, "r") as file:
            data_json = json.load(file)
            # return float(data.get("balance", 0.0))

            total_price = data_json.get("total_price", 0.0)
            rounded_price = math.ceil(total_price)

            data = {
                "device_id": plug_id,
                "total_price": rounded_price,
                "detail": "EasyPlug",
                "tel": data_json.get("customer", "")
            }
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # If file not found or corrupted, create a default balance
        # write_balance_to_file(plug_id, 0.0)
        return {}
    
# Function to write balance to the JSON file
def write_balance_to_file(plug_id, total_price):
    file_path = BALANCE_FILES.get(plug_id, "balance-plug1.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # If total_price is 0, reset the balance completely
    if total_price == 0.0:
        data["balance"] = 0.0
        data["total_price"] = 0.0
        data["plug_status"] = "inactive"
        data["customer"] = ""

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Load token from token.json
with open("pupa-token.json", "r") as file:
    token_data = json.load(file)

url = "https://pupa.pea.co.th/pupapay/finish-usage/"
headers = {
    "Authorization": token_data["Authorization"],  # Load token from JSON
    "Content-Type": "application/json"
}
# data = {
#     "device_id": "EZP000101",
#     "total_price": "0",
#     "detail": "EasyPlug",
#     "tel": "0922478181"
# }

data = read_data_from_file("EZP000101")
print("data is",data)

response = requests.post(url, json=data, headers=headers)

# Print response
print("Status Code:", response.status_code)
print("Response Body:", response.text)

write_balance_to_file("EZP000101", 0)

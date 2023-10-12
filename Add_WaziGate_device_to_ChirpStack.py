import requests
import json

# ChirpStack API server URL
api_url = "http://192.168.189.11:8080/api"

# ChirpStack JWT API authentication token (replace with your token)
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhcyIsImV4cCI6MTY5NjQ5NzI0OCwiaWQiOjEsImlzcyI6ImFzIiwibmJmIjoxNjk2NDEwODQ4LCJzdWIiOiJ1c2VyIiwidXNlcm5hbWUiOiJhZG1pbiJ9.7ifZXr47tLiy_1qmo3-H1t6UHB7lecSI-iHUY6LyKGw"
headers = {
    "Grpc-Metadata-Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


# ===========================================
# Create an OTAA LoRaWAN device on ChirpStack
# ===========================================
# Device details
device_name = "WaziHAT_Pro_for_SenseCap"
dev_eui = "2CF7F1C0443001A8"
app_eui = "8000000000000009"
app_key = "6E184C1F22B8512F41AFE87A2C788DA7"
device_profile_id = "c6e4e6e9-de98-48a6-8646-8e6f2ac88b0a" # Replace with the device profile for OTAA

# define device data
device_data = {
    "device": {
        "applicationID": 1,
        "name": device_name,
        "devEUI": dev_eui,
        "description": "SenseCap S2120 WeatherStation",
        "deviceProfileID": device_profile_id,  
        "isDisabled": False,
        "skipFCntCheck": True,
        "isABP": False,  # Set to False for OTAA activation
        "tags": {},
    }
}

# Create the device
create_device_response = requests.post(f"{api_url}/devices", data=json.dumps(device_data), headers=headers)
print("create_device_response status code : ",create_device_response.status_code)
if create_device_response.status_code == 200:
    print("OTAA Device created successfully.")
else:
    print("Failed to create the OTAA device!")
    print(create_device_response.content)
    print("======")


# Prepare the OTAA AppKey data, we use the network key
otaa_key_data = {
    "deviceKeys": {
        "devEUI": dev_eui,
        "nwkKey": app_key,
    }
}

# Set the OTAA AppKey for the device
set_otaa_key_response = requests.post(f"{api_url}/devices/{dev_eui}/keys", data=json.dumps(otaa_key_data), headers=headers)
print("set_otaa_key_response status code : ",set_otaa_key_response.status_code)
if set_otaa_key_response.status_code == 200:
    print("OTAA AppKey set successfully.")
else:
    print("Failed to set the OTAA AppKey!")
    print(set_otaa_key_response.content)
    print("======")
# ===========================================


"""
# ==============================
# Get information about a device
# ==============================
response = requests.get(f"{api_url}/devices/aa555a0021011d01", headers=headers)
print("response status code : ",response.status_code)
if response.status_code == 200:
    data = response.json()
    print("Devices: ")
    print(json.dumps(data, indent=2))
else:
    print("Failed to retrieve data!")
    print(response.content)
    print("======")
# ===========================================
"""


"""
# ===========================================
# Get a device keys on ChirpStack
# ===========================================
dev_eui = "2CF7F1C0443001A8"

# Get the device keys
device_key_response = requests.get(f"{api_url}/devices/{dev_eui}/keys", headers=headers)
print("device_key_response status code : ",device_key_response.status_code)
if device_key_response.status_code == 200:
    data = device_key_response.json()
    print("Device keys: ")
    print(json.dumps(data, indent=2))
else:
    print("Failed to retrieve device keys!")
    print(device_key_response.content)
    print("======")
# successful request returns: Device keys:
#{
#  "deviceKeys": {
#    "devEUI": "a84041498183b4d4",
#    "nwkKey": "8313129972ba51b6ac85962838982b69",
#    "appKey": "00000000000000000000000000000000",
#    "genAppKey": ""
#  }
#}
# ===========================================
"""


"""
# =============================================
# Get activation and session keys for a device
# =============================================
dev_eui = "A84041498183B4D4"
activation_request_response = requests.get(f"{api_url}/devices/{dev_eui}/activation", headers=headers)
print("activation_request_response status code : ",activation_request_response.status_code)
if activation_request_response.status_code == 200:
    activation_data = activation_request_response.json()
    #print(json.dumps(activation_data, indent=2))
   
    # Extract Device Address, NwkSKey, and AppSKey from the response
    device_address = activation_data["deviceActivation"]["devAddr"]
    nwk_skey = activation_data["deviceActivation"]["nwkSEncKey"]
    app_skey = activation_data["deviceActivation"]["appSKey"]
    
    print("Device Address:", device_address)
    print("Network Session Key (NwkSKey):", nwk_skey)
    print("Application Session Key (AppSKey):", app_skey)

else:
    print("Failed to retrieve activation and session keys!")
    print(activation_request_response.content)
    print("======")
"""
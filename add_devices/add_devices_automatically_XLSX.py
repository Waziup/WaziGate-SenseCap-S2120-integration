import argparse
import pandas as pd
import urllib.parse
import requests
import sys

Token = ''
Device_url = ''

## EXTRACT CUSTOM IDs FROM XLSX
def load_xlsx(filename = "SmartTrap_LoRa_keys.xlsx"):
    # Load the Excel file
    df = pd.read_excel(filename)

    # Select a column by name (replace 'ColumnName' with the real one)
    column_data = df[['Name', 'DevAddr', 'NWKSKEY', 'APPSKEY']]

    # Print each value in that column
    for index, row in column_data.iterrows():
        print(index, row['Name'], row['DevAddr'], row['NWKSKEY'], row['APPSKEY'])

    return column_data

## MAKE API CALL TO GET TOKEN
def get_token(ip_wg):
    token = ''
    token_url = ip_wg + "/auth/token"

    # Parse the URL
    parsed_token_url = urllib.parse.urlsplit(token_url)

    # Encode the query parameters
    encoded_query = urllib.parse.quote(parsed_token_url.query, safe='=&')

    # Reconstruct the URL with the encoded query
    encoded_url = urllib.parse.urlunsplit((parsed_token_url.scheme, 
                                        parsed_token_url.netloc, 
                                        parsed_token_url.path, 
                                        encoded_query, 
                                        parsed_token_url.fragment))

    # Define headers for the POST request
    headers = {
        'accept': 'application/json',
        #'Content-Type': 'application/json',  # Make sure to set Content-Type
    }

    # Define data for the GET request
    data = {
        'username': 'admin',
        'password': 'loragateway',
    }

    try:
        # Send a GET request to the API
        response = requests.post(encoded_url, headers=headers, json=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # The response content contains the data from the API
            token = response.json()
            print("Token retrieved successfully:", token)

            return token
        else:
            print("Request failed with status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection errors)
        print("Request error:", e)
        return None
    
# UPLOAD forwarder codec: (decoding does not take place)
def post_custom_wazigate_codec(ip_wg):
    new_codec_script = """
        /**
        * Entry, decoder.js
        */
        function bytes2HexString(bytes) {
            return Array.from(bytes) // Ensure bytes is an array
                .map(byte => byte.toString(16).padStart(2, '0')) // Convert to hex
                .join('');
        }

        function Decode(port, bytes) {
            return { sensor1: bytes2HexString(bytes) };
        }
        """

    json_body = {
        "name": "LoRaForwarderHEX_flytrap",
        "mime": "application/javascript",
        "script": new_codec_script
    }

    try:
        response = requests.post(
            ip_wg + "/codecs",  # <-- Replace with IP or base URL
            json=json_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {Token}"  # <-- include token if required
            }
        )

        if response.status_code == 200:
            print("New codec ID:", response.text)
            return response.text
        else:
            print("Request failed:", response.status_code, response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error at POST_custom_WaziGate_CODEC: {e}")
        return None
    
def add_device(name, ip_wg):
    global Device_url

    Device_url = f"{ip_wg}/devices"

    # Parse the URL
    parsed_url = urllib.parse.urlsplit(Device_url)
    
    # Encode the query parameters
    encoded_query = urllib.parse.quote(parsed_url.query, safe='=&')
    
    # Reconstruct the URL with the encoded query
    encoded_url = urllib.parse.urlunsplit((parsed_url.scheme,
                                           parsed_url.netloc,
                                           parsed_url.path,
                                           encoded_query,
                                           parsed_url.fragment))
    
    # Define headers for the GET request
    headers = {
        'Authorization': f'Bearer {Token}',
    }
    
    data = {
        'name': name,
    }
    
    try:
        # Send a GET request to the API
        response = requests.post(encoded_url, headers=headers, json=data)
    
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # The response content contains the data from the API
            response_ok = response.json()
            return response.text.strip().strip('"')
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection errors)
        print("Request error:", e, "Error in adding new device!")
        return None

# ADD meta data
def add_meta(index, returned_device_ids, dev_addr, net_shared_key, app_key, codec_id):
    specific_device_url = Device_url + "/" + returned_device_ids[index] + "/meta"
    print(specific_device_url)
    # Parse the URL
    parsed_url = urllib.parse.urlsplit(specific_device_url)
    
    # Encode the query parameters
    encoded_query = urllib.parse.quote(parsed_url.query, safe='=&')
    
    # Reconstruct the URL with the encoded query
    encoded_url = urllib.parse.urlunsplit((parsed_url.scheme,
                                           parsed_url.netloc,
                                           parsed_url.path,
                                           encoded_query,
                                           parsed_url.fragment))
    
    # Define headers for the GET request
    headers = {
        'Authorization': f'Bearer {Token}',
    }
    
    data = {
        "codec": codec_id,
        "lorawan": {
            "appSKey": app_key,
            "devAddr": dev_addr,
            "nwkSEncKey": net_shared_key,
            "profile": "WaziDev"
        }
    }

    
    try:
        # Send a GET request to the API
        response = requests.post(encoded_url, headers=headers, json=data)
        print(response.text)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # The response content contains the data from the  
            print('[200] Response: ' + response.text)
        else:
            print("[add_meta]Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            response_ok = None
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection errors)
        print("Request error:", e, "Error changing device metadata!")

def main(ip, filename) -> int:
    global Token

    # get data from xlsx
    column_data = load_xlsx(filename)

    # get token
    Token = get_token(ip)

    # add codec
    codec_id = post_custom_wazigate_codec(ip)

    # add devices to WG and change metadata
    returned_device_ids = []
    for index, row in column_data.iterrows():
        # add a device
        returned_device_id = add_device(row['Name'], ip)
        returned_device_ids.append(returned_device_id)
        # add metadata
        add_meta(index, returned_device_ids, row['DevAddr'], row['NWKSKEY'], row['APPSKEY'], codec_id)

    print(returned_device_ids)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A simple script to add devices from xlsx file to WaziGate. Look at the xlsx file for reference, the column names need to be identical.")
    parser.add_argument("--ip", type=str, default="http://wazigate.local", help="Ip of wazigate in local subnet. e.g. http://192.168.1.29")
    parser.add_argument("--filename", type=str, default="SmartTrap_LoRa_keys.xlsx", help="Path and filename of the spreadsheet that has ABP credentials. e.g. SmartTrap_LoRa_keys.xlsx")

    args = parser.parse_args()

    main(ip=args.ip, filename=args.filename)
# WaziGate Device Provisioning Script

This Python script automates the provisioning of LoRaWAN ABP devices on a WaziGate.  
It performs the following actions:

1. Reads device credentials from an Excel (.xlsx) file  
2. Retrieves an authentication token from WaziGate  
3. Uploads a custom JavaScript codec  
4. Registers each device on WaziGate  
5. Updates device metadata (LoRaWAN keys and codec assignment)

---

## Requirements

- Python 3.8 or newer  
- WaziGate accessible on the local network  
- Excel file with columns: `Name`, `DevAddr`, `NWKSKEY`, `APPSKEY`

---

## Installation

```bash
git clone https://github.com/<your-repo>/wazigate-provisioning.git
cd wazigate-provisioning
pip install -r requirements.txt
```

Create a `requirements.txt` with:

```
pandas
requests
openpyxl
```

---

## Excel Format

The `.xlsx` file must contain the following column headers:

| Name   | DevAddr   | NWKSKEY    | APPSKEY    |
|--------|-----------|------------|------------|
| Trap01 | 26011AF3  | ABCD1234…  | 5678EFGH…  |
| Trap02 | 26011B02  | 1122AABB…  | 3344CCDD…  |

---

## Usage

```bash
python add_devices.py --ip http://192.168.1.29 --filename SmartTrap_LoRa_keys.xlsx
```

| Argument     | Description | Default |
|--------------|-------------|---------|
| `--ip`       | WaziGate base URL (must include http://) | `http://192.168.1.29l` |
| `--filename` | Path to the Excel spreadsheet           | `SmartTrap_LoRa_keys.xlsx` |

---

## Script Workflow

| Step | Action |
|------|--------|
| 1 | Load device credentials from the spreadsheet |
| 2 | Authenticate with WaziGate to obtain an access token |
| 3 | Upload a JavaScript codec |
| 4 | Create a device for each spreadsheet row |
| 5 | Update device metadata with LoRaWAN credentials and codec reference |

---

## Notes

- Default WaziGate credentials used are `admin` / `loragateway`. Modify in the script if different.
- The codec is uploaded only once and reused across all devices.
- The script does not check for existing devices with identical names; this can be added if needed.

---

## Planned Improvements

- Add support for updating devices using `PUT /devices/{id}` if `/meta` endpoint changes
- Optional OTAA support (`AppKey`, `JoinEUI`)
- Skip devices that already exist
- Optional CSV file input

---

## License

MIT License
import os
import requests
from db_config import collection
from datetime import datetime


def check_otx(ip):
    OTX_API_KEY = os.getenv("OTX_API_KEY")

    url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general"

    headers = {
        "X-OTX-API-KEY": OTX_API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        pulse_count = len(data.get("pulse_info", {}).get("pulses", []))

        return pulse_count
    else:
        print(f"[ERROR] OTX failed for {ip}")
        return None


print("[START] Collecting threat intel...\n")

ip_targets = ["8.8.4.4", "9.9.9.9"]

for ip in ip_targets:
    pulse_count = check_otx(ip)

    if pulse_count is not None:
        if collection.find_one({"ip": ip}) is None:
            collection.insert_one({
                "ip": ip,
                "source": "OTX",
                "pulse_count": pulse_count,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"[+] Inserted: {ip}")
        else:
            print(f"[!] Already exists: {ip}")

print("[DONE]")

import os
import requests
from db_config import collection
from datetime import datetime 

API_KEY = os.getenv("VT_API_KEY")

# 👉 test IP list (baad me tu change kar sakta hai)
ip_targets = ["8.8.4.4", "9.9.9.9"]

def get_risk_level(malicious):
    # 👉 custom logic (isko tweak kar sakta hai)
    if malicious >= 10:
        return "high"
    elif malicious >= 5:
        return "medium"
    else:
        return "low"

print("[START] Collecting threat intel...\n")

for ip in ip_targets:

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {
    "x-apikey": API_KEY
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    result = response.json()
    
    stats = result["data"]["attributes"]["last_analysis_stats"]
    malicious = stats.get("malicious", 0)

    risk = get_risk_level(malicious)

    # Duplicate check
    if collection.find_one({"ip": ip}) is None:
        data = {
    "ip": ip,
    "source": "VirusTotal",
    "risk": risk_level,
    "malicious": malicious,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

        collection.insert_one(data)
        print(f"[+] Inserted: {ip} | Risk: {risk}")
    else:
        print(f"[!] Already exists: {ip}")

else:
    print(f"[ERROR] Failed for {ip} | Status: {response.status_code}")
    headers = {
        "x-apikey": API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        stats = data["data"]["attributes"]["last_analysis_stats"]
        malicious_count = stats["malicious"]

        risk = get_risk_level(malicious_count)

        # 👉 duplicate check
        if collection.find_one({"ip": ip}) is None:

            record = {
                "ip": ip,
                "malicious_count": malicious_count,
                "risk": risk,
                "source": "virustotal"
            }

            collection.insert_one(record)

            print(f"[+] Added: {ip}")
            print(f"    Malicious: {malicious_count}")
            print(f"    Risk: {risk}\n")

        else:
            print(f"[!] Skipped (already exists): {ip}\n")

    else:
        print(f"[ERROR] API failed for {ip}")

print("[DONE] Data collection finished.")

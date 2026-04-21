from db_config import collection

print("\n[] Threat Intelligence Dashboard\n")

# Counts
total = collection.count_documents({})
high = collection.count_documents({"risk": "high"})
medium = collection.count_documents({"risk": "medium"})
low = collection.count_documents({"risk": "low"})

print(f"Total IPs Scanned: {total}")
print(f"High Risk: {high}")
print(f"Medium Risk: {medium}")
print(f"Low Risk: {low}")

# Sorting order (high → medium → low)
risk_order = {"high": 1, "medium": 2, "low": 3}

print("\n Detailed Report (Sorted by Risk):\n")

data_list = list(collection.find())

# Sort manually
data_list.sort(key=lambda x: risk_order.get(x.get("risk", "").lower(), 3))

for data in data_list:
    ip = data.get("ip", "N/A")
    risk = data.get("risk", "N/A")
    malicious = data.get("malicious", 0)
    source = data.get("source", "VirusTotal")
    timestamp = data.get("timestamp", "N/A")

    print(f"IP: {ip}")
    print(f"Risk: {risk} | Malicious: {malicious}")
    print(f"Source: {source}")
    print(f"Timestamp: {timestamp}")
    print("-" * 40)

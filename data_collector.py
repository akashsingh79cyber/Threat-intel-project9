import requests
from db_config import collection

print("Data Collector Started...")

# Dummy test IP list (real API baad me use karenge)
ip_list = ["8.8.8.8", "1.1.1.1", "192.168.1.1"]

for ip in ip_list:
    # Duplicate check
    if collection.find_one({"ip": ip}) is None:
        data = {
            "ip": ip,
            "source": "test",
            "risk": "medium"
        }
        collection.insert_one(data)
        print(f"Inserted: {ip}")
    else:
        print(f"Already exists: {ip}")

print("Done")

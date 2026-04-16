from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["threat_intel"]
collection = db["malicious_ips"]

print("DB Connected Successfully")

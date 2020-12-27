import requests
import json
import time
import socket
import ClaymoreRPC

def create_session_call():
    url = "http://192.168.31.200:5000/endpoints/create_session"

    payload={
        "pc_identifier": socket.gethostname()
    }
    payload = json.dumps(payload)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)

def ping_server(session_id, details, hashrate="", temperature="", power_consumption=""):
    url = "http://192.168.31.200:5000/endpoints/ping"

    payload={
        "details": details,
        "session_id": session_id,
        "hashrate": hashrate,
        "temperature": temperature,
        "power_consumption": power_consumption
    }
    payload = json.dumps(payload)
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

def get_mining_data(claymore_miner_object):
    return claymore_miner_object.unified_data()

returned_object = create_session_call()

if returned_object["status"] != True:
    print("server error")
    exit()
    
print("successful session creation!")
session_id = returned_object["inserted_id"]
ping_server(session_id, "init ping")
print("Session id:", session_id)
claymore_miner = ClaymoreRPC.ClaymoreRPC("192.168.31.20", 3333)
while True:
    try:
        mining_data = get_mining_data(claymore_miner)
        
    except:
        print("Claymore API interface failed")
        time.sleep(10)
        continue

    # should divide by million to get MH/s
    hashrate = mining_data["total hashrate"] / 1_000_000
    power = mining_data["power consumption"]
    temps = []
    for index, gpu in enumerate(mining_data["GPUs"]):
        gpu_single = mining_data["GPUs"][f"GPU {index}"]
        temp = gpu_single["temp"]
        temps.append(str(temp))

    temps_str = ""
    temps_str = ", ".join(temps)
    print(hashrate, temps_str, power)
    ping_server(session_id, "all good", str(hashrate), str(temps_str), str(power))
    time.sleep(2)
import requests
import json
import time
import socket

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

def ping_server(session_id, details):
    url = "http://192.168.31.200:5000/endpoints/ping"

    payload={
        "details": details,
        "session_id": session_id
    }
    payload = json.dumps(payload)
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)


returned_object = create_session_call()

if returned_object["status"] != True:
    print("server error")
    exit()
    
print("successful session creation!")
session_id = returned_object["inserted_id"]
print("Session id:", session_id)

while True:
    ping_server(session_id, "hashrate here")
    time.sleep(30)
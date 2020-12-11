import requests
import json
import datetime
import time

def get_all_active_sessions():
    url = "http://192.168.31.200:5000/endpoints/all_active"
    response = requests.request("POST", url)

    return json.loads(response.text)

def get_single_active_session_info(session_id):
    url = "http://192.168.31.200:5000/endpoints/check_status"

    payload = {
        "session_id": str(session_id)
    }
    payload = json.dumps(payload)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)

def destroy_session_and_restart(session_id):
    url = "http://192.168.31.200:5000/endpoints/end_session"

    payload = {
        "session_id": str(session_id)
    }
    payload = json.dumps(payload)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)

if __name__ == "__main__":
    while True:
        all_sessions = get_all_active_sessions()["active_sessions"]
        
        for session in all_sessions:
            session_id = session["session_id"]
            pc_identifier = session["pc_identifier"]
            date_initiated = session["date_initiated"]
            date_initiated_dt_object = datetime.datetime.strptime(date_initiated, '%Y-%m-%d %H:%M:%S')

            date_delta_has_been_running_for = datetime.datetime.now() - date_initiated_dt_object


            print(f"{session_id} has been running for {str(date_delta_has_been_running_for)}")


            session_last_ping_info = get_single_active_session_info(session_id)
            ping_details = session_last_ping_info["details"]
            ping_time = session_last_ping_info["date_last_pinged"]
            ping_time_dt_object = datetime.datetime.strptime(ping_time, '%Y-%m-%d %H:%M:%S')

            date_delta_last_ping = datetime.datetime.now() - ping_time_dt_object
            time_passed_in_secs = date_delta_last_ping.total_seconds()
            print(f"{time_passed_in_secs} seconds have passed between now and last ping")

            if time_passed_in_secs >= 70:
                print(f"calling the destroy session and restart API call for session_id: {session_id}")
                destroy_session_and_restart(session_id)
                time.sleep(3)
            #print("Session last ping info:", session_last_ping_info)
            #print("Time delta between last ping:", date_delta_last_ping)

        if len(all_sessions) == 0:
            print("No active sessions!")
            time.sleep(1)
        time.sleep(3)
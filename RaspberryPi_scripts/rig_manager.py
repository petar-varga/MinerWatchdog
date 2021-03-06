import requests
import json
import datetime
import time

MAX_RETRIES_GET_FIRST_PING = 5

def get_all_currently_performing_sessions():
    url = "http://192.168.31.200:5000/endpoints/all_currently_performing"
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

def destroy_session_and_restart(session_id, pc_identifier):
    url = "http://192.168.31.200:5000/endpoints/end_session"

    payload = {
        "session_id": str(session_id),
        "pc_identifier": pc_identifier
    }
    payload = json.dumps(payload)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)

def active_status_handler(session_id, pc_identifier, date_initiated):
    date_initiated_dt_object = datetime.datetime.strptime(date_initiated, '%Y-%m-%d %H:%M:%S')

    date_delta_has_been_running_for = datetime.datetime.now() - date_initiated_dt_object

    print(f"{session_id} has been running for {str(date_delta_has_been_running_for)}")
    
    retry_counter = 0
    session_last_ping_info = None
    while retry_counter < MAX_RETRIES_GET_FIRST_PING:
        try:
            session_last_ping_info = get_single_active_session_info(session_id)
            break
        except:
            print(f"can't get a ping for session_id: {session_id}")
            retry_counter = retry_counter + 1
    
    if session_last_ping_info == None:
        raise ValueError(f"Can't get ping for session_id {session_id}")

    ping_details = session_last_ping_info["details"]
    ping_time = session_last_ping_info["date_last_pinged"]
    ping_time_dt_object = datetime.datetime.strptime(ping_time, '%Y-%m-%d %H:%M:%S')

    date_delta_last_ping = datetime.datetime.now() - ping_time_dt_object
    time_passed_in_secs = date_delta_last_ping.total_seconds()
    print(f"{time_passed_in_secs} seconds have passed between now and last ping")

    if time_passed_in_secs >= 70:
        print(f"calling the destroy session and restart API call for session_id: {session_id}")
        destroy_session_and_restart(session_id, pc_identifier)
        time.sleep(3)

def warning_status_handler(session_id, pc_identifier, date_initiated):
    """ 
    placeholder empty function
    """
    pass

if __name__ == "__main__":
    while True:
        all_sessions = get_all_currently_performing_sessions()["active_sessions"]
        
        if len(all_sessions) == 0:
            print("No active sessions!")
            time.sleep(5)
            continue

        for session in all_sessions:
            session_id = session["session_id"]
            pc_identifier = session["pc_identifier"]
            session_status = session["status"]
            date_initiated = session["date_initiated"]

            if session_status == "active":
                try:
                    active_status_handler(session_id, pc_identifier, date_initiated)
                except ValueError:
                    print(f"issue with session: {session}")
                    continue
            
            if session_status == "warning":
                warning_status_handler(session_id, pc_identifier, date_initiated)
        
        time.sleep(3)
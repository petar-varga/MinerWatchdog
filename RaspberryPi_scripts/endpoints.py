from os import abort
import threading
import time
from flask import Blueprint, request, Response, jsonify
from flask import json
from flask.globals import session
from flask.helpers import send_from_directory
from flask_restful import abort
import os
from threading import Thread
from utils import (
    db_insert_id, db_read, db_write, db_write_executemany
)
from GPIO_Interface_script import restart

def get_matching_raspberry_pi_pin(pc_identifier):
    response = db_read("""SELECT * FROM `hw_info` 
    WHERE `pc_identifier` LIKE %s""", (pc_identifier, ))

    valid_response = response[0]
    raspberry_pin = int(valid_response["raspberry_pi_pin"])
    return raspberry_pin

endpoints = Blueprint("endpoints", __name__)

@endpoints.route("/create_session", methods=["POST"])
def create_session():
    pc_identifier = request.json["pc_identifier"]
    inserted_id = db_insert_id("""INSERT INTO `session` 
    (`id`, `date_initiated`, `date_ended`, `pc_identifier`, `status`) 
    VALUES (NULL, NOW(), NULL, %s, 'active')""",(pc_identifier,))
    return jsonify({
        "status": inserted_id != None,
        "inserted_id": inserted_id
    })

@endpoints.route("/ping", methods=["POST"])
def ping():
    details = request.json["details"]
    session_id = request.json["session_id"]
    hashrate = request.json["hashrate"]
    temperature = request.json["temperature"]

    if hashrate != "" and temperature != "":
        inserted_id = db_insert_id("""INSERT INTO `ping` 
        (`id`, `session_id`, `hashrate_mhs`, `temperature`, `details`, `date_sent`) 
        VALUES (NULL, %s, %s, %s, %s, NOW())""", (session_id, hashrate, temperature, details))
    else:
        inserted_id = db_insert_id("""INSERT INTO `ping` 
        (`id`, `session_id`, `details`, `date_sent`) 
        VALUES (NULL, %s, %s, NOW())""", (session_id, details))
        
    return jsonify({
        "status": inserted_id != None,
        "inserted_id": inserted_id
    })

@endpoints.route("/end_session", methods=["POST"])
def destroy_session():
    session_id = request.json["session_id"]
    pc_identifier = request.json["pc_identifier"]

    updated = db_write("""UPDATE `session` 
    SET `status` = 'ended',  `date_ended` = NOW() 
    WHERE `session`.`id` = %s""", (session_id, ))

    insert_action_id = db_write("""INSERT INTO `action_log` 
    (`id`, `id_session`, `action_type`, `date_initiated`) 
    VALUES (NULL, %s, 'restart_auto', NOW())""", (session_id, ))

    raspberry_pin = get_matching_raspberry_pi_pin(pc_identifier)

    # start a thread which starts the GPIO interface script
    x = threading.Thread(target=restart, args=(raspberry_pin, ))
    x.start()
    return jsonify({
        "status_session_updated": updated != None,
        "action_executed": insert_action_id != None
    })

@endpoints.route("/check_status", methods=["POST"])
def check_status():
    session_id = request.json["session_id"]

    response_single = db_read("""SELECT * FROM `ping` 
    WHERE `session_id` = %s 
    ORDER BY `ping`.`date_sent` DESC 
    LIMIT 1""", (session_id, ))[0]

    details = response_single["details"]
    date_ping_sent = response_single["date_sent"]

    return jsonify({
        "details": details,
        "date_last_pinged": str(date_ping_sent),
    })

@endpoints.route("/all_currently_performing", methods=["POST"])
def all_currently_performing():
    responses = db_read("""SELECT * FROM `session` 
    WHERE `status` != 'ended'""")

    response_return_object = []
    for response_single in responses:
        pc_identifier = response_single["pc_identifier"]
        session_id = response_single["id"]
        date_initiated = response_single["date_initiated"]
        current_status = response_single["status"]
        response_return_object.append({
            "pc_identifier": pc_identifier,
            "session_id": session_id,
            "date_initiated": str(date_initiated),
            "status": current_status
        })

    return jsonify({
        "active_sessions": response_return_object
    })


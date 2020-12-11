from os import abort
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

    updated = db_write("""UPDATE `session` 
    SET `status` = 'ended',  `status` = NOW() 
    WHERE `session`.`id` = %s""", (session_id, ))

    insert_action_id = db_write("""INSERT INTO `action_log` 
    (`id`, `id_session`, `action_type`, `date_initiated`) 
    VALUES ('', %s, 'restart_auto', NOW())""", (session_id, ))

    # start a thread which starts the GPIO interface script

    return jsonify({
        "status_session_updated": updated != None,
        "action_executed": insert_action_id != None
    })


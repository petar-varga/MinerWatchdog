from os import abort
import time
from flask import Blueprint, request, Response, jsonify
from flask import json
from flask.helpers import send_from_directory
from flask_restful import abort
import os
from threading import Thread
from utils import (
    db_insert_id, db_read, db_write, db_write_executemany
)

endpoints = Blueprint("endpoints", __name__)

@endpoints.route("/sample", methods=["POST"])
def sample():
    return jsonify({
        "test1": "OK",
        "test2": "NOT OK"
    })

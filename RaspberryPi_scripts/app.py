# app.py
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask.json import JSONEncoder
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST
from endpoints import endpoints
from datetime import date

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
from dbconnection import db
app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_HOST"] = MYSQL_HOST
db.init_app(app)

app.register_blueprint(endpoints, url_prefix="/endpoints")

if __name__ == "__main__":
    app.run(port = 5000, debug=False, host="0.0.0.0")
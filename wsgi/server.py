"""
"""

import os
import flask
import redis3
from gevent import pywsgi

APP = flask.Flask("me")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 80))

@APP.route("/")
def index():
    """
    """
    return b"Oh. Hey."

@APP.route("/getFoo")
def getFoo():
    r = redis3.Redis(host="data-svc", port=6379, db=0)
    return r.get("foo")

def main():
    """
    """
    print("launching wsgi server at %s:%u..." % (SERVER_HOST, SERVER_PORT))
    pywsgi.WSGIServer((SERVER_HOST, SERVER_PORT), APP).serve_forever()

if __name__ == "__main__":
    main()

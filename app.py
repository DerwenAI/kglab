#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, render_template, send_from_directory, url_for
from http import HTTPStatus
from pathlib import PurePosixPath
import os
import sys


######################################################################
## app definitions

APP = Flask(__name__, static_folder="site", template_folder="site")

APP.config["DEBUG"] = False
APP.config["MAX_CONTENT_LENGTH"] = 52428800
APP.config["SECRET_KEY"] = "Technically, I remain uncommitted."
APP.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3000


docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

@APP.route("/docs/", methods=["GET"])
@APP.route("/docs/<path:path>", methods=["GET"], defaults={"path": None})
@APP.route("/docs/<path:path>", methods=["GET"])
def static_proxy (path=""):
    #print("suffix", PurePosixPath(path).suffix)

    if path[-3:] not in ["css", ".js", "png"]:
        path = os.path.join(path, "index.html")

    return send_from_directory(docs, path)

#return render_template(path, content=""), HTTPStatus.OK.value


@APP.route("/index.html")
@APP.route("/home/")
@APP.route("/")
def home_redirects ():
    return redirect(url_for("static_proxy"))


######################################################################
## main

def main ():
    PORT = 8000
    APP.run(host="0.0.0.0", port=PORT, debug=True)


if __name__ == "__main__":
    main()

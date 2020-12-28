#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, send_from_directory, url_for
from pathlib import PurePosixPath
import os


APP = Flask(__name__, static_folder="site", template_folder="site")

APP.config["DEBUG"] = False
APP.config["MAX_CONTENT_LENGTH"] = 52428800
APP.config["SECRET_KEY"] = "Technically, I remain uncommitted."
APP.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3000


@APP.route("/docs/", methods=["GET"])
@APP.route("/docs/<path:path>", methods=["GET"], defaults={"path": None})
@APP.route("/docs/<path:path>", methods=["GET"])
def static_proxy (path=""):
    if not path:
        suffix = ""
    else:
        suffix = PurePosixPath(path).suffix

    if suffix not in [".css", ".js", ".png"]:
        path = os.path.join(path, "index.html")

    return send_from_directory(APP.static_folder, path)


@APP.route("/index.html")
@APP.route("/home/")
@APP.route("/")
def home_redirects ():
    return redirect(url_for("static_proxy"))


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8000, debug=True)

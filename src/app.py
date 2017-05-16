#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from tlf import blu_tlf
from database import *

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('SERRA_SETTINGS', silent=True)
app.secret_key = os.environ["SESSION_SECRET_KEY"]
app.register_blueprint(blu_tlf, url_prefix='/tlf')

@app.route('/', methods = ["GET"])
def main():
    return render_template('main.html', title = "Buscador")

if __name__ == "__main__":
    app.debug = os.environ['DEBUG']
    app.run('0.0.0.0', port=80, threaded=True)


from flask import Flask

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('SERRA_SETTINGS', silent=True)
app.secret_key = os.environ["SESSION_SECRET_KEY"]

@app.route('/', methods = ["GET"])
def main():
    return "Hello Sallent"

if __name__ == "__main__":
    app.run('0.0.0.0', port=80, threaded=True)


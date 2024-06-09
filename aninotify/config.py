from dotenv import load_dotenv

import os

load_dotenv()

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_USERID = os.environ.get("TG_USERID")



TIME_REQUEST = 10

URL_JSON = "aninotify/tasks.json"


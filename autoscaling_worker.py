from apscheduler.schedulers.blocking import BlockingScheduler
from uniandes.cloud.aws.SQS import SQS

import requests
import base64
import json
import os

sched = BlockingScheduler()
app = "smarthtool"
process = "worker"

sqs = SQS()

min_num_worker = int(os.environ.get("worker_min",0))
max_num_worker = int(os.environ.get("worker_max",5))

# Generate Base64 encoded API Key
BASEKEY = base64.b64encode(":" + os.environ["heroku_api_key"])
# Create headers for API call
HEADERS = {
    "Accept": "application/vnd.heroku+json; version=3",
    "Authorization": BASEKEY
}

def get_current_dyno_quantity():
    url = "https://api.heroku.com/apps/" + app + "/formation"
    try:
        result = requests.get(url, headers=HEADERS)
        for formation in json.loads(result.text):
            if formation["type"] == "worker":
                current_quantity = formation["quantity"]
                return int(current_quantity)
    except:
        return None


def scale(size):
    payload = {'quantity': size}
    json_payload = json.dumps(payload)
    url = "https://api.heroku.com/apps/" + app + "/formation/" + process
    try:
        result = requests.patch(url, headers=HEADERS, data=json_payload)
        if result.status_code == 200:
            print "Success!"
        else:
            print "Failure"
    except:
        print "Exception!"


@sched.scheduled_job('interval', minutes=int(os.environ.get("worker_scaling_time",1)))
def job():
    print "See Worker Autoscaling"
    message_number = sqs.get_message_number()
    print message_number
    dyno_number = get_current_dyno_quantity()
    print dyno_number
    if dyno_number is not None:
        if message_number == 0:
            print "Message equal 0"
            if dyno_number > 0:
                print "Decreasing to 0"
                scale(min_num_worker)
        elif message_number > 0 and message_number < int(os.environ.get("worker_message",100)):
            print "Message in range"
            if dyno_number - 1 >= min_num_worker:
                print "Decreasing in 1"
                scale(dyno_number - 1)
            elif dyno_number == 0:
                print "Increasing in 1 from 0"
                scale(1)
        else:
            if dyno_number+1 <= max_num_worker:
                print "Aumenting in 1"
                scale(dyno_number+1)
    else:
        print "Returning None"

sched.start()
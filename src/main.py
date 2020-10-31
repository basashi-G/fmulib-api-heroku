from flask import Flask, jsonify
import datetime
from time import sleep
from models import Calender
from scheduler import scheduler
import logging

WAIT_TIME = 20

# logger
logger = logging.getLogger("root").getChild(__name__)
logger.debug("start main.py")


# make cal and set job
calender = Calender()


def job():
    calender.fetch_from_network()
    sleep(60 * WAIT_TIME)


scheduler(job)


app = Flask(__name__)


@app.route("/")
def root():
    return "This server is for API of FMU library."


@app.route("/today")
def return_today_time():
    logger.info("/today is called.")
    date = datetime.date.today()
    result = calender.check(date)
    json = {
        "status": result[0],
        "when": "today",
        "opentime": result[1],
    }
    return jsonify(json)


@app.route("/tomorrow")
def return_tomorrow_time():
    logger.info("/tomorrow is called.")
    date = datetime.date.today() + datetime.timedelta(days=1)
    result = calender.check(date)
    json = {
        "status": result[0],
        "when": "tomorrow",
        "opentime": result[1],
    }
    return jsonify(json)


@app.route("/<year>/<month>/<day>")
def return_specified_time(year, month, day):
    logger.info("specified is called.")
    try:
        date = datetime.date(year=int(year), month=int(month), day=int(day))
    except ValueError:
        return "invalid parameter", 400

    result = calender.check(date)
    json = {
        "status": result[0],
        "when": {"year": year, "month": month, "day": day},
        "opentime": result[1],
    }
    return jsonify(json)


if __name__ == "__main__":
    print("flask")
    # app.env = 'development'
    app.run()
else:
    print("uwsgi")

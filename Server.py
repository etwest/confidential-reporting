#!/usr/bin/python3

# variables which need to be changed for different administrators
toaddrs  = 'protonmail addresses'

# for reCAPTCHA v3
site_key = "copy site key here"

secret_key = "copy secret key here"

# The public key for the protonmail account
pubKey = '''Copy public key here within the quotations'''

# The plaintext of this password is stored right here
# so we will need to make sure that we never send anything sensitive via 
# intermediary that isn't encrypted

username = 'copy intermediary email address here'
password = 'copy app password for email address here'

from flask import (
  Flask, make_response, jsonify, render_template
)
from flask import request as flask_request
from flask_talisman import Talisman
import requests
import os
import json
import sys
import smtplib
import datetime

# Some constants for use later
MAX_SIZE = 25000
HTTP_SUCCESS = 200
HTTP_PRECONDITION_FAILED = 412
HTTP_TOO_LARGE = 413
SMTP_PORT = 465

# create the log directory if it doesn't exist yet
exists = os.path.isdir("logs")
if not exists:
  os.mkdir("logs")

# get the process ID of this process
pid = os.getpid()

# write a message to a log file, log files are broken up by pid and date
def logToFile(message):
  time = datetime.date.today()
  with open("logs/"+str(time.year)+"."+str(time.month)+"."+str(time.day)+":"+str(pid), "w+") as logfile:
    logfile.write(message)

SELF = "'self'"

app = Flask(__name__)

# Content Security Policy to prevent the execution of scripts we don't trust
CSP = {
'default-src': [
    SELF,
    'maxcdn.bootstrapcdn.com',
    'fonts.gstatic.com',
    'www.google.com',
  ],
  'img-src': SELF,
  'script-src': [
    SELF,
    'ajax.googleapis.com',
    'www.google.com',
    'code.jquery.com',
    'www.gstatic.com',
    'maxcdn.bootstrapcdn.com',
  ],
  'style-src': [
    SELF,
    'fonts.googleapis.com',
    'maxcdn.bootstrapcdn.com',
  ],
}

talisman = Talisman(app, 
  content_security_policy = CSP,
  content_security_policy_nonce_in = ['script-src'],
  feature_policy={
    'geolocation': '\'none\'',
  })

#########################################
# create error handler for invalid reports
#########################################
class InvalidReport(Exception):
  status_code = 400

  def __init__(self, message, status_code=None, payload=None):
    Exception.__init__(self)
    self.message = message
    if status_code is not None:
      self.status_code = status_code
    self.payload = payload

  def to_dict(self):
    rv = dict(self.payload or ())
    rv['message'] = self.message
    return rv

@app.errorhandler(InvalidReport)
def handle_invalid_report(error):
  response = make_response(jsonify(error.to_dict()))
  response.status_code = error.status_code
  return response

#########################################
# route for submitting reports
#########################################
@app.route("/report", methods=['PUT'])
def insert():
  time = datetime.datetime.now()
  
  # limit the size of the report field
  if len(flask_request.form["report"]) > MAX_SIZE:
    print(str(time) + ": length of report is way to long. We're dropping it to protect ourselves")
    raise InvalidReport("length of report was too long", HTTP_TOO_LARGE)

  # Code for the recaptcha
  response = requests.post('https://www.google.com/recaptcha/api/siteverify',
    data={'secret':secret_key, 'response':flask_request.form["token"]})
  recaptcha_check = response.json()

  if recaptcha_check['success'] == False:
    print(str(time) + ": Failed recaptcha success, dropping report")
    raise InvalidReport("failed recaptcha success", HTTP_PRECONDITION_FAILED)
  elif recaptcha_check["score"] <= 0.6:
    print(str(time) + ": Failed recaptcha with score of " + str(recaptcha_check["score"]) + ", dropping report")
    raise InvalidReport("failed recaptcha score", HTTP_PRECONDITION_FAILED)

  # Code for sending the email
  # TODO: make subjects sequential

  server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', SMTP_PORT)
  server_ssl.ehlo()

  server_ssl.login(username,password)
  subject = 'Report'

  msg = "\r\n".join([
    "From: "+username,
    "To: "+toaddrs,
    "Subject:"+subject,
    "",
    flask_request.form["report"]
    ])
  server_ssl.sendmail(username, toaddrs, msg)
  server_ssl.quit()
  return json.dumps(True)

#########################################
# routes for html files
#########################################
@app.route("/", methods=["GET"])
def main_page():
  return render_template('home.html', site_key=site_key)

@app.route("/resources", methods=["GET"])
def resource_page():
  return render_template('resources.html', site_key=site_key)

@app.route("/privacy", methods=['GET'])
def privacy_page():
  return render_template('privacy.html', site_key=site_key)

@app.route("/report", methods=['GET'])
def report_page():
  return render_template('report.html', site_key=site_key, pubKey=pubKey)
  
#########################################
# Route to return raw public key
#########################################
@app.route("/key", methods=['GET'])
def get_pubKey():
  response = make_response(pubKey, HTTP_SUCCESS)
  response.headers['Content-Type'] = 'text/plain'
  return response

# ONLY for testing, uses self signed certificates and doesn't do 
# redirection to https
if __name__ == "__main__":
	app.run(host="localhost", threaded=True, ssl_context=('certs/cert.pem', 'certs/key.pem'))

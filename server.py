#!/usr/bin/python3
# WikiBOT

from flask import Flask, request, jsonify
import requests
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.SID = os.environ.get('SID')
app.KEY = os.environ.get('KEY')
client = Client(app.SID,app.KEY)

def welcome_user(lang='es'):
  """
  Welcomes the user
  """
  WELCOME_MESSAGE = {
  'es': 'Hola! Soy un bot que consulta Wikipedia. Para usarme escribime aglo y te respondo con el artículo! 👉 '
  'en': "Hello! i'm a bot that searches Wikipedia. To use me, ask me "}


@app.route("/")
def hello():
  return "Para usar el bot:  Manda wassap a +1 415 523 8886 with code join yet-door.!"

@app.route("/incoming", methods=["POST"])
def incomming():
#  url = request.url
#  body = {'Body':'Dijiste {0}'.format(request.form['Body'])}
#  print(r.text
#  print(dir(request))
#  print(request.url)
#  print(request.form)
#  print(request.form['Body'])
  resp = MessagingResponse()
  resp.message("Hola! venis de {0} y lo que escribiste es {1}".format(request.url,request.form['Body']))
  return str(resp)


if __name__ == "__main__":
  app.run()

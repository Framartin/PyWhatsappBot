#!/usr/bin/python3
# WikiBOT
VERSION="0.1.1toolforge"

from flask import Flask, request, jsonify
import requests
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import yaml

app = Flask(__name__)
#Changes for toolfoger
__dir__ = os.path.dirname(__file__)

app.config.update(
    yaml.safe_load(open(os.path.join(__dir__, 'config.yaml'))))

app.SID = app.config['SID']
app.KEY = app.config['KEY']
#app.SID = os.environ.get('SID')
#app.KEY = os.environ.get('KEY')
client = Client(app.SID,app.KEY)
#test

def welcome_user(lang='es'):
  """
  Welcomes the user
  """
  WELCOME_MESSAGE = {
  'es': 'Hola! Soy un bot que consulta Wikipedia. Para usarme escribime aglo y te respondo con el artículo! Si estabas buscando ayuda en wikipedia 👉 https://es.wikipedia.org/wiki/Ayuda O https://es.wikipedia.org/wiki/Ayuda:Contenidos ',
  'en': "Hello! i'm a bot that searchs Wikipedia. To use me, write to me something that you want to look for in Wikipedia and i shall give it to you! :D. If you were looking for help on Wikipedia: https://en.wikipedia.org/wiki/Help"
  }
  return WELCOME_MESSAGE[lang]

def body_process(cuerpo):
  """
  Tries to understand the body of the message. Dummy function for now but thinking about parsing 'lang,words_to_search' on the bot so the user can specify babel site
  And maybe project? like wikidata,Racing Club
  """
  pass


def wikipedia_lookup(lookup, lang='es'):
  """
  Lookups on wikipedia using the api
  https://es.wikipedia.org/w/api.php?action=help&modules=main
  """
  SITE='https://{0}.wikipedia.org/'.format(lang) #Sitio de donde usar la API. lang es el lenguaje de la wiki
  EXCHARS=200 #limite de chars en la desc, muy largo y wassap no me deja
  LOOKUP='{0}'.format(lookup).replace(' ','%20') #Reemplazo whitespace por %20 Para las cosas que tienen espacio en el nombre
  WIKIPEDIA_API_LOOKUP="w/api.php?action=query&prop=extracts&exintro&exchars={1}&explaintext&titles={0}&format=json".format(LOOKUP,EXCHARS) #La api en cuestion. ver paramentros en la doc
  #r = requests.get('https://es.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles=Albert%20Einstein&format=json')
  r = requests.get('{0}{1}'.format(SITE,WIKIPEDIA_API_LOOKUP)) #hago el POST
  if r.status_code != 200:
    print('Connection lost with Wikipedia API!: Return code: {0}'.format(r.status_code))
    return 'Connection lost with Wikipedia API!: Return code: {0}'.format(r.status_code)
  resultado = r.json() #paso a json el POST
  print(resultado) #console.log
  try:
    pageid=list(resultado['query']['pages'].values())[0]['pageid'] #consigo el pageid
  except KeyError: #Si no se encuentra la busqueda, pageid no existe en la colección que devuelve la API
    print('KeyError!')
    URL='https://es.wikipedia.org/w/index.php?title={0}&action=edit&redlink=1'.format(LOOKUP.replace('%20','_'))
    MENSAJE = {
    'es':'🤔 \nNo pude encontrar lo que buscaste...\n¿Está bien escrito?\nSi lo está, ¿por qué no pruebas creando el artículo? :)\n {0}'.format(URL),
    'en':"🤔 \nCan't seem to find the thing you are looking for...Check spelling?\nAlso, if it's right, why not create the article? :D\n {0}".format(URL)
    }
    print(MENSAJE[lang])
    return MENSAJE[lang] #devuelvo el mensaje para escribir de vuelta

  extract = resultado['query']['pages'][str(pageid)]['extract'] #consigo el "extracto" del arti
  title = resultado['query']['pages'][str(pageid)]['title'] #consigo el título
  curid='?curid={0}'.format(pageid) #consigo el id de la pagina
  url='{0}{1}'.format(SITE,curid) #construyo la URL del arti usando el curid
  MENSAJE = {
  'es':'*{0}*\n{1}\nMás info acá: {2}'.format(title,extract,url), 
  'en':'*{0}*\n{1}\nMore info here: {2}'.format(title, extract,url)  
  } #el mensaje que se construye. Se podrian agregar más idiomas o modificar desde acá
  print(MENSAJE[lang])
  return MENSAJE[lang] #devuelvo el mensaje para escribir de vuelta
  
  
  
  
  

@app.route("/")
def hello():
  return "Para usar el bot:  Manda wassap a +1 415 523 8886 with code join yet-door.!"

@app.route("/incoming", methods=["POST"])
def incoming():
  cuerpo = request.form['Body']
  resp = MessagingResponse()
  if 'ayuda' in cuerpo.lower():
    resp.message(welcome_user('es'))
  elif 'help' in cuerpo.lower():
    resp.message(welcome_user('en'))
  else:
    resp.message(wikipedia_lookup(cuerpo, lang='es'))
  return str(resp)


if __name__ == "__main__":
  app.run()

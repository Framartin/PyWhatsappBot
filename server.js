var express = require('express');
var app = express();
var request = require('request');
const bodyParser = require('body-parser');


const accountSid = process.env.SID;
const authToken = process.env.KEY;
const client = require('twilio')(accountSid, authToken);
const MessagingResponse = require('twilio').twiml.MessagingResponse;

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: false }));



app.post('/incoming', (req, res) => {
  const twiml = new MessagingResponse();
  console.log(req.body)
  if(req.body.Body.toLowerCase().trim()!="hi" && req.body.Body.toLowerCase().trim()!="hello" && req.body.Body.toLowerCase().trim()!="test" && req.body.Body.toLowerCase().trim()!="help"){
  request('https://api.duckduckgo.com/?skip_disambig=1&format=json&pretty=1&q='+req.body.Body, function (error, response, body) {
    body = JSON.parse(body)
    console.log('body:', body["Abstract"]);
    
    if(body["Abstract"] == ""){
	    body["Abstract"]= body["RelatedTopics"][0]["Text"]
	  }
    
    var msg = twiml.message("Esto es lo que encontré sobre " + `*`+body["Heading"]+`*` +`
    `+ body["Abstract"] + " La url del arti: " + body["AbstractURL"]);
  res.writeHead(200, {'Content-Type': 'text/xml'});
  res.end(twiml.toString());
  });
  }
  else{
    var msg = twiml.message(`*HOLA! 👋*
Soy un bot hecho en node al que le gusta el death metal y wikipedia.

Probamos? mandame cualquier cosa y veo que te devuelvo`)
    res.writeHead(200, {'Content-Type': 'text/xml'});
  res.end(twiml.toString());
  }
  
});

app.post('/check', function(req, res) {
  console.log(req.body.Body)
});
app.get('/', function(request, response) {
  response.sendFile(__dirname + '/views/index.html');
});


var listener = app.listen(process.env.PORT, function() {
  console.log('Your app is listening on port ' + listener.address().port);
});

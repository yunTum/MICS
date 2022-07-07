var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

const { database, createtable} = require('./public/model/db-querys');
const aedes = require('aedes')()
const server = require('net').createServer(aedes.handle)

var app = express();

// Database connect
database().connect((err) => {
    if (err) throw err;
    console.log('Connected');

    try {
      createtable();
    } catch (e) {
      console.error(e);
    }
    
});
//database().useDatabase('iot')

// view engine setup
app.set('port', process.env.PORT || 1883);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

//Register Data to MySQL
const insert_data = (payload) => {
  var sql = 'INSERT INTO data VALUES (?, ?, ?, ?, ?, ?);'
  var palams = [
    null,
    payload.interested, 
    payload.age, 
    payload.gender, 
    payload.start_time, 
    payload.end_time
  ]
  //Throw query and Save data
  database().query(sql, palams, function(error, response){
    if(error) throw error;
    console.log(response);
  })
  database().end();
}

//////////MQTT setting
// MQTT Broker
server.listen(app.get('port'), function () {
	console.log('server listening on port', app.get('port'))
})

// Client Eroor
aedes.on('clientError', function (client, err) {
	console.log('client error', client.id, err.message, err.stack)
})

// Connected Error
aedes.on('connectionError', function (client, err) {
	console.log('client error', client, err.message, err.stack)
})

// New Subscriber Connect
aedes.on('subscribe', function (subscriptions, client) {
	if (client) {
		console.log('subscribe from client', subscriptions, client.id)
	}
})

// New Client Connect
aedes.on('client', function (client) {
	console.log('new client', client.id)
})

var text_decoder = new TextDecoder("utf-8");

// Publisher Connect
// Recieve data
aedes.on('publish', function (packet, client) {
	if (client) {
		console.log('message from client', client.id)
    //Payload: binary -> utf-8
    var payload = text_decoder.decode(Uint8Array.from(packet.payload).buffer)
    payload = JSON.parse(payload)
    insert_data(payload)
	}
})
///////////////

module.exports = app;

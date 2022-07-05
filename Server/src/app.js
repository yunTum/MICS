var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

const aedes = require('aedes')()
const server = require('net').createServer(aedes.handle)
const mysql = require('mysql');

// DBに接続する設定情報
const con = mysql.createConnection({
    host: 'mysql',
    user: 'nonodebri',
    password: 'NoNou22',
    database: 'iot'
});

var app = express();

con.connect((err) => {
    if (err) throw err;
    console.log('Connected');
});

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

// クライアントエラーの場合
aedes.on('clientError', function (client, err) {
	console.log('client error', client.id, err.message, err.stack)
})

// 接続エラーの場合
aedes.on('connectionError', function (client, err) {
	console.log('client error', client, err.message, err.stack)
})

// publishされた場合
aedes.on('publish', function (packet, client) {
	if (client) {
		console.log('message from client', client.id)
	}
})

// 新しいsubscriberが接続した場合
aedes.on('subscribe', function (subscriptions, client) {
	if (client) {
		console.log('subscribe from client', subscriptions, client.id)
	}
})

// 新しいクライアントが接続した場合
aedes.on('client', function (client) {
	console.log('new client', client.id)
})

// MQTTブローカー起動
server.listen(app.get('port'), function () {
	console.log('server listening on port', app.get('port'))
})

module.exports = app;

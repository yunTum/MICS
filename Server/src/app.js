var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var http = require("http")
const { insert_data} = require('./public/model/db-querys');
var WebSocketServer = require("ws").Server
var app = express();

// view engine setup
app.set('port', process.env.PORT || 3000);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

var indexRouter = require('./routes/index');
app.use('/', indexRouter);

var timeDataRouter = require('./routes/timedata');
app.use('/camera-data', timeDataRouter);

var createTableRouter = require('./routes/createTable');
app.use('/create-dataTable', createTableRouter);

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
  res.on('error',function(err) {
    console.log("something wrong");
});
});

const port = app.get('port')
//web server
var server = http.createServer(app)
server.listen(port)

console.log("http server listening on %d", port)

//////////WebSocket setting
var wss = new WebSocketServer({server: server})
console.log("websocket server created")

wss.on("connection", function(ws) {
  console.log("websocket connection open")

  ws.on('message',(data)=>{
    data_json = JSON.parse(data)
    console.log("recieved");
    console.log(data_json);
    insert_data(data_json)
  });

  ws.on("close", function() {
    console.log("websocket connection close")
  })
})

module.exports = app;

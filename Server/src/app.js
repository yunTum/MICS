var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var http = require("http")
const { database, createtable, handleDisconnect} = require('./public/model/db-querys');
var WebSocketServer = require("ws").Server
var app = express();

// Database connect
database().connect((err) => {
    if (err) throw err;
    console.log('Connected');

    try {
      createtable();
      console.log('Created');
    } catch (e) {
      console.error(e);
      console.log('Create Error');
    }
    
});

handleDisconnect(); 


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

var homeRouter = require('./routes/home');
app.use('/home', homeRouter);

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
    insert_data(data_json)
  });

  ws.on("close", function() {
    console.log("websocket connection close")
  })
})


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

module.exports = app;

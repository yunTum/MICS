// Write Qurey
const mysql = require('mysql');
const { response } = require('../../app');

// DB Setting
const database = () => {
    const con = mysql.createPool({
        host: 'us-cdbr-east-06.cleardb.net',
        user: 'bd4dceab87de57',
        password: '33f46b06',
        port : 3306,
        database: 'heroku_10ab3b9d2993672'
    });
    return con
};
//Enter into MySQL
//mysql -u [user] -p
//[password]


//Create DB table in iot
const createtable = () => {
    var sql = "CREATE TABLE data (\
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',\
        interested INTEGER NOT NULL COMMENT '関心度',\
        age INTEGER NOT NULL COMMENT '年齢',\
        gender INTEGER NOT NULL COMMENT '性別',\
        start_time datetime NOT NULL COMMENT '測定開始時間',\
        end_time datetime NOT NULL COMMENT '測定終了時間',\
        end_time_unix INTEGER NOT NULL COMMENT '測定終了UNIX時間'\
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

      database().getConnection((error, connection) => {
        var result = connection.query(sql, (error, response) => {
          if(error) throw error;
          connection.destroy();
          return response;
      })
      return result;
    })
}

//not use
const existtable = () => {
    var sql = "SELECT 1 FROM data LIMIT 1;"

      database().query(sql, function(error, response){
        if(error) throw error;
        console.log(response);
      })
}

const get_data = () => {
  var sql = 'SELECT * FROM data;'
  database().getConnection((error, connection) => {

    var result = connection.query(sql, (error, response) => {
      if(error) throw error;
      console.log(response);
      connection.destroy();
      return response;
    })
    return result;
  })
}

// const get_reqdata = (start_time, end_time) => {
//   var sql = 'SELECT * FROM data WHERE end_time BETWEEN ' + start_time + ' AND ' + end_time + ';'
//   database().getConnection((error, connection) => {
//   var result = connection.query(sql, (error, response) => {
//     if(error) throw error;
//     console.log(response);
//     connection.release();
//     return response;
//   })
//   return result
// })
// }

const PyTime2JascTime = (Pytime) => {
  //payload.~_time : YYYYMMDDhhmmss
  const year = parseInt(Pytime.substring(0, 4));
  const month = parseInt(Pytime.substring(4, 6));
  const day = parseInt(Pytime.substring(6, 8));
  const hour = parseInt(Pytime.substring(8, 10));
  const min = parseInt(Pytime.substring(10, 12));
  // YYYYMMDDHHMMSS -> YYYY-MM-DD hh:mm:ss        
  const date = new Date(year, month - 1, day, hour, min);
  return date
}

const convertDatetimeFromUnixtime = (UnixTime) => {
  
  const date = new Date(UnixTime)
  let format = "yyyy-MM-dd hh:mm:ss"
  
  const year = date.getFullYear()
  const month = zeroPadding(date.getMonth()+1)
  const day = zeroPadding(date.getDate())
  const hour = zeroPadding(date.getHours())
  const minutes = zeroPadding(date.getMinutes())
  const seconds = zeroPadding(date.getSeconds())
  
  return format
  .replace("yyyy", year)
  .replace("MM", month)
  .replace("dd", day)
  .replace("hh", hour)
  .replace("mm", minutes)
  .replace("ss", seconds)
  
  function zeroPadding(value) {
      return ("0" + value).slice(-2);
  }
}

//Register Data to MySQL
const insert_data = (payload) => {
  var start_time = PyTime2JascTime(payload.start_time)
  var end_time = PyTime2JascTime(payload.end_time)
  
  // Unix time
  var end_time_unix = Date.parse(end_time)/1000
  var sql = 'INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?);'
  var palams = [
    null,
    payload.interested, 
    payload.age, 
    payload.gender, 
    start_time, 
    end_time,
    end_time_unix
  ]
  //Throw query and Save data
  database().getConnection((error, connection) => {
    var result = connection.query(sql, palams, (error, response) => {
    if(error) throw error;
    connection.destroy();
    return response
  })
  return result;
})
}

exports.convertDatetimeFromUnixtime = convertDatetimeFromUnixtime;
exports.insert_data = insert_data;
exports.database = database;
exports.createtable = createtable;
exports.existtable = existtable;
exports.get_data = get_data;
// exports.get_reqdata = get_reqdata;
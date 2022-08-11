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
        end_time datetime NOT NULL COMMENT '測定終了時間'\
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

      database().getConnection((error, connection) => {
        var result = connection.query(sql, (error, response) => {
          if(error) throw error;
          return response;
      })
      connection.release();
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
      return response;
    })
    connection.release();
    return result;
  })
}

const get_reqdata = (start_time, end_time) => {
  var sql = 'SELECT * FROM data WHERE end_time BETWEEN ' + start_time + ' AND ' + end_time + ';'
  database().getConnection((error, connection) => {
  var result = connection.query(sql, (error, response) => {
    if(error) throw error;
    console.log(response);
    return response;
  })
  connection.release();
  return result
})
}

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
  database().getConnection((error, connection) => {
    var result = connection.query(sql, palams, (error, response) => {
    if(error) throw error;
    return response
  })
  connection.release();
  return result;
})
}

exports.insert_data = insert_data;
exports.database = database;
exports.createtable = createtable;
exports.existtable = existtable;
exports.get_data = get_data;
exports.get_reqdata = get_reqdata;
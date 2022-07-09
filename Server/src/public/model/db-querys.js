// Write Qurey
const mysql = require('mysql');

// DB Setting
const database = () => {
    const con = mysql.createConnection({
        host: 'us-cdbr-east-06.cleardb.net',
        user: 'bd4dceab87de57',
        password: '33f46b06',
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

      database().query(sql, function(error, response){
        //if(error) throw error;
        //console.log(response);
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

exports.database = database;
exports.createtable = createtable;
exports.existtable = existtable;
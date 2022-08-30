var express = require('express');
var router = express.Router();
const cors = require('cors')
const { database, convertDatetimeFromUnixtime } = require('../public/model/db-querys');


router.get('/', cors(), function(req, res, next) {
    const reqdata = req.query
    const end_time = convertDatetimeFromUnixtime(reqdata.end_time*1000)
    const start_time = convertDatetimeFromUnixtime(reqdata.start_time*1000)

    // レスポンスが先の処理で来てしまい、DB接続が後なので、同じコード内にSQL記述
    var sql = 'SELECT * FROM data WHERE end_time BETWEEN ' + ' " ' + start_time + ' " ' + ' AND ' + ' " ' +  end_time + ' " ' +  ';'
    database().getConnection((error, connection) => {
    connection.query(sql, (error, response) => {
      if(error) throw error;
      sql_data = JSON.stringify(response)
      console.log('Response Data Length: ' + Object.keys(JSON.parse(sql_data)).length + ' items')  ;
      connection.destroy();
      res.json( sql_data );
    })
  })
    
});

module.exports = router;
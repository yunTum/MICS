var express = require('express');
var router = express.Router();
const cors = require('cors')
const { database } = require('../public/model/db-querys');


router.get('/', cors(), function(req, res, next) {
    const reqdata = req.query
    const end_time = reqdata.end_time
    const start_time = reqdata.start_time

    // レスポンスが先の処理で来てしまい、DB接続が後なので、同じコード内にSQL記述
    var sql = 'SELECT * FROM data WHERE end_time BETWEEN ' + start_time + ' AND ' + end_time + ';'
    database().getConnection((error, connection) => {
    connection.query(sql, (error, response) => {
      if(error) throw error;
      console.log(response);
      connection.destroy();
      res.json( JSON.stringify(response) );
    })
  })
    
});

module.exports = router;
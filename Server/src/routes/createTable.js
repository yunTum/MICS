var express = require('express');
var router = express.Router();
const cors = require('cors')
const { createtable } = require('../public/model/db-querys');

// DB上にテーブルが作成されていない場合、新規作成
// request
//     createBool:true

router.get('/', cors(), function(req, res, next) {
    const reqdata = req.query
    const createBoolflg = reqdata.createBool

    if (createBoolflg){
        res.send(createtable())
    }
    
});

module.exports = router;
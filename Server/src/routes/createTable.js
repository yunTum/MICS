var express = require('express');
var router = express.Router();
const cors = require('cors')
const { createtable } = require('../public/model/db-querys');

router.get('/', cors(), function(req, res, next) {
    const reqdata = req.query
    const createBoolflg = reqdata.createBool

    if (createBoolflg){
        res.send(createtable())
    }
    
});

module.exports = router;
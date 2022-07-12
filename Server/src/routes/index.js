var express = require('express');
var router = express.Router();
const { get_data } = require('../public/model/db-querys');

/* GET home page. */
router.get('/iot-data', function(req, res, next) {
  var value = get_data()[0]
  res.render('output', { title: 'Express', data: value });
});

module.exports = router;

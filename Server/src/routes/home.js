var express = require('express');
var router = express.Router();
const cors = require('cors')

router.get('/', cors(), function(req, res, next) {
  res.render('index', { title: 'HOME' });
  res.send('Hello World')
  res.json({'message': 'Hello World'})
});

module.exports = router;
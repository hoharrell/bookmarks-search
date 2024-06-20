const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const mysql = require('mysql');
const books = require('./database');

const connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '******', // change
  database : 'book_marks'
});

connection.connect();

const port = process.env.PORT || 8080;

const app = express()
  .use(cors())
  .use(bodyParser.json())
  .use(books(connection));

app.listen(port, () => {
  console.log(`Express server listening on port ${port}`);
});
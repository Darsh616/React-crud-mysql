const express = require("express");
const morgan = require("morgan");
const mysql = require("mysql");
const myConnection = require("express-myconnection");
const path = require('path');
const app = express();
require('dotenv').config();

// To get the database password from the .env file
const PASS = process.env.DATABASE_PASSWORD;

// Importing routes
const customerRoutes = require('./routes/customer');

// settings
app.set('port', process.env.PORT || 3000);
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// middlewares
app.use(morgan('dev'));
app.use(myConnection(mysql, {
    host:'host.docker.internal',// host:  'localhost' || '127.0.0.1'||'host.docker.internal',localhost
    user: 'root',   
    password: 'newpassword',
    port: '3306',
    database: 'crudnodejsmysql'
}, 'single'));
app.use(express.urlencoded({extended: false}));

// Routes
app.use('/', customerRoutes);

// Static files
app.use(express.static(path.join(__dirname, 'public')));

// Starting the server
app.listen(app.get('port'), () => {
    console.log('Server on port 3000');
require('dotenv').config();  // This loads the variables from the .env file

const PASS = process.env.DATABASE_PASSWORD || '';  // Read the password from the .env file, default to an empty string if not set

})

/**
 * Module dependencies.
 */

var express = require('express');
var routes = require('./routes');
var user = require('./models/user');
var http = require('http');
var path = require('path');

var MongoStore = require('connect-mongodb');
var settings = require('./settings');

var app = express();

// all environments
// can't change the orders???
app.set('port', process.env.PORT || 3000);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(express.cookieParser());

app.use(express.session({
    secret: settings.cookiesSecret,
    Store: new MongoStore({
        db: settings.db
    })
}));


app.use(function(req, res, next){
	res.locals.user = req.session.user;
	var err = req.session.error;
	if (err && err.length) {
		res.locals.error = err;
        //console.log(res.locals.error);
    } else
		res.locals.error = null;

	var succ = req.session.success;
	if (succ && succ.length) {
		res.locals.success = succ;
        //console.log(res.locals.success);
    } else
		res.locals.success = null;
	next();
});


app.use(app.router);
//app.use(express.router(routes));
app.use(express.static(path.join(__dirname, 'public')));


routes(app);

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});

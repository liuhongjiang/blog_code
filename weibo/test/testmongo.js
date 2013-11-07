var settings = require('../settings')
var Db = require('mongodb').Db
var Connection = require('mongodb').Connection
var Server = require('mongodb').Server
console.log(settings.host)
console.log(Connection.DEFAULT_PORT)

var mongodb = new Db(settings.db, new Server(settings.host, Connection.DEFAULT_PORT, {}));

mongodb.open(function (err, db) {
    if (err) {
        console.log(err);
    }

    db.collection('users', function(err, collection) {
        if (err) {
            mongodb.close();
            return console.log(err);
        };

        collection.findOne({name:'aaa'}, function(err, doc) {
            mongodb.close();
            if (doc) {
                console.log(doc);
            } else {
                console.log(err);
            }
        });
    });
});

/*
 * GET users listing.
 */

var mongodb = require('../models/db')

function User(user) {
    this.name = user.name;
    this.password = user.password;
};
module.exports = User;

User.prototype.save = function save(cb) {
    var user = {
        name: this.name,
        password: this.password.toString(),
    };
    mongodb.open(function(err, db) {
        if (err) {
            return cb(err);
        }

        db.collection('users',function(err, collection){
            if (err) {
                mongodb.close();
                return cb(err);
            }
            collection.ensureIndex('name', {unique:true});

            collection.insert(user, {safe:true}, function(err, user) {
                mongodb.close();
                cb(err, user);
            });
        });
    });
};

User.get = function get(username, cb) {
    //console.log(mongodb);
    mongodb.open(function (err, db) {
        if (err) {
            return cb(err);
        }

        //console.log(username);

        db.collection('users', function(err, collection) {
            if (err) {
                mongodb.close();
                return cb(err);
            };

            collection.findOne({name:username}, function(err, doc) {
                mongodb.close();
                if (doc) {
                    //console.log("lhj")
                    //console.dir(doc)
                    var user = new User(doc);
                    //console.log('find the user');
                    //console.log(user);
                    cb(err, user);
                } else {
                    cb(err, null);
                }
            });
        });
    });
};

exports.list = function(req, res){
  res.send("respond with a resource");
};

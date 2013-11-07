
/*
 * GET home page.
 */

var crypto = require('crypto')

var User = require('../models/user');
var Post = require('../models/post')

//exports.index = function(req, res){
//  res.render('index', { title: 'Express' });
//};
//
//exports.user = function(req, res){
//};
//
//exports.post = function(req, res){
//};
//
//exports.reg = function(req, res){
//};
//
//exports.doReg = function(req, res){
//};
//
//exports.login = function(req, res){
//};
//
//exports.doLogin = function(req, res){
//};
//
//exports.logout = function(req, res){
//};

module.exports = function(app) {
    app.get('/', function(req, res) {
        Post.get(null, function(err, posts) {
            if (err) {
                posts = []
            }
            res.render('index', {
                title: '首页',
                posts: posts,
            });
        });
    });

    app.get('/reg', checkNotLogin)
    app.get('/reg', function(req, res){
        res.render('reg', {
            title:'用户注册'
        });
    });

    app.post('/reg', checkNotLogin);
	app.post('/reg', function(req, res) {
		req.session.error = null;
		req.session.success = null;
		if (req.body['password-repeat'] != req.body['password']) {
			req.session.error = '两次输入的口令不一致';
			return res.redirect('/reg');
		}

		var md5 = crypto.createHash('md5');
		var password = md5.update(req.body.password).digest('base64');

		var newUser = new User({
			name: req.body.username,
			password: password,
		});

		User.get(newUser.name, function(err, user) {
			if (user)
				err = 'Username already exists 用户已经存在!';
			if (err) {
				req.session.error = err;
				return res.redirect('/reg');
			}

			newUser.save(function(err) {
				if (err) {
					req.session.error = err;
					return res.redirect('/reg');
				}
				req.session.user = newUser;
				req.session.success = '注册成功';
				res.redirect('/');
			});
		});
	});

	app.get('/login', function(req, res) {
		req.session.error = null;
		req.session.success = null;
		res.render('login',{
			title:'用户登入',
		});
	});

	app.post('/login', checkNotLogin);
	app.post('/login', function(req, res) {
		req.session.error = null;
		req.session.success = null;
		var md5 = crypto.createHash('md5');
		var password = md5.update(req.body.password).digest('base64');
        //console.log(req.body.password);

        //console.log(req.body.username);

		User.get(req.body.username, function(err, user) {
            req.session.error = null;
            req.session.success = null;
			if (!user) {
				req.session.error = '用户不存在';
				return res.redirect('/login');
			}
            //console.log('-------------------------')
            //console.log(user.password.toString())
            //console.log(user.password)
            //console.log('-------------------------')
            //console.log(password.toString());
            //console.log(password);
			if (user.password != password) {
				req.session.error = '用户口令错误';
				return res.redirect('/login');
			}

			req.session.user = user;
			req.session.success = '登入成功';
			res.redirect('/');
		});
	});

	app.get('/logout', checkLogin)
	app.get('/logout', function(req,res){
		req.session.user = null;
        req.session.error = null;
		req.session.success = '登出成功';
		res.redirect('/');
	})

	app.post('/post', checkLogin);
	app.post('/post', function(req, res) {
		var currentUser = req.session.user;
		var post = new Post(currentUser.name, req.body.post);
        //console.log(post)
		post.save(function(err) {
			if (err) {
				req.session.error = err;
				return res.redirect('/');
			}
			req.session.success = 'post successfully!';
			res.redirect('/u/' + currentUser.name);
		});
	});

	app.get('/u/:user', function(req, res) {
        //console.log('req.session.user = %s', req.session.user);
		User.get(req.params.user, function(err, user) {
			if (!user) {
				req.session.error = "user not exist";
				return res.redirect('/');
			}
			Post.get(user.name, function(err, posts) {
				if (err) {
					req.session.error = err;
					return res.redirect('/')
				};
				res.render('user', {
					title: user.name,
					posts: posts,
				})
			});
		});
	});
};

function checkLogin(req, res, next) {
	req.session.error = null;
    req.session.success = null;
	if(!req.session.user) {
		req.session.error = 'Not login';
		return res.redirect('login')
	}
	next();
}

function checkNotLogin(req, res, next) {
	req.session.error = null;
    req.session.success = null;
	if (req.session.user) {
		req.session.error = 'Already login';
		return res.redirect('/')
	}
	next()
}

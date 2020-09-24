const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

/* Create connection */
const db = mysql.createConnection({
	host: 'localhost',
	user: 'root',
	password: '',
	database: 'intervote',
	port: 3306
});

/* Connect to MySQL */
db.connect((err) => {
	if(err){throw err;}
	console.log('MySQL Connected...');
});

const app = express();

/* Insert post id */
app.get('/addmsg', (req, res) => {
	console.log(req.query.id);
	console.log(req.query.name);
	let sql = `INSERT INTO messages SET message = '${req.query.message}', upvotes = 0, downvotes = 0`;
	let query = db.query(sql, (err, result) => {
			if(err){throw err;}
			sql = `SELECT * FROM messages`;
			query = db.query(sql, (err, result) => {
				if(err){throw err;}
				res.json(result);
			});
	});
});

/* Select posts */
app.get('/allmsgs', (req, res) => {
	let sql = 'SELECT * FROM messages';
	let query = db.query(sql, (err, results) => {
		if(err){throw err;}
		console.log(results);
		res.json(results);
	});
});

/* Update Stat */
app.get('/updatemsg', (req, res) => {
	let sql = `UPDATE messages SET upvotes = ${req.query.upvotes},downvotes = ${req.query.downvotes} WHERE id = '${req.query.id}'`;
	let query = db.query(sql, (err, results) => {
		if(err){throw err;}
		sql = `SELECT * FROM messages`;
		query = db.query(sql, (err, result) => {
			if(err){throw err;}
			res.json(result);
		});
	});
});

const port = 5000;

app.listen(port, () => `Server running on port ${port}`);

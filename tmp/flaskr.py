# import
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
#from __future__ import with_statement
from contextlib import closing

# config
DATABASE = '/Users/kinksaiz/Documents/PYTHON/FlaskBase/flaskr/DB/flaskr.db'
DEBUG = True
SECRET_KEY = 'dev_key'
USERNAME = 'kinksaiz'
PASSWORD = 'check1234'

# app main
app = Flask(__name__)
app.config.from_object(__name__)


# rendering template section
@app.route('/')
def show_entries():
	cur = g.db.execute('select title, text from entries order by id desc')
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title, text) values (?, ?)',
				[request.form['title'], request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('hello!')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('good bye!')
	return redirect(url_for('show_entries'))


# connection db
@app.before_request
def before_request():
	g.db = connect_db()

@app.after_request
def after_request(response):
	g.db.close()
	return response

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
	db.commit()

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
	app.run()

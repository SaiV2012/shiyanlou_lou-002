#!usr/bin/env python3
# -*- coding:utf-8 -*-

import json, os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/joker_sai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	created_time = db.Column(db.DateTime)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category = db.relationship('Category',backref=db.backref('files', lazy='dynamic'))
	cotent = db.Column(db.Text)

	def __init__(self, title, created_time, category, content):
		self.title = title
		self.created_time = created_time
		self.category = category
		self.content = content

	def __repr__(self):
		return '<File %r)>' % self.title

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Category %r>' % self.name

@app.route('/add')
def add():
	try:
		if (Category.query.all()):
			return "<p>there was data here"
	except:
		db.create_all()
		java = Category('Java')
		python = Category('python')
		file1 = File('Hello Java', datetime.utcnow(), java, 'File content - Java is cool!')
		file2 = File('Hello python', datetime.utcnow(), python, 'File content - Pyhton is cool!')
		db.session.add(java)
		db.session.add(python)
		db.session.add(file1)
		db.session.add(file2)
		db.session.commit()
		return "<p>add successfully!"

@app.route('/')
def index():
	ls_temp = File.query.all()
	return render_template('index.html', ls_temp=ls_temp)

@app.route('/files/<file_id>')
def file(filename):
	path = os.path.dirname(os.path.abspath('__file__')) + '/files'
	filename = filename + '.json'
	with open(path + '/' + filename, 'r') as file:
		content = json.loads(file.read())
	return render_template('file.html', content=content, filename=filename)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html')
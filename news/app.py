#!usr/bin/env python3
# -*- coding:utf-8 -*-

import json, os
from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
	path = os.path.dirname(os.path.abspath('__file__')) + '/files'
	ls_files = os.listdir(path)
	ls = []
	for file in ls_files:
		with open(path + '/' + file, 'r') as file:
			content = json.loads(file.read())
		ls.append(content['title'])
	return render_template('index.html', ls=ls)

@app.route('/files/<filename>')
def file(filename):
	path = os.path.dirname(os.path.abspath('__file__')) + '/files'
	filename = filename + '.json'
	with open(path + '/' + filename, 'r') as file:
		content = json.loads(file.read())
	return render_template('file.html', content=content, filename=filename)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html')
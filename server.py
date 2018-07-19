#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import bottle
from bottle import Bottle, route, run, template, get, post, debug, static_file, request, redirect, response, hook
from beaker.middleware import SessionMiddleware
import time
import random
import string
import logging
import logging.handlers
import pandas as pd
import numpy as np
import sqlite3
import json
import matplotlib
import cufflinks as cf
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import hashlib
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from datetime import datetime
#global variables declaration
global selectedVal
cf.set_config_file(offline=False, world_readable=True, theme='ggplot')
py.sign_in('yourUsername', 'yourPassword')

log = logging.getLogger('bottle')
log.setLevel('INFO')
h = logging.handlers.TimedRotatingFileHandler(
    'logs/nlog', when='midnight', backupCount=9999)
f = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
h.setFormatter(f)
log.addHandler(h)
global selectedVal
selectedVal = -1

secretKey = "SDMDSIUDSFYODS&TTFS987f9ds7f8sd6DFOUFYWE&FY"
session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': False,
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

def md5sum(t): #for password hashing
    return hashlib.md5(t.encode("utf8")).hexdigest()

def reduceTrans(dataToRed):
	newData = pd.DataFrame()
	for i in dataToRed['InvoiceDateFormat'].unique():
		cut = dataToRed.loc[dataToRed['InvoiceDateFormat'] == i]
		cut2 = cut.tail(len(cut) - 3)
		qsum = cut2['Quantity'].sum()
		cut2 = cut2.tail(1)
		cut2['Quantity'] = qsum
		cut2['CustomerID'] = -1
		newData = pd.concat([newData, cut.head(3), cut2])
	newData = newData.sort_values(by = 'yearMonth')
	return newData

def getData():
	conn = sqlite3.connect("databaseA.db")
	data = pd.read_sql_query('select * from onlineRetail where Description = "' + selectedVal + '"', conn)
	conn.close()
	return data
	
def makeStats():
	trans = getData()
	minDate = np.min(trans['InvoiceDate'])
	minDate = minDate.split(' ')[0]
	minDate = datetime.strptime(minDate ,'%Y-%m-%d').strftime('%d/%b/%y')
	maxDate = np.max(trans['InvoiceDate'])
	maxDate = maxDate.split(' ')[0]
	maxDate = datetime.strptime(maxDate ,'%Y-%m-%d').strftime('%d/%b/%y')
	sumQuant = np.sum(trans['Quantity'])
	totRev = np.round(np.sum(trans['Quantity'] * trans['UnitPrice']), 2)
	meanPrice = np.round(totRev / sumQuant, 2)
	minPrice = np.min(trans['UnitPrice'])
	maxPrice = np.max(trans['UnitPrice'])
	whenMaxPrice = trans['InvoiceDate'][trans.index[trans['UnitPrice'] == np.max(trans['UnitPrice'])].tolist()].values
	whenMaxPrice = list(set([val.split(' ')[0] for i, val in enumerate(whenMaxPrice)]))
	whenMaxPrice = [datetime.strptime(val ,'%Y-%m-%d') for i, val in enumerate(whenMaxPrice)]
	whenMaxPrice.sort()
	whenMaxPrice = [datetime.strftime(whenMaxPrice[i] , '%d/%b/%y') for i, val in enumerate(whenMaxPrice)]
	salesMaxPrice = np.sum(trans['Quantity'][trans.index[trans['UnitPrice'] == np.max(trans['UnitPrice'])].tolist()])
	whenMinPrice = trans['InvoiceDate'][trans.index[trans['UnitPrice'] == np.min(trans['UnitPrice'])].tolist()].values
	whenMinPrice = list(set([whenMinPrice[i].split(' ')[0] for i in range(len(whenMinPrice))]))
	whenMinPrice = [datetime.strptime(val ,'%Y-%m-%d') for i, val in enumerate(whenMinPrice)]
	whenMinPrice.sort()
	whenMinPrice = [datetime.strftime(whenMinPrice[i] , '%d/%b/%y') for i, val in enumerate(whenMinPrice)]
	salesMinPrice = np.sum(trans['Quantity'][trans.index[trans['UnitPrice'] == np.min(trans['UnitPrice'])].tolist()])
	countries = trans[['CountryISO', 'Quantity']].groupby(['CountryISO'], as_index = False, sort = False).sum()
	countriesDict = {}
	for row, val in countries.iterrows():
		countriesDict[val['CountryISO']] = val['Quantity']
	return [{'The least recent transaction': minDate, 'The most recent transaction': maxDate, 'Total sale': sumQuant, 'Total Revenue': totRev, 'Min. Price': minPrice, 'Mean Price': meanPrice, 'Max. Price': maxPrice, 'Days when minimum price occured': whenMaxPrice, 'Total sale when the price was minimum': salesMaxPrice, 'Dates when maximum price occured': whenMinPrice, 'Totale sale when the price was maximum': salesMinPrice}, countriesDict]

def makeLinePlot(trans, type, time):
	newData2 = trans[[type, 'Quantity']].groupby([type], as_index=False, sort = False).sum()
	trans.sort_values(by = type, ascending = True)
	linePlot = newData2.iplot(x = type, y = 'Quantity', title = 'Number of product sold in each ' + time, filename = 'barLine' + time)
	return linePlot
	
def makeLinePlot2(trans, type, time):
	newData2 = trans[[type, 'UnitPrice']].groupby([type], as_index=False, sort = False).sum()
	trans.sort_values(by = type)
	linePlot = newData2.iplot(x = type, y = 'UnitPrice', title = 'Price per unit in each ' + time, xTitle = 'Price', filename = 'pricePerTime' + time)
	return linePlot
	
def makeLinePlot3(trans):
	newData2 = trans[['Quantity', 'UnitPrice']].groupby(['UnitPrice'], as_index=False, sort = False).sum()
	newData2 = newData2.sort_values(by = 'Quantity')
	linePlot = newData2.iplot(x = 'Quantity', y = 'UnitPrice', title = 'Demand curve', yTitle = 'Price', xTitle = 'Quantity', filename = 'priceQuantity')
	return linePlot

def makeCombinedPlot(trans, type, time):
	# columns that help to sort dates before statisticts
	trans['yearMonth'] = pd.to_datetime(trans.InvoiceDate).map(lambda x: 100 * x.year + x.month)
	trans['yearMonthDay'] = pd.to_datetime(trans.InvoiceDate).map(lambda x: (100 * x.year + x.month) * 100 + x.day)
	trans['InvoiceDateFormat2'] = pd.to_datetime(trans.InvoiceDate).dt.strftime('%d/%b/%y')
	trans.sort_values(by = 'InvoiceDateFormat2')
	trans['InvoiceDateFormat'] = pd.to_datetime(trans.InvoiceDate).dt.strftime('%b/%y')
	timeSer = trans[['InvoiceDateFormat', 'Quantity', 'CustomerID', 'yearMonth']].groupby(['InvoiceDateFormat', 'CustomerID'], as_index=False).sum()
	timeSer = timeSer.sort_values(by=['InvoiceDateFormat', 'Quantity'], ascending = False)
	reducedData = reduceTrans(timeSer)
	dataToPlot = reducedData.groupby(['InvoiceDateFormat', 'CustomerID'], sort = False)['Quantity'].sum().unstack('CustomerID')#.fillna(0)
	trans = trans.sort_values(by = 'yearMonthDay')
	dataLine = trans[[type, 'Quantity']].groupby([type], as_index=False, sort = False).sum()
	linePlot = dataLine.iplot(x = type, y = 'Quantity', asFigure = True, filename = 'barLine', title = 'Number of product sold in each ' + time)
	barPlot = dataToPlot.iplot(kind='bar', barmode='stack', asFigure = True, filename = 'barPlot', legend = False, title = 'Number of products sold in each month by Customer<br>(only 3 Customers with the greatest amount are showed)', xTitle = 'Customer with ID = 0 mens "Others"', colorscale = 'RdBu')
	barPlot['data'].extend(linePlot['data'])
	combinedPlot = py.iplot(barPlot,  xTitle = 'Quantity', filename = 'Combo')
	return combinedPlot

	
def getProductList():
	conn = sqlite3.connect("databaseA.db")
	# slect from view (performance)
	productList = pd.read_sql_query("select * from products", conn)
	productList = dict(enumerate(productList['Description'], 1))
	conn.close()
	return productList

#def getUsers(): ##for further using in def login() and used after SECRET KEY
#	dane = pd.read_csv('users.csv', sep = ';')
#	users = {} #for further using in def login()
#	for index, row in dane.iterrows():
#		specUser = {}
#		name = row['name']
#		specUser['name'], specUser['password'], specUser['loggedIn'], specUser['lastSeen'], specUser['randStr']  = name, #row['password'], row['loggedIn'], row['lastSeen'], row['randStr']
#		users[name] = specUser
#	return users

def getUsers(): #written as getUsersDB at scratch
	conn = sqlite3.connect("databaseA.db")
	c = conn.cursor()
	c.execute("SELECT * FROM users")
	userslist = c.fetchall()
	conn.close()
	users = {} #for further using in def login()
	for i in userslist:
		specUser = {}
		name = i[0] 
		specUser['name'] = name
		#specUser['password'] = i[1] #could be restored
		#specUser['email'] = i[2]
		specUser['loggedIn'] = bool(i[3])
		specUser['lastSeen'] = i[5]
		specUser['randStr'] = i[4]
		#specUser['isAdmin'] = bool(i[6])
		users[name] = specUser
	del(userslist)
	return users


def getItems(searchItem):
	conn = sqlite3.connect("databaseA.db")
	df = pd.read_sql_query('select * from onlineRetail where InvoiceNo in (select InvoiceNo from onlineRetail where Description = "' + searchItem + '") ;', conn)
	df['Description'] = df['Description'].str.strip()
	conn.close()
	return df
	
def encode_units(x):
	if x <= 0:
		return 0
	if x >= 1:
		return 1

def getRules(item):
	conn = sqlite3.connect("databaseA.db")
	df = pd.read_sql_query('select * from rules where antecedants like "%' + item + '%";', conn)
	df['antecedants'] = df['antecedants'].str.split(';')
	df['consequents'] = df['consequents'].str.split(';')
	df['support'] = df['support'].round(decimals = 4)
	df['confidence'] = df['confidence'].round(decimals = 4)
	df['lift'] = df['lift'].round(decimals = 2)
	dict = {}
	for i, row in df.iterrows():
		dict[str(i)] = {'antecedants': row['antecedants'], 'consequents': row['consequents'], 'support': row['support'], 'confidence': row['confidence'], 'lift': row['lift']}
	conn.close()
	return dict


# get users from sql to dict
users = getUsers()

def checkAuth():
	loginName = request.get_cookie("user", secret = secretKey)
	#print('checkAuth')
	print(loginName)
	randStr = request.get_cookie("randStr", secret = secretKey)
	#print(randStr)
	#print(users[loginName].get("randStr", ""))
	log.info(str(loginName) + ' ' + request.method + ' ' +
			request.url + ' ' + request.environ.get('REMOTE_ADDR'))
	users = getUsers() #create users dictionary. it still very fast and useful here
	print(users)
	print(loginName in users, users[loginName].get("randStr", "") == randStr, users[loginName]["loggedIn"] == True)
	if (loginName in users) and (users[loginName]["loggedIn"] == True):
		conn = sqlite3.connect("databaseA.db")
		c = conn.cursor()
		c.execute('UPDATE users SET LastSeen = "' + str(time.time()) + '"  WHERE Name = "' + loginName + '"')
		conn.commit()
		conn.close()
        #users[loginName]["lastSeen"] = time.time()
		del(users)
		print('inside if')
		return loginName
	elif (loginName in users) and (users[loginName]["loggedIn"] == True):
		conn = sqlite3.connect("databaseA.db")
		c = conn.cursor()
		c.execute('UPDATE users SET LoggedIn = "' + str(0) + '"  WHERE Name = "' + loginName + '"')
		conn.commit()
		conn.close()
		del(users)
		print('inside elif')
		return loginName
	else:
		print('inside else')
		del(users)
		return redirect('/login')


#def checkAuth(): #old version
#	loginName = request.get_cookie("user", secret = secretKey)
#	#print('checkAuth')
#	#print(loginName)
#	randStr = request.get_cookie("randStr", secret = secretKey)
#	#print(randStr)
#	#print(users[loginName].get("randStr", ""))
#	log.info(str(loginName) + ' ' + request.method + ' ' +
#			request.url + ' ' + request.environ.get('REMOTE_ADDR'))
#	if (loginName in users) and (users[loginName].get("randStr", "") == randStr) and (users[loginName]["loggedIn"] == True) and #(time.time() - users[loginName]["lastSeen"] < 3600):
#		users[loginName]["lastSeen"] = time.time()
#		return loginName
#	return redirect('/login')

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='./static')

@route('/')
@route('/login')
@route('/login/')
@route('/login', method='POST')
def login():
	loginName = request.get_cookie("user", secret = secretKey)
	if loginName:
		redirect('/searchSite')
	message = {'content': ''}
	loginName = request.forms.get('login_name', default="starting") #never delete user "starting" from table "users"
	password = md5sum(request.forms.get('password', default="wrong")) #from page
	randStr = ''.join(random.choice(
		string.ascii_uppercase + string.digits) for _ in range(18))
	log.info(str(loginName) + ' ' + request.method + ' ' +
			request.url + ' ' + request.environ.get('REMOTE_ADDR'))
	conn = sqlite3.connect("databaseA.db")
	c = conn.cursor()
	c.execute('SELECT Name FROM users')
	result = c.fetchall()
	exist = 0
	for i in result: #it prevents error 500 in case of uncorrect name/password
		if loginName == i[0]:
			exist = 1
			break
	del(result)
	if exist == 0:
		message['content'] = 'This user does not exist :('
		message = json.dumps(message)
		return template('login', message = message)
	c.execute('SELECT Password FROM users WHERE Name = "' + loginName + '"')
	ourpassword = (c.fetchone())[0] #already hashed
	conn.close()
	if (ourpassword == password):
		response.set_cookie("user", loginName, secret=secretKey)
		response.set_cookie("randStr", randStr, secret=secretKey)
		conn = sqlite3.connect("databaseA.db")
		c = conn.cursor()
		c.execute('UPDATE users SET LoggedIn = "' + str(1) + '" , RandStr = "' + randStr + '" , \
        LastSeen = "' + str(time.time()) + '"  WHERE Name = "' + loginName + '"')
		conn.commit()
		conn.close()
		redirect('/searchSite')
		del(ourpassword)
		return True
	elif (loginName != "starting"):
		del(ourpassword)
		message['content'] = 'Password is not correct! (:'
		message = json.dumps(message)
		return template('login', message = message)
	else:
		del(ourpassword)
		#message['content'] = 'Please provide Login and Password ('
		#message = json.dumps(message)
		return template('login', message = message)

@route('/loggingOut')	
def logOut():
	response.set_cookie('user', '')
	redirect('/login')
		
@route('/registration')
@route('/registration/')
@route('/registration', method = 'POST')
def registration():
	message = {'content': ''}
	loginName = request.forms.get('login_name', default="starting") #never delete user "starting" from table "users"
	email = request.forms.get('email', default="email@email")
	password = request.forms.get('password', default="wrong") #from page
	password2 = request.forms.get('password2', default="wrong")
	print(loginName, email, password, password2)
	#if loginName == 'starting' or email == 'email@email' or password == 'wrong' or password2 == 'wrong':
		#return template('registration', message = message)
	if loginName == '' or email == '' or password == '' or password2 == '':
		message['content'] = 'Please fill all fields!'
		message = json.dumps(message)
		return template('registration', message = message)
	elif password != password2:
		message['content'] = 'Passwords are not equal!'
		message = json.dumps(message)
		return template('registration', message = message)
	#else:
		#log.info(str(loginName) + ' ' + request.method + ' ' +
				#request.url + ' ' + request.environ.get('REMOTE_ADDR'))
		#if password != password2:
			#return template('registration', message = message)
	conn = sqlite3.connect("databaseA.db")
	c = conn.cursor()
	c.execute('SELECT Name FROM users')
	result = c.fetchall()
	exist = 0
	for i in result: #it prevents error 500 in case of uncorrect name/password
		if (loginName == i[0]) and (loginName != "starting"):
			exist = 1
			#break
	del(result)
	if exist == 1:
		conn.close()
		redirect('/login')
	elif loginName != "starting":
		conn.create_function("md5", 1, md5sum)
		c.execute('INSERT INTO users VALUES (?, md5(?), ?, ?, ?, ?, ?)', (loginName, password, email, 0, '""', 0, 0))
		conn.commit()
		conn.close()
	#if (ourpassword == password): #from DB of CSV????? See function GetUsers. is dictionary of from function
		redirect('/login')
	else:
		conn.close()
		return template('registration', message = message)
	#loginName = "starting"
	#return template('login')

@route('/rules')
@route('/rules/')
def rules():
	loginName = checkAuth()
	s = bottle.request.environ.get('beaker.session')
	rules = getRules(s['selectedVal'])
	print(rules)
	rules = json.dumps(rules)
	return template('rules', rules = rules, login = loginName)
	
@route('/searchSite')
@route('/searchSite', method='POST')
def returnText():
	loginName = checkAuth()
	global selectedVal
	selectedVal = request.forms.get('sel', default=False)
	s = bottle.request.environ.get('beaker.session')
	s['selectedVal'] = selectedVal
	s.save()
	if selectedVal == False:
		searchVal = getProductList()
		searchVal = json.dumps(searchVal)
		return template('search', products = searchVal, login = loginName)
	else:
		redirect('/statistics')
		return True

@route('/searchSite2')
@route('/searchSite2', method='POST')
def returnText():
	loginName = checkAuth()
	global selectedVal
	selectedVal = request.forms.get('sel', default=False)
	print(selectedVal)
	s = bottle.request.environ.get('beaker.session')
	s['selectedVal'] = selectedVal
	s.save()
	print(selectedVal)
	if selectedVal == False:
		searchVal = getProductList()
		searchVal = json.dumps(searchVal)
		return template('search2', products = searchVal, login = loginName)
	else:
		redirect('/statistics')
		return True
		
@route('/statistics')
def makePlot():
	loginName = checkAuth()
	if selectedVal == '':
		redirect('/searchSite2')
	else:
		data = getData()
		plotToDraw1 = makeCombinedPlot(data, 'InvoiceDateFormat', 'month')
		plotToDraw2 = makeLinePlot(data, 'InvoiceDateFormat2', 'day')
		plotToDraw3 = makeLinePlot2(data, 'InvoiceDateFormat', 'month')
		plotToDraw4 = makeLinePlot3(data)
		stats = makeStats()[0]
		countries = makeStats()[1]
		stats = json.dumps(stats)
		countries = json.dumps(countries)
		return template('statisticts', stats = stats, countries = countries, selectedVal = selectedVal, login = loginName)

	
@route('/index')
@route('/index/')
@route('/index/<message>')
def index(message=''):
	loginName = checkAuth()
	print(loginName)
	print('after Auth')
	messDict = {'error': "Something went wrong",
				'ok': "Everything is ok."}
	return template('index', message=messDict.get(message, ""), loginName=loginName)

run(
    app=app,
    host='localhost',
    port= 8080
)
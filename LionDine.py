from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

from bs4 import BeautifulSoup
import requests
import datetime



menus = {}
menus['date']=""

def getMenu(x):
	if x == "ferris":
		url = "https://dining.columbia.edu/menus/64"
	if x == "jjs":
		url = "https://dining.columbia.edu/menus/66"
	if x == "john jay":
		url = "https://dining.columbia.edu/menus/67"
	content = requests.get(url).content
	soup = BeautifulSoup(content,"lxml")
	foods = soup.findAll("span", {"class": "meal-title-calculator"})
	array = []
	for x in foods:
		food = x.text
		array.append(food)
	return array

def getName(x):
	if x == "ferris":
		name = "Ferris"
	if x == "jjs":
		name = "JJ's"
	if x == "john jay":
		name = "John Jay"
	return name


def printMenu(foods, name):
	if len(foods) == 0:
		str = "Looks like " + name + " is closed today.  Try with a different dining location to check the menu there."
		return str
	else:
		str = "The menu at " + name + " is: \n"
		for x in foods:
			str += x + "\n"
	return str[:-1]

def process(text):
	#check if it's a new day and if so, update data
	now = str(datetime.datetime.now()).split()[0]
	if menus['date']!=str(now):
		menus['ferris']=getMenu('ferris')
		menus['jjs']=getMenu('jjs')
		menus['john jay']=getMenu('john jay')
		menus['date']=str(now)

	text = text.lower()

##    if text.split()[0] == "menu":
##
##        menu = menus[text[1]]
##        return printMenu(menu, text[1])
		# for food in menu:
			#print(food)
	if(text=="who is god?"):
		return "Sergio is god"
	if text.split()[0] == "find":
		food = text[5:]
		return printLocations(findFood(food), food)
	else:
		if "john jay" in text or "johnjay" in text:
			menu = menus["john jay"]
			return printMenu(menu, "John Jay")
		elif "ferris" in text:
			menu = menus["ferris"]
			return printMenu(menu, "Ferris")
		elif "jjs" in text or "jj's" in text:
			menu = menus["jjs"]
			return printMenu(menu, "JJ's")
		else:
			return "Welcome to LionDine!  Ask about a dining hall for their menu or say 'find <food>' to see where it's available!"

def findFood(name):
	foods = set()

	johnJay = menus["john jay"]
	for x in johnJay:
		if (x.lower()).find(name.lower()) > 0:
			foods.add("John Jay: "+x)

	ferris = menus["ferris"]
	for x in ferris:
		if (x.lower()).find(name.lower()) > 0:
			foods.add("Ferris: " + x)

	jj = menus["jjs"]
	for x in jj:
		if (x.lower()).find(name.lower()) > 0:
			foods.add("JJ's: " +x)
	return foods

def printLocations(locations, food):
	food=food[:-1]
	if len(locations) > 0:
		str = "Search results for \"" +  food + "\" in dining halls:\n"
		for x in locations:
			str += x+"\n"
		return str[:-1]
	else:
		return("We didn't find any results for \"" + food+"\" at a Columbia dining hall today :(")

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():


	body = request.values.get('Body', None)

	resp = MessagingResponse()

	resp.message(process(body))
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)





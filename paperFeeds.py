import datetime
import requests
# from telegram.ext import *
import paramiko
from time import sleep
import feedparser
from os.path import exists
import json
from bs4 import BeautifulSoup

def checkFeeds (url):
	newsFeed = feedparser.parse(url)
	return newsFeed['entries']

def removeSpaces (inputString):
	while (" " in inputString):
		inputString = inputString.replace ("  ", "")
	inputString = inputString.replace ("\t", "")
	return inputString

def sendMessage (msg):
	url = ({}/sendMessage?chat_id=@polymerpapers&text={}".format (channelAPI, msg))

	while True:
		try:
			request = requests.post (url)
			if (request.status_code == 200):
				break
			else:
				continue
		except:
			continue

def printDict (inputDict):
	for item in inputDict:
		if (checkRelevance (item['link'])):
			sendMessage (item['title'] + "\n" + item['link'])
			sleep (5)

def checkRelevance (url):
	response = requests.get (url)
	paperContents = response.text
	cleanText = BeautifulSoup(paperContents, "lxml").text
	cleanText = cleanText.lower ()
	keywords = ['crytallization', 'nucleation', 'napss', 'na pss', 'na-pss', 'sodium polystyrene sulfonate', 'sodium (polystyrene sulfonate)', 'sps', 'molecular dynamics', 'md', 'simulation', 'computation']
	wordCount = 0

	for word in keywords:
		wordCount += cleanText.count (word)

	if (wordCount > 0):
		return 1
	else:
		# This should return 0, but there aren't many relevant papers while searching strictly with those keywords
		# So temporarily changing this to 1. 
		# Later on, this can be changed to 0 and the bot can return very relevant searches
		return 1

def findNewPapers (feeds1, feeds2):
	print ("Finding new papers")
	itemFound = 0

	for item2 in feeds2:
		for item1 in feeds1:
			if (item2['id'] == item1['id']):
				itemFound = 1

	if (itemFound == 0):
		isRelevant = checkRelevance (item['link'])
		if (isRelevant):
			sendMessage (item['title'] + "\n" + item['link'])

def getInitialFeeds (logFile, url):
	isFileExists = exists (logFile)
	if (not isFileExists):
		initialFeeds = checkFeeds (url)
		with open (logFile, "w", encoding = 'utf-8') as file:
			json.dump (initialFeeds, file)
		printDict (initialFeeds)
	else:
		with open (logFile, "r", encoding = 'utf-8') as file:
			initialFeeds = json.load (file)

	return initialFeeds

def saveFeeds (logFile, feeds):
	with open (logFile, "w", encoding = 'utf-8') as file:
		json.dump (feeds, file)

def main ():
	print ("Loading Polymer...")
	polymerFeed1 = getInitialFeeds ("polymer.log", "https://rss.sciencedirect.com/publication/science/00323861")
	print ("Loading Macromolecules...")
	macromoleculesFeed1 = getInitialFeeds ("macromolecules.log", "http://feeds.feedburner.com/acs/mamobx")
	print ("Loading Acta Materialia...")
	actaMaterialiaFeed1 = getInitialFeeds ("actaMaterialia.log", "https://rss.sciencedirect.com/publication/science/13596454")
	print ("Loading Progress in Polymer Science")
	progressInPolymerScienceFeed1 = getInitialFeeds ("progressInPolymerScience.log", "https://rss.sciencedirect.com/publication/science/00796700")
	print ("Loading Biomacromolecules...")
	biomacromoleculesFeed1 = getInitialFeeds ("biomacromolecules.log", "http://feeds.feedburner.com/acs/bomaf6")
	print ("Loading Carbohydrate Polymers...")
	carbohydratePolymersFeed1 = getInitialFeeds ("carbohydratePolymers.log", "https://rss.sciencedirect.com/publication/science/01448617")
	print ("Loading Applied Polymer Science...")
	appliedPolymerScienceFeed1 = getInitialFeeds ("appliedPolymerScience.log", "https://onlinelibrary.wiley.com/action/showFeed?jc=10974628&type=etoc&feed=rss")
	print ("Loading Polymer Degradation and Stability...")
	polymerDegradationAndStabilityFeed1 = getInitialFeeds ("polymerDegradationAndStability.log", "https://rss.sciencedirect.com/publication/science/01413910")
	print ("Loading Macromolecular Rapid Communication...")
	macromolecularRapidCommunicationFeed1 = getInitialFeeds ("macromolecularRapidCommunication.log", "https://onlinelibrary.wiley.com/feed/15213927/most-recent")
	print ("Loading Journal of Polymer Science...")
	polymerScienceFeed1 = getInitialFeeds ("polymerScience.log", "https://onlinelibrary.wiley.com/feed/26424169/most-recent")
	print ("Loading European Journal of Polymer Science...")
	europeanPolymerScienceFeed1 = getInitialFeeds ("europeanPolymerScience.log", "https://rss.sciencedirect.com/publication/science/00143057")

	print ("Checking Polymer...")
	polymerFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/00323861")
	print ("Checking Macromolecules...")
	macromoleculesFeed2 = checkFeeds ("http://feeds.feedburner.com/acs/mamobx")
	print ("Checking Acta Materialia...")
	actaMaterialiaFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/13596454")
	print ("Checking Progress in Polymer Science...")
	progressInPolymerScienceFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/00796700")
	print ("Checking Biomacromolecules...")
	biomacromoleculesFeed2 = checkFeeds ("http://feeds.feedburner.com/acs/bomaf6")
	print ("Checking Carbohydrate Polymers...")
	carbohydratePolymersFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/01448617")
	print ("Checking Applied Polymer Science...")
	appliedPolymerScienceFeed2 = checkFeeds ("https://onlinelibrary.wiley.com/action/showFeed?jc=10974628&type=etoc&feed=rss")
	print ("Checking Polymer Degradation and Stability...")
	polymerDegradationAndStabilityFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/01413910")
	print ("Checking Macromolecular Rapid Communication...")
	macromolecularRapidCommunicationFeed2 = checkFeeds ("https://onlinelibrary.wiley.com/feed/15213927/most-recent")
	print ("Checking Journal of Polymer Science...")
	polymerScienceFeed2 = checkFeeds ("https://onlinelibrary.wiley.com/feed/26424169/most-recent")
	print ("Checking European Journal of Polymer Science...")
	europeanPolymerScienceFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/00143057")

	findNewPapers (polymerFeed1, polymerFeed2)
	findNewPapers (macromoleculesFeed1, macromoleculesFeed2)
	findNewPapers (actaMaterialiaFeed1, actaMaterialiaFeed2)
	findNewPapers (progressInPolymerScienceFeed1, progressInPolymerScienceFeed2)
	findNewPapers (biomacromoleculesFeed1, biomacromoleculesFeed2)
	findNewPapers (carbohydratePolymersFeed1, carbohydratePolymersFeed2)
	findNewPapers (appliedPolymerScienceFeed1, appliedPolymerScienceFeed2)
	findNewPapers (polymerDegradationAndStabilityFeed1, polymerDegradationAndStabilityFeed2)
	findNewPapers (macromolecularRapidCommunicationFeed1, macromolecularRapidCommunicationFeed2)
	findNewPapers (polymerScienceFeed1, polymerScienceFeed2)
	findNewPapers (europeanPolymerScienceFeed1, europeanPolymerScienceFeed2)

	saveFeeds ("polymer.log" ,polymerFeed2)
	saveFeeds ("macromolecules.log" ,macromoleculesFeed2)
	saveFeeds ("actaMaterialia.log" ,actaMaterialiaFeed2)
	saveFeeds ("progressInPolymerScience.log" ,progressInPolymerScienceFeed2)
	saveFeeds ("biomacromolecules.log" ,biomacromoleculesFeed2)
	saveFeeds ("carbohydratePolymers.log" ,carbohydratePolymersFeed2)
	saveFeeds ("appliedPolymerScience.log" ,appliedPolymerScienceFeed2)
	saveFeeds ("polymerDegradationAndStability.log" ,polymerDegradationAndStabilityFeed2)
	saveFeeds ("macromolecularRapidCommunication.log" ,macromolecularRapidCommunicationFeed2)
	saveFeeds ("polymerScience.log" ,polymerScienceFeed2)
	saveFeeds ("europeanPolymerScience.log" ,europeanPolymerScienceFeed2)
	print ("Sleeping for the next 1 hour...")
	now = now = datetime.datetime.utcnow()+datetime.timedelta(hours = 0, minutes = 0)
	print ("Current time: {}".format (now))

if __name__ == '__main__':
	while True:
		main()
		sleep (3600)

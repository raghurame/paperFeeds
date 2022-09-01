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
	# for i in newsFeed['entries']:
	# 	print (i)
	# 	exit (1)
	return newsFeed['entries']

def removeSpaces (inputString):
	while (" " in inputString):
		inputString = inputString.replace ("  ", "")
	inputString = inputString.replace ("\t", "")
	return inputString

def sendMessage (msg):
	url = ("https://api.telegram.org/bot1527916318:AAHAi0r-XS3HLFObPDhttjeNMhegwSNDF3g/sendMessage?chat_id=@polymerpapers&text={}".format (msg))

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
			sendMessage (item['title'] + "\n" + item['id'])
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
		# Later on, this can be changed to 0 and the bot can return relevant searches
		return 1

def findNewPapers (feeds1, feeds2):
	print ("Finding new papers")

	for item2 in feeds2:
		itemFound = 0
		for item1 in feeds1:
			if (item2['id'] == item1['id']):
				itemFound = 1

		if (itemFound == 0):
			isRelevant = checkRelevance (item2['link'])
			print ("itemFound == 0\t" + item2['link'])
			if (isRelevant):
				sendMessage (item2['title'] + "\n" + item2['id'])

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
			# for i in initialFeeds:
			# 	print (i)
			# exit (1)

	return initialFeeds

def saveFeeds (logFile, feeds):
	with open (logFile, "w", encoding = 'utf-8') as file:
		json.dump (feeds, file)

def main ():
	polymerFeed1 = getInitialFeeds ("polymer.log", "https://rss.sciencedirect.com/publication/science/00323861")
	macromoleculesFeed1 = getInitialFeeds ("macromolecules.log", "http://feeds.feedburner.com/acs/mamobx")
	actaMaterialiaFeed1 = getInitialFeeds ("actaMaterialia.log", "https://rss.sciencedirect.com/publication/science/13596454")
	progressInPolymerScienceFeed1 = getInitialFeeds ("progressInPolymerScience.log", "https://rss.sciencedirect.com/publication/science/00796700")
	biomacromoleculesFeed1 = getInitialFeeds ("biomacromolecules.log", "http://feeds.feedburner.com/acs/bomaf6")
	carbohydratePolymersFeed1 = getInitialFeeds ("carbohydratePolymers.log", "https://rss.sciencedirect.com/publication/science/01448617")
	appliedPolymerScienceFeed1 = getInitialFeeds ("appliedPolymerScience.log", "https://onlinelibrary.wiley.com/action/showFeed?jc=10974628&type=etoc&feed=rss")
	polymerDegradationAndStabilityFeed1 = getInitialFeeds ("polymerDegradationAndStability.log", "https://rss.sciencedirect.com/publication/science/01413910")
	macromolecularRapidCommunicationFeed1 = getInitialFeeds ("macromolecularRapidCommunication.log", "https://onlinelibrary.wiley.com/feed/15213927/most-recent")
	polymerScienceFeed1 = getInitialFeeds ("polymerScience.log", "https://onlinelibrary.wiley.com/feed/26424169/most-recent")
	europeanPolymerScienceFeed1 = getInitialFeeds ("europeanPolymerScience.log", "https://rss.sciencedirect.com/publication/science/00143057")

	polymerFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/00323861")
	macromoleculesFeed2 = checkFeeds ("http://feeds.feedburner.com/acs/mamobx")
	actaMaterialiaFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/13596454")
	progressInPolymerScienceFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/00796700")
	biomacromoleculesFeed2 = checkFeeds ("http://feeds.feedburner.com/acs/bomaf6")
	carbohydratePolymersFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/01448617")
	appliedPolymerScienceFeed2 = checkFeeds ("https://onlinelibrary.wiley.com/action/showFeed?jc=10974628&type=etoc&feed=rss")
	polymerDegradationAndStabilityFeed2 = checkFeeds ("https://rss.sciencedirect.com/publication/science/01413910")
	macromolecularRapidCommunicationFeed2 = checkFeeds ("https://onlinelibrary.wiley.com/feed/15213927/most-recent")
	polymerScienceFeed2 = checkFeeds ("https://onlinelibrary.wiley.com/feed/26424169/most-recent")
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

if __name__ == '__main__':
	main()
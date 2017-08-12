import sys
import signal
from time import sleep

import RPi.GPIO as GPIO

import twitter
from credentials import *

import re
from textblob import TextBlob

channel = 11

bear_id = 888598391298465792

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)

#GPIO.output(channel, GPIO.HIGH)

def signal_handler(signal, frame):
	print 'Caught SIGINT - exiting cleanly...'
	GPIO.cleanup()
	sys.exit()

def clean_tweet(tweet):
	'''
	Utility function to clean tweet text by removing links, special characters
	using simple regex statements.
	'''
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analyse_tweet(tweet):
	analysis = TextBlob(clean_tweet(tweet))
	return analysis.sentiment.polarity

#signal.signal(signal.SIGINT, signal_handler)

api = twitter.Api(consumer_key=CONSUMER_KEY,
                consumer_secret=CONSUMER_SECRET,
                access_token_key=ACCESS_TOKEN,
                access_token_secret=ACCESS_SECRET)

#timeline = api.GetHomeTimeline()
#print timeline

#status = api.PostUpdate('Another post!')

try:
	stream = api.GetStreamFilter(track=['#colabsau'])

	for line in stream:
		text = line['text']
		sen_val = analyse_tweet(text)
		print text
		print 'Sentiment: ' + str(sen_val)
		print '###########'

		if sen_val > 0.5 and line['user']['id'] != bear_id:
			print 'Reposting!'
			api.PostRetweet(line['id'])

except:
	print 'Error in reading stream!'
	GPIO.cleanup()

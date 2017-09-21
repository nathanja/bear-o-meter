import sys
import signal
from time import sleep

from threading import Timer

from datetime import datetime

try:
	import RPi.GPIO as GPIO
except:
	GPIO = None

import twitter
from credentials import *

import re
from textblob import TextBlob

# Global constants/variables
channels = [3,5]
fan_balance = 0
gpio_initialised = False

# 1 Jan 1970 constant
epoch = datetime.utcfromtimestamp(0)

# Function for converting timestamps to epochs
def datetime_to_epoch(datestring):
	global epoch
    #time_pattern = '%Y/%m/%d %H:%M:%S.%f'

    #dt = datetime.strptime(datestring,time_pattern)
    #dt = datetime.utcnow()
	dt = datetime.fromtimestamp(datestring)

    return (dt - epoch).total_seconds()


def init_gpio():
	global gpio_initialised
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(channels, GPIO.OUT, initial=GPIO.LOW)
	gpio_initialised = True


def signal_handler(signal, frame):
	print 'Caught SIGINT - exiting cleanly...'
	global gpio_initialised
	if gpio_initialised:
		print('Cleaning up GPIO')
		GPIO.cleanup()
		gpio_initialised = False

	sys.exit()


def reset_timer(tim, new_time, func, f_args)
	tim.cancel()
	tim = Timer(new_time, func, args=f_args)
	tim.start()
	return tim


def inflate(power='FULL'):
	print('Inflating ' + power)
	if power == 'FULL':
		GPIO.output(channels, GPIO.HIGH)
	elif power == 'OFF':
		GPIO.output(channels, GPIO.LOW)
	elif power == 'HALF':
		if fan_balance == 0:
			GPIO.output(channels, (GPIO.HIGH, GPIO.LOW))
			fan_balance = 1
		else:
			GPIO.output(channels, (GPIO.LOW, GPIO.HIGH))
			fan_balance = 0
	else:
		print('Warning: unknown power level input!')
		GPIO.output(channels, GPIO.LOW)	


def clean_tweet(tweet):
	'''
	Utility function to clean tweet text by removing links, special characters
	using simple regex statements.
	'''
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def analyse_tweet(tweet):
	#analysis = TextBlob(clean_tweet(tweet))
	analysis = TextBlob(tweet)
	return analysis.sentiment.polarity


def analyse_stream(bear_id, track_list):
	if not track_list:
		print 'You gave me nothing to track!'
		return

	try:
		stream = api.GetStreamFilter(track=track_list)
		tim = Timer(30.0, inflate, args=['OFF'])

		last_time = 0

		for line in stream:
			text = line['text']
			sen_val = analyse_tweet(text)
			print text
			print 'Sentiment: ' + str(sen_val)
			print '###########'
			
			if 'power on' in text.lower():
				inflate('FULL')
			elif 'power off' in text.lower():
				inflate('OFF')
			elif sen_val > 0.39 and line['user']['id'] != bear_id:
				print 'Reposting!'
				api.CreateFavorite(status_id=line['id'])
				api.PostRetweet(line['id'])

				tweet_time = datetime_to_epoch(line['created_at'])
				inflate('FULL')

				time_dif = tweet_time - last_time
				if time_dif > 120.0:
					tim = reset_timer(tim, 60.0, inflate, ['OFF'])

				elif time_dif > 20.0:
					tim = reset_timer(tim, 45.0, inflate, ['OFF'])
		
				else:
					tim = reset_timer(tim, 30.0, inflate, ['OFF'])

				last_time = tweet_time

	except:
		print 'Error in reading stream!'
		global gpio_initialised

		if gpio_initialised:
			print('Cleaning up GPIO')
			GPIO.cleanup()
			gpio_initialised = False


if __name__ == '__main__':

	signal.signal(signal.SIGINT, signal_handler)

	api = twitter.Api(consumer_key=CONSUMER_KEY,
					consumer_secret=CONSUMER_SECRET,
					access_token_key=ACCESS_TOKEN,
					access_token_secret=ACCESS_SECRET)

	init_gpio()
	#timeline = api.GetHomeTimeline()
	#print timeline

	#status = api.PostUpdate('Another post!')

	myself = api.VerifyCredentials().AsDict()
	print 'id: ', myself['id']
	print 'name: ', myself['name']
	print 'screen_name: ', myself['screen_name']
	analyse_stream(myself['id'], ['#colabssydney','@'+myself['screen_name']])



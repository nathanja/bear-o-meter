import sys

import twitter
from credentials import *

api = twitter.Api(consumer_key=CONSUMER_KEY,
                consumer_secret=CONSUMER_SECRET,
                access_token_key=ACCESS_TOKEN,
                access_token_secret=ACCESS_SECRET)

#timeline = api.GetHomeTimeline()
#print timeline

#status = api.PostUpdate('Another post!')

import re
import traceback
import time
import random
from api_access_object import twitter_api as TwitterAPI

# twitter_object = TwitterAPI._get_api_client(TwitterAPI._get_api_auth_details())
# print 'testing'
# TwitterAPI.bot_lookup(twitter_object,'yathshar')


######################################################################################################################
########################### The non streaming functions of the bot #######################################################


def love_user_only(screen_name,message = "This is a default message"):
	## Initialiazing the API keys
	twitter_object = TwitterAPI._get_api_client(TwitterAPI._get_api_auth_details())
	paginate_older_attribute = '0'

	while True:
		try:
			## calling the twitter's user_timeline end point
			tweets = TwitterAPI.get_user_tweets(twitter_object,screen_name,paginate_older_attribute)

			## following the user and sending him a DM
			TwitterAPI.bot_follow(twitter_object,screen_name)
			print "followed user -> " , screen_name

			if (len(tweets) > 0):
				for tweet in tweets:
					try:
						## retweet and like the tweets
						TwitterAPI.bot_retweet(twitter_object,str(tweet['id_str']))
						print "retweeted the tweet_id -> " , tweet['id']
						TwitterAPI.bot_like(twitter_object,str(tweet['id_str']))
						print "liked the tweet_id -> " , tweet['id']
						TwitterAPI.bot_reply(twitter_object,'@'+tweet['user']['screen_name']+' '+message,tweet['id'])
						print "replied to user -> " , tweet['user']['screen_name'], " with this message ->", message

					except Exception, e:
						print "Error: %s" % e
						continue

				## Twitter allows only 200 posts per user in 1 call. Therefore, we need to paginate to
				##older tweets to get the allowed 3200 tweets for a user
				new_paginate_older_attribute = str(min(tweets, key = lambda x: int(x['id']))['id'])
				paginate_older_attribute = str(int(new_paginate_older_attribute) - 1)

			## DM will only work if user is following you

			else:
				TwitterAPI.bot_chat(twitter_object,message,screen_name)
				print "Sent a DM to -> " , screen_name, "With message - > ", message
				print "Completed the task...Exiting now!!"
				break


		except Exception, e:
			print "This needs you attention %s" % e
			##  sleep and try again
			time.sleep(random.randint(0,50))

def love_tweets_with_message(text_to_search, message = "This is a bot!!"):
	## Initialiazing the API keys
	twitter_object = TwitterAPI._get_api_client(TwitterAPI._get_api_auth_details())
	paginate_older_attribute = '0'
	while True:
		try:
			## calling the twitter's search post end point

			tweets = TwitterAPI.get_tweets(twitter_object,text_to_search,paginate_older_attribute)
			if (len(tweets['statuses']) > 0):
				for tweet in tweets['statuses']:

					## if the tweets are matching the search criteria then follow/retweet/like/reply/send a DM
					TwitterAPI.bot_follow(twitter_object,tweet['user']['screen_name'])
					print "followed user -> " , tweet['user']['screen_name']
					TwitterAPI.bot_retweet(twitter_object,tweet['id'])
					print "retweeted the tweet_id -> " , tweet['id']
					TwitterAPI.bot_like(twitter_object,tweet['id'])
					print "liked the tweet_id -> " , tweet['id']
					TwitterAPI.bot_reply(twitter_object,'@'+tweet['user']['screen_name']+' '+message,tweet['id'])
					print "replied to user -> " , tweet['user']['screen_name'], " with this message ->", message

				## The below bot_chat functs sends a DM.. will only work if the person is also following you
					# TwitterAPI.bot_chat(twitter_object,message,tweet['user']['screen_name'])


				## pagination code for search endpoint.
				## search end point allows only 100 tweets per request.
				if 'next_results' not in tweets['search_metadata'] or len(tweets['statuses']) == 0:
					print "Completed the task...Exiting now!!"
					break
				else:
					new_paginate_older_attribute = tweets['search_metadata']['next_results'].split('&')[0].strip('?max_id=')
					paginate_older_attribute = str(new_paginate_older_attribute)

			else:
				print "Completed the task...Exiting now!!"
				break

		except Exception, e:
			print "Error: %s" % e
			##  sleep and try again
			time.sleep(random.randint(0,50))



## This is main function of the non steaming bot

def love_bot(screen_name = "",text_to_search = "",message="this is a bot"):
	print 'Initializing bot....'


	## Check if params are present
	if screen_name != None and screen_name != '':
		love_user_only(screen_name,message)
	elif text_to_search != "":
		love_tweets_with_message(text_to_search,message)



######################################################################################################################
########################### The Streaming functions of the bot #######################################################
def start_like_bot(screen_name = "",text_to_match= "" ,message= "This is a default message -- I am a bot"):

## Exiting if nothing is specified
	if screen_name == "" and text_to_match == "":
		print "Specify atleast one parameter.... exiting"
		exit()

## initializing the API keys
	api_key = TwitterAPI._get_api_auth_details()
	twitter_object_lookup = TwitterAPI._get_api_client(api_key)
	twitter_object = TwitterAPI._get_api_client_stream(api_key)

	track     = text_to_match
	follow 	  = screen_name

## Twitter Streaming API required user_id for 'follow'... So for the given screen_name, user_lookup end point is called to extract the user_id
	if follow != "":
		follow = TwitterAPI.bot_lookup(twitter_object_lookup,screen_name.lstrip('@'))

	while True:
		try:
			## if screen_name and hence the user_id is invalid
			if follow == False:
				print "invalid screen_name...exiting.."
				break
			else:
				## if both screen_name and text_to_search is specified
				if follow != "" and follow != None:
					iterator       = twitter_object.statuses.filter(follow = follow,track = track)
				else:
				## for only text_to_search is given
					iterator       = twitter_object.statuses.filter(track = track)

				print "iterating through all the steaming tweets for the given params"
				for tweet in iterator:

					TwitterAPI.bot_retweet(twitter_object_lookup,tweet['id'])
					print "retweeted the tweet_id -> " , tweet['id']
					TwitterAPI.bot_like(twitter_object_lookup,tweet['id'])
					print "liked the tweet_id -> " , tweet['id']
					TwitterAPI.bot_reply(twitter_object_lookup,'@'+ tweet['user']['screen_name'] +' '+ message,tweet['id'])
					print "replied to user -> " , tweet['user']['screen_name'], " with this message ->", message
					TwitterAPI.bot_tweet(twitter_object_lookup,message)
					print "tweeted with message -> " , message
				## uncomment the below 2 calls if you want to use them
					# TwitterAPI.bot_follow(twitter_object_lookup,screen_name)
				## chat will only work if the user is following you
					# TwitterAPI.bot_chat(twitter_object_lookup,message,screen_name)

		except Exception, e:
			print str(e)
			time.sleep(random.randint(0,30))

# start_like_bot(screen_name = 'yathshar',text_to_match = 'india',message = '#india just testing my new product')

def start_hate_bot(screen_name = "",text_to_match = "",message = "This is a default message -- I am a bot"):

## Exiting if nothing is specified
	if screen_name == "" and text_to_match == "":
		print "Specify atleast one parameter.... exiting"
		exit()

## initializing the API keys
	api_key = TwitterAPI._get_api_auth_details()
	twitter_object_lookup = TwitterAPI._get_api_client(api_key)
	twitter_object = TwitterAPI._get_api_client_stream(api_key)
	track     = text_to_match
	follow 	  = screen_name

## Twitter Streaming API required user_id for 'follow'... So for the given screen_name, user_lookup end point is called to extract the user_id
	if follow != "":
		follow = TwitterAPI.bot_lookup(twitter_object_lookup,screen_name.lstrip('@'))

	while True:
		try:
			## if screen_name and hence the user_id is invalid
			if follow == False:
				print "invalid screen_name...exiting.."
				break
			else:
				print track,follow
				if follow != "" and follow != None:
					iterator       = twitter_object.statuses.filter(follow = follow,track = track)
				else:
				## for only text_to_search is given
					iterator       = twitter_object.statuses.filter(track = track)

				print "iterating through all the steaming tweets for the given params"
				for tweet in iterator:

## Its nearly impossible that the streaming tweets will be already liked/retweeted by the user, therefore
## first I am liking/retweeting the tweet and then unliking and unretweeting it

					TwitterAPI.bot_retweet(twitter_object_lookup,tweet['id_str'])
					print "retweeted the tweet_id -> " , tweet['id']

					TwitterAPI.bot_unretweet(twitter_object_lookup,tweet['id_str'])
					print "unretweeted the tweet_id -> " , tweet['id']


					TwitterAPI.bot_like(twitter_object_lookup,tweet['id_str'])
					print "liked the tweet_id -> " , tweet['id']
					TwitterAPI.bot_unlike(twitter_object_lookup,tweet['id_str'])
					print "unliked the tweet_id -> " , tweet['id']

					TwitterAPI.bot_reply(twitter_object_lookup,'@'+ tweet['user']['screen_name'] +' '+ message,tweet['id_str'])
					print "replied to user -> " , tweet['user']['screen_name'], " with this message ->", message


				## uncomment the below 2 calls if you want to use them
					# TwitterAPI.bot_unfollow(twitter_object_lookup,screen_name)

				## chat will only work if the user is following you
					# TwitterAPI.bot_chat(twitter_object_lookup,message,screen_name)

		except Exception, e:
			print str(e)
			traceback.print_exc()
			time.sleep(random.randint(0,30))

# start_hate_bot(screen_name = 'yathshar',text_to_match = 'euro',message = '#india just testing my new product')



def start_conditional_bot(screen_name = "",text_to_match = "",message = "This is a default message -- I am a bot"):

## Exiting if nothing is specified
	if screen_name == "" and text_to_match == "":
		print "Specify atleast one parameter.... exiting"
		exit()

## initializing the API keys
	api_key = TwitterAPI._get_api_auth_details()
	twitter_object_lookup = TwitterAPI._get_api_client(api_key)
	twitter_object = TwitterAPI._get_api_client_stream(api_key)
	track     = text_to_match
	follow 	  = screen_name

## Twitter Streaming API required user_id for 'follow'... So for the given screen_name, user_lookup end point is called to extract the user_id
	if follow != "":
		follow = TwitterAPI.bot_lookup(twitter_object_lookup,screen_name.lstrip('@'))

	print "Starting streaming!!"
	while True:
		try:
			iterator = twitter_object.statuses.sample()


			for tweet in iterator:
## Checking if the tweet is not deleted
				if 'delete' not in tweet:
				## if the author of the tweets matches the given screen_name then like the tweet
					if tweet['user']['screen_name'] == str(screen_name.lstrip('@')):
						TwitterAPI.bot_like(twitter_object_lookup,tweet['id'])
						print "liked the tweet_id -> " , tweet['id']

					## if the text of the tweets contains the given text then reply and retweet and follow
					if text_to_match in tweet['text']:
						TwitterAPI.bot_reply(twitter_object_lookup,'@'+tweet['user']['screen_name']+' '+message,tweet['id'])
						print "replied to user -> " , tweet['user']['screen_name'], " with this message ->", message

						TwitterAPI.bot_retweet(twitter_object_lookup,tweet['id'])
						print "retweeted the tweet_id -> " , tweet['id']

						TwitterAPI.bot_follow(twitter_object_lookup,screen_name)
						print "followed the user -> " , tweet['user']['screen_name']

					## will work only if the user is following you
						# TwitterAPI.bot_chat(twitter_object_lookup,message,tweet['user']['screen_name'])

				## if the user is tweeting with the word 'hate' then reply 'please don't spread hate
					if 'hate' in tweet['text']:
						TwitterAPI.bot_reply(twitter_object_lookup,'@'+tweet['user']['screen_name']+' Please dont spread hate',tweet['id'])
						print "replied to user -> " , tweet['user']['screen_name'], " with this message ->", message
						# TwitterAPI.bot_unlike(twitter_object_lookup,tweet['id'])

				## if there are more than 1 hashtags, then takes the 1st hashtag and tweet with the given message
					if len(tweet['entities']['hashtags']) > 0:
						hashtags = tweet['entities']['hashtags'][0]['text']
						TwitterAPI.bot_tweet(twitter_object_lookup,'#'+hashtags + ' '+ message)
						print "tweeted with message -> " , '#'+hashtags + ' '+ message

						TwitterAPI.bot_retweet(twitter_object_lookup,tweet['id'])
						print "retweeted the tweet_id -> " , tweet['id']


		except Exception, e:
			print str(e)
			traceback.print_exc()
			print 'gooing to sleep'
			time.sleep(10)
			print 'woke up!!'


# start_conditional_bot('yathshar','pokemon','pokemonGo!!')
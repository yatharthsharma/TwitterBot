from twitter import * # https://github.com/sixohsix/twitter
import csv
import random

def _get_api_auth_details():
	auth_details = list(csv.reader(open('api_keys.csv')))

	del(auth_details[0])

	random_auth_detail = random.choice(auth_details)

	api_key = {}

	api_key['api_key'] = random_auth_detail[0].strip()
	api_key['api_secret'] = random_auth_detail[1].strip()
	api_key['access_token'] = random_auth_detail[2].strip()
	api_key['access_token_secret'] = random_auth_detail[3].strip()

	return api_key

def _get_api_client(api_key):
	api = Twitter(auth = OAuth(
		str(api_key['access_token']),
		str(api_key['access_token_secret']),
		str(api_key['api_key']),
		str(api_key['api_secret'])))

	return api

def _get_api_client_stream(api_key):
	api = TwitterStream(auth = OAuth(
		str(api_key['access_token']),
		str(api_key['access_token_secret']),
		str(api_key['api_key']),
		str(api_key['api_secret'])))

	return api


## retweet ##
def bot_retweet(twitter_object,id):
	if id != "" and id != None:
		twitter_object.statuses.retweet(_id = id)
	else:
		return "ID cannot be blank"

## unretweet ##
def bot_unretweet(twitter_object,id):
	if id != "" and id != None:
		twitter_object.statuses.unretweet(_id = id)
	else:
		return "ID cannot be blank"

## delete a tweet ##
def bot_delete(twitter_object,id):
	if id != "" and id != None:
		twitter_object.statuses.destroy(_id = id)
	else:
		return "ID cannot be blank"

## reply to a tweet ##
def bot_reply(twitter_object,message,id):

	# message should contain @username
	if id != None:
		twitter_object.statuses.update (status=message,in_reply_to_status_id=id)
	else:
		return "Id of the tweet not specified"

## tweet ##
def bot_tweet(twitter_object,message):

	if message != "" and message != None:
		twitter_object.statuses.update (status=message)
	else:
		return "message cannot be blank!!!"

## send a DM to a user ##
def bot_chat (twitter_object,message,screen_name,user_id=None):

	if message != "" and message != None:
		if user_id == None and screen_name != None:
			twitter_object.direct_messages.new (text= message,screen_name = screen_name)
		elif screen_name == None and user_id != None:
			twitter_object.direct_messages.new (text= message,user_id = user_id)
		elif screen_name != None and user_id != None:
			twitter_object.direct_messages.new (text= message,user_id = user_id,screen_name=screen_name)
		else:
			return "Either screen_name or user_id should be there"
	else:
		return "message and cannot be blank!!!"

## delete the DM ##
def bot_delete_chat (twitter_object,id):
	if id != "" and id != None:
		twitter_object.direct_messages.new (id= id)

## follow a user ##
def bot_follow(twitter_object,screen_name,user_id=None):
	if user_id == None and screen_name != None:
		twitter_object.friendships.create (follow = True, screen_name = screen_name)
	elif screen_name == None and user_id != None:
		twitter_object.friendships.create (follow = True, user_id = user_id)
	elif screen_name != None and user_id != None:
		twitter_object.friendships.create (follow = True, user_id = user_id,screen_name=screen_name)
	else:
		return "Either screen_name or user_id should be there"

## unfollow a user ##
def bot_unfollow(twitter_object,screen_name,user_id=None):
	if user_id == None and screen_name != None:
		twitter_object.friendships.destroy ( screen_name = screen_name)
	elif screen_name == None and user_id != None:
		twitter_object.friendships.destroy ( user_id = user_id)
	elif screen_name != None and user_id != None:
		twitter_object.friendships.destroy ( user_id = user_id,screen_name=screen_name)
	else:
		return "Either screen_name or user_id should be there"

## like a tweet ##
def bot_like(twitter_object,id):
	if id != "" and id != None:
		twitter_object.favorites.create(_id = id)
	else:
		return "ID cannot be blank"



## unlike the tweet ##
def bot_unlike(twitter_object,id):
	if id != "" and id != None:
		twitter_object.favorites.destroy(_id = id)
	else:
		return "ID cannot be blank"


def bot_lookup(twitter_object,screen_name):
	if screen_name != "" and screen_name != None:
		try:

			user_obj = twitter_object.users.lookup(screen_name = screen_name)
			return user_obj[0]['id']

		except Exception, e:
			return False

	else:
		return "ID cannot be blank"

def get_user_tweets(twitter_object,screen_name,paginate_older_attribute):

	if paginate_older_attribute == '0':
		user_tweets = twitter_object.statuses.user_timeline(
		screen_name = screen_name,
		count = 200,
		include_entities = True)
	else:
		user_tweets = twitter_object.statuses.user_timeline(
			screen_name = screen_name,
			count = 200,
			max_id= paginate_older_attribute,
			include_entities = True)
	return user_tweets

def get_tweets(twitter_object, search_phrase, paginate_older_attribute):

	if paginate_older_attribute == '0':
		statuses = twitter_object.search.tweets(
			q = search_phrase,
			count = 100,
			include_entities = True)
	else:
		statuses = twitter_object.search.tweets(
			q = search_phrase,
			max_id = paginate_older_attribute,
			count = 100,
			include_entities = True)

	return statuses




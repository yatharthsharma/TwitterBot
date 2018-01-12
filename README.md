# TwitterBot

A Python bot that automates several actions on Twitter

# Dependencies

- You need to install this twitter (https://github.com/sixohsix/twitter) library.
   - sudo pip install twitter
- You will also need to create an app account on https://dev.twitter.com/apps using your Twitter account
 - Modify the settings for that app account to allow Read, write, and direct messages
 - Python 2.7 

# Functionalities

TwitterBot can be used to automatically do the following actions:

1. Basic Functionality:
 - tweet (on your behave)
 - delete your tweet
 - like a tweet
 - unlike a tweet (dislike a tweet)
 - retweet a tweet
 - unretweet a tweet (undo retweet)
 - reply to a tweet
 - reply to all the tweets of a user
 - reply to all the tweets matching a text
 - Send a DM (will only work if the user is following you & your app has direct messages permissions)
 - delete a DM
 - follow a user
 - unfollow a user
2. Advanced Functionalities
 - Stream data using twitterStream API and perform the basic functionalities (mentioned above) based on a criteria.
 - Use twitter REST API to get tweets done in past and perform the basic functionalities based on a criteria.


# Code structure
 - api_access_object -> twitter_api.py contains all the twitter API calls.
 - api_key.csv contains the twitter API keys (I have not pushed my own API key, you are required to add your own API key in this file).
 - twitter_bot.py contains the 4 advanced functionalities of TwitterBot

# functions description:
1. functions in twitter_api.py are self explanatory.
2. functions in twitterBot.py: Functions using TwitterStreaming API (This is used to interact with live tweets).
 - start_like_bot(screen_name,text_to_match,message) -> The use of this bot is to like/retweet/reply to all the tweets retrieved from TwitterStreaming API (Tweets are retrieved based on the input parameters).
 - start_hate_bot(screen_name,text_to_match,message) -> The use of this bot is to do the reverse of the start_like_bot function i.r dislike/unretweets the tweets coming from TwitterStreaming API
 - start_conditional_bot(screen_name,text_to_match,message) -> This performs different actions on the tweets retrieved from twitterStreamin API based on pre-defined conditions as follows.
    - if the author of the tweet is same as the input screen_name, then it likes the tweet.
    - if the text of the tweets contains the given input text_to_match, then it replies and retweets the tweet + follows the user.
    - if there is a tweet with the word 'hate in it, then it sends a 'please don't spread hate' reply to the tweet.
    - if there are more than 1 hashtags in the tweet, then takes the 1st hashtag and tweets using the hashtag and the input message + retweets the tweet.
3. functions in twitterBot.py: Functions using REST API (This is used to interact with old tweets).
  - love_user_only(screen_name,message) -> It collects all the old tweets of a user with the given input screen_name and likes/retweets/replies to the tweet + follows the user + DM the user.
  - love_tweets_with_message(text_to_search, message) -> It collects all the old tweets matching the given input text and likes/retweets/replies to the tweet + follows the user.
  - love_bot(screen_name,text_to_search,message): parent function for the above 2 functions.

# How to run and Usage

 **twitterStreaming bot:**

from twitterBot import *

1. start_like_bot(screen_name = 'yathshar') -> collects all the **live** tweets of the input user and performs the actions specified above in the function description.
2. start_like_bot(screen_name = 'yathshar',message = "hi") ->  collects all the **live** tweets of the input user and performs the actions specified above in the function description and **replies to the tweet using the input message**.
3. start_like_bot(text_to_match = 'india') -> collects all the **live** tweets based on the given input parameter **text_to_match** and performs the actions specified above.
4. start_like_bot(screen_name = 'yathshar',text_to_match = 'india') -> It performs an **OR** search, collecting live tweets containing either tweets done by the author as mentioned in the input param (screen_name) or tweets containing the text as specified in the input param (text_to_match).

**similarly for start_hate_bot**

5. start_hate_bot(screen_name = 'yathshar') -> collects all the **live** tweets of the input user and performs the actions specified above in the function description.
6.  start_hate_bot(screen_name = 'yathshar',message = "hi") ->  collects all the **live** tweets of the input user and performs the actions specified above in the function description and **replies to the tweet using the input message**.
7. start_hate_bot(text_to_match = 'india') -> collects all the **live** tweets based on the given input parameter.
8. start_hate_bot(screen_name = 'yathshar',text_to_match = 'india') -> It performs an **OR** search, collecting live tweets containing either tweets done by the author as mentioned in the input param (screen_name) or tweets containing the text as specified in the input param (text_to_match).

9. start_conditional_bot(screen_name = 'yathshar',text_to_match = 'pokemon',message = 'pokemonGo!!') -> It performs an **OR** search, collecting live tweets containing either tweets done by the author as mentioned in the input param (screen_name) or tweets containing the text as specified in the input param (text_to_match). After collecting the tweets, it performs the actions mentioned in the function description above.

**RESTAPI bot: **

1. love_bot(screen_name ='yathshar') ->  collects all the **old** tweets of the input user and performs the actions specified above in the function description.
2. love_bot(text_to_search= "india") -> collects all the **old** tweets based on the given input parameter **text_to_match** and performs the actions specified above.

#Questions

If you have any questions regarding this drop me a mail - yatharth.sharma@gmail.com

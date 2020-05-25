import tweepy
import logging
from config import create_api
import time
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class BobadaStreamListener(tweepy.StreamListener):
    def __init__(self, api, bobo_list):
        self.api = api
        self.bobo_list = bobo_list
        self.last_new_friends_check = time.time()

    def on_status(self,tweet):
        logger.info("Processing tweet id %d" % (tweet.id))

        #Check if tweet author is in list
        if tweet.author.id_str not in self.bobo_list:
            logger.info("Tweet was authored by %s" %(tweet.author.screen_name))
            return self.check_new_follows() 
        
        # If it's a reply, do nothing
        if tweet.in_reply_to_status_id is not None:
            logger.info("Tweet was reply")
            return self.check_new_follows() 
        
        # If it's a retweet, do nothing
        if hasattr(tweet, 'retweeted_status'):
            logger.info("Tweet was retweet")
            return self.check_new_follows() 

        # Reply
        try:
            username = tweet.author.screen_name
            message = "@%s Dale bobo" %username
            logger.info("Replying to %s" % (username))
            new_tweet = self.api.update_status(status=message, in_reply_to_status_id=tweet.id)
            # Retweet response
            if not new_tweet.retweeted:
                new_tweet.retweet()
            
        except tweepy.TweepError as e:
            logger.error("Error on reply and retweet: %s" % (e.message[0]['message']), exc_info=True)
 
        return self.check_new_follows() 
    
    def on_error(self, status):
        logger.error(status,exc_info=True)
        
    def check_new_follows(self):
        # Check new follows every 5 minutes
        # This is to avoid reaching rate limit for this stream
        # See https://developer.twitter.com/en/docs/basics/rate-limiting
        new_time = time.time()
        elapsed = new_time - self.last_new_friends_check
        if (elapsed < 5*60):
            return True
        else:
            new_follows_id = [friend.id_str for friend in tweepy.Cursor(self.api.friends).items()]
            self.last_new_friends_check = time.time()
            return set(new_follows_id) == set(self.bobo_list)
        
def reply_al_bobo(api):
    
    # Bobo list is followed people
    bobo_list= [friend.id_str for friend in tweepy.Cursor(api.friends).items()]
    
    bobada_listener = BobadaStreamListener(api, bobo_list)    
    bobada_stream = tweepy.Stream(api.auth, bobada_listener)
    
    try:
        bobada_stream.filter(follow=bobo_list)
    except Exception as e:
        logger.error("Error on stream.filter", exc_info=True)

def bobo_names_to_id(api, bobo_list_names):
    bobo_list_id = []
    for bobo in bobo_list_names:
        try:
            bobo_user = api.get_user(bobo)
            bobo_user_id = bobo_user.id_str
            bobo_list_id.append(bobo_user_id)
        except tweepy.TweepError as e:
            logger.error("Error on bobo name %s: %s" % (bobo,e.message[0]['message']))
            raise
        
    return bobo_list_id


def main(bobo_list):
    api = create_api()

    if bobo_list is not None:
        # Convert bobo username to id
        bobo_list_id = bobo_names_to_id(api,bobo_list)
    
        #Follow bobo if not following
        relationships = api.lookup_friendships(bobo_list_id)
        for relationship in relationships:
            if not relationship.is_following:
                try:
                    logger.info("Following %s" %(relationship.screen_name))
                    api.create_friendship(relationship.screen_name)
                except tweepy.TweepError as e:
                    logger.error("Error on follow: %s" % (e.message[0]['message']), exc_info=True)

    while True:
        reply_al_bobo(api)
        logger.info("Waiting...")
        time.sleep(60)
        logger.info("OK go")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot that replies <<Dale bobo>> to the list of people it follows.")
    parser.add_argument("-b", "--bobo_list", metavar="bobo_list", type=str, required=False,
                        default=None, nargs='+', action="store",
                        help="list of bobo usernames you want the bot to follow and reply to. If not given, it only replies to the ones it follows")
    
    args = parser.parse_args()
    bobo_list =  args.bobo_list
    
    main(bobo_list)

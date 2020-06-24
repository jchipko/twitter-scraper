import settings
import tweepy
import dataset
from sqlalchemy.exc import ProgrammingError
import json
from clean_text import deEmojify

db = dataset.connect(settings.CONNECTION_STRING)


class MyStreamListener(tweepy.StreamListener):
    '''
    Override tweepy.StreamListener to add logic to on_status
    '''
    
    def on_status(self, status):
        '''
        Extract info from tweets
        '''
        
        if status.retweeted:
            return True
        # Extract attributes from each tweet
        id_str = status.id_str
        created_at = status.created_at
        name = status.user.screen_name
        text = deEmojify(status.text)    # Pre-processing the text  
        
        user_created_at = status.user.created_at
        user_location = deEmojify(status.user.location)
        geo = status.geo
        user_description = deEmojify(status.user.description)
        user_followers_count =status.user.followers_count
        longitude = None
        latitude = None
        coords = status.coordinates
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
            
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        
        print(status.text)
        print("Long: {}, Lati: {}".format(longitude, latitude))
        
        table = db[settings.TABLE_NAME]
        try:
            table.insert(dict(
                user_description=user_description,
                user_location=user_location,
                coordinates=coords,
                longitude=longitude,
                latitude=latitude,
                text=text,
                geo=geo,
                user_name=name,
                id_str=id_str,
                created=created_at,
                retweet_count=retweet_count,
                favorite_count=favorite_count
            ))
        except ProgrammingError as err:
            print(err)
    
    
    def on_error(self, status_code):
        '''
        Stop scraping data before exceeding API rate limits.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False

auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)

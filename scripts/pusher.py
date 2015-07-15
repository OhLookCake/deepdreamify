import praw
import urllib
import pyimgur
import logging
from credentials import *



def post_to_imgur(imagepath, titletexti, album='WHOXh'):
    imgurposter = logging.getLogger('imgurpost')
    imgurposter.info('Imgur posting initiated')

    CLIENT_ID = IMGUR_CLIENT_ID,
    CLIENT_SECRET = IMGUR_CLIENT_SECRET

    im = pyimgur.Imgur(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    imgurposter.info('Connected to imgur')
    im.exchange_pin(IMGUR_PIN)
    imgurposter.info('Pin exchanged')

    image = im.upload_image(path=imagepath, title=titletext, description=titletext, album=album)
    imgurposter.info('Image uploded')
    imgurposter.info(image.link)

    im.refresh_access_token()
    print(image.link)


def post(image):
    '''
    Posts the passed imgur link to reddit
    '''

    #CONFIG
    postto = 'sometimesitestthings'

    fetchlogger = logging.getLogger('fetcher')
    timestamp = str(int(time.time()))
    fetchlogger.info('Fetcher initiated')
    fetchlogger.info('Timestamp: ' + timestamp)

    # CONFIGURATION
    r = praw.Reddit(user_agent = user_agent)
    subreddit = r.get_subreddit(postto)

    r.login(REDDIT_USERNAME, REDDIT_PASS)













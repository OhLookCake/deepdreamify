import praw
import urllib
import pyimgur
import pickle
import logging
from credentials import *



def post_to_imgur(imagepath, titletext, descriptiontext, album='WHOXh'):
    '''
    Posts the image provided to imgur album with the preconfigured user
    The im instance is loaded from a serialized object, as stored by 
    the authentication script
    '''
    imgurposter = logging.getLogger('imgurpost')
    imgurposter.info('Imgur posting initiated')

    #CLIENT_ID = IMGUR_CLIENT_ID
    #CLIENT_SECRET = IMGUR_CLIENT_SECRET

    #im = pyimgur.Imgur(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    #imgurposter.info('Connected to imgur')
    #im.exchange_pin(IMGUR_PIN)
    #imgurposter.info('Pin exchanged')

    im = pickle.load(open('records/im.ser', 'rb' ))
    im.refresh_access_token()

    image = im.upload_image(path=imagepath, title=titletext, description=descriptiontext, album=album)
    imgurposter.info('Image uploded')
    imgurposter.info(image.link)

    return str(image.link)


def post_to_reddit(url, title, link_to_original, postto='deepdreamified'):
    '''
    Posts the passed imgur link to reddit
    '''

    rpostlogger = logging.getLogger('redditpost')
    rpostlogger.info('Reddit Post initiated')

    # CONFIGURATION
    r = praw.Reddit(user_agent = user_agent)
    subreddit = r.get_subreddit(postto)

    r.login(REDDIT_USERNAME, REDDIT_PASS)

    newsubmission = r.submit(subreddit=postto, title=title, url=url, resubmit=True)
    rpostlogger.info('Submitted to reddit at ', str(newsubmission.permalink))
    newsubmission.add_comment('Original post [here](' + link_to_original  +')')
    rpostlogger.info('Comment (link to original) added')

    return newsubmission.permalink



def comment_on_post(post_id, comment):
      commenterlogger = logging.getLogger('commenter')

      r = praw.Reddit(user_agent = user_agent)
      r.login(REDDIT_USERNAME, REDDIT_PASS)

      submission = r.get_submission(submission_id=post_id)
      submission.add_comment(comment)
      commenterlogger.info('Comment posted')








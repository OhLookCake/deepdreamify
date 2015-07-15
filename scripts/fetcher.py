import praw
import urllib
import time
import os
import re
import logging
from urllib2 import urlopen
from credentials import *
from bs4 import BeautifulSoup


def fetch(fetchfrom='pics', numfetch=5):

    
    fetchlogger = logging.getLogger('fetcher')
    timestamp = str(int(time.time()))
    fetchlogger.info('Fetcher initiated')
    fetchlogger.info('Timestamp: ' + timestamp)

    # CONFIGURATION
    r = praw.Reddit(user_agent = user_agent)
    subreddit = r.get_subreddit(fetchfrom)

    recordsfile = 'records/done.txt'

    #GET list of posts already processed
    postsdone = []
    if not os.path.isfile(recordsfile):
        postsdone = []
    else:
        with open(recordsfile, 'r') as donefile:
            postsdone = donefile.read().split('\n')
            postsdone = filter(None, postsdone)

    print postsdone


    #FETCH
    imagelist = []

    ctr = 0
    for submission in subreddit.get_hot(limit = numfetch):
        ctr+=1
        fetchlogger.info(ctr)
        fetchlogger.info('Title: ' + submission.title)
        fetchlogger.info('    Id: ' + submission.id)
        if submission.id in postsdone:
            fetchlogger.info('    Action: None; Already done')
            continue
        else:
            print 'notfound', submission.id
            imageurl = submission.url
            fetchlogger.info('    ' + imageurl)

            imgurUrlPattern = re.compile(r'http[s]*://imgur.com/[^\.\/]+$')
            if imgurUrlPattern.match(imageurl):
	        #convert to direct link. http://imgur.com/ABC -> http://i.imgur.com/ABC.jpg
	        soup = BeautifulSoup(urlopen(imageurl), "lxml")
	        matches = soup.select('div.image img')
	        if len(matches) > 0 and matches[0].has_attr('src'):
	            imageurl = 'https:' + matches[0]['src']
                imageurl = imageurl.split('?')[0]
                fetchlogger.info('    Redirecting to ' +  imageurl)
            filename = imageurl.split('/')[-1]

            fetchlogger.info('    ' + imageurl)
            if filename.split('.')[-1].lower() in ['jpg', 'jpeg', 'bmp', 'png', 'tif', 'tiff']:
                urllib.urlretrieve(imageurl, 'images/' + filename)
                imagelist.append([filename, submission.id])
                fetchlogger.info('    Action: Downloaded')
            else:
                fetchlogger.warn('    Action: Ignored; Not an image url')

    return imagelist



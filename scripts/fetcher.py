import praw
import urllib
import time
import os
import re
from urllib2 import urlopen
from bs4 import BeautifulSoup


# PARAMETERS
fetchfrom = 'pics' 	#subreddit to fetch from
numfetch = 25   		#number of (top) hot posts to fetch


# CONFIGURATION
user_agent = ('picsfetcher 0.1')
r = praw.Reddit(user_agent = user_agent)
subreddit = r.get_subreddit(fetchfrom)


#FETCH
imagelist = []
timestamp = str(int(time.time()))
print timestamp

for submission in subreddit.get_hot(limit = numfetch):
    print('Title: ' + submission.title)

    imageurl = submission.url 
    print(imageurl)

    imgurUrlPattern = re.compile(r'http[s]*://imgur.com/[^\.\/]+$')
    if imgurUrlPattern.match(imageurl):
        #convert to direct link. http://imgur.com/ABC -> http://i.imgur.com/ABC.jpg
        soup = BeautifulSoup(urlopen(imageurl), "lxml")
        matches = soup.select('div.image img')
        if len(matches) > 0 and matches[0].has_attr('src'):
            imageurl = 'https:' + matches[0]['src']
            print('Redirecting to ' +  imageurl)
    filename = imageurl.split('/')[-1]

    print(imageurl)
    if filename.split('.')[-1].lower() in ['jpg', 'jpeg', 'bmp', 'png', 'tif', 'tiff']:
        urllib.urlretrieve(imageurl, 'images/' + filename)
        imagelist.append(filename)
        print('Done')
    else:
        print('Not an image url')








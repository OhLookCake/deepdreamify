import logging
from fetcher import *
from dreamifyinterface import *
from pusher  import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='records/main.log',
                    filemode='a')

##### Print logs to screen

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

####

logging.info('Started new instance')
logging.info('Calling Fetcher')

#1. Fetch
imagelist = fetch(fetchfrom='pics', numfetch=25)
logging.info('Fetched imagelist')
print imagelist

ctr = 0
logging.info('Iterating over images:')
for image in imagelist:
    '''
    [filename, submission.id, submission.title, filemaxdim]
    image[0]: filename/imgurname - used to refer to file name on disk (includes extension)
    image[1]: submissionid - used to keep record of which submission is processed
    image[2]: submission title - used to give title to post on imgur, reddit
    image[3]: max file dimension - used to decide if resizing is needed
    image[4]: permalink - used to post the comment to posted image
    '''

    ctr+=1
    logging.info(str(ctr) + ': ' + str(image[0]) + ' - ' + image[1] + ' - ' + image[4])
    # 2. Deepdreamify
    ddfiedfile = 'records/ddfied.txt'
    postsddfied = []
    if not os.path.isfile(ddfiedfile):
        postsddfied = []
    else:
        with open(ddfiedfile, 'r') as donefile:
            postsddfied = donefile.read().split('\n')
            postsddfied = filter(None, postsddfied)
    if image[1] not in postsddfied:
        if image[2] > 800:
            dreamify('images/raw/'+image[0], resize_newsize=800)
        else:
            dreamify('images/raw/'+image[0])
    
        with open(ddfiedfile, 'a') as donefile:
            donefile.write(image[1]+'\n')
    else:
        logging.info('Already Dreamified; Skipping Dreamification process')

    # 3. Upload dreamified image to imgur
    imagetitle = '.'.join(image[0].split('.')[:-1])
    imgurlink = post_to_imgur('images/processed/'+imagetitle+'.jpg', titletext='Deep-dream-ified: ' + image[2], descriptiontext = '')
    logging.info('Imgur link: ' + imgurlink)

    # 4. Post on reddit, add comment (link to original post)
    rpostedfile = 'records/rposted.txt'
    postsrposted = {}
    redditlink = ''
    if not os.path.isfile(rpostedfile):
        postsrposted = {}
    else:
        with open(rpostedfile, 'r') as donefile:
            postsandurls = donefile.read().split('\n')
            postsandurls = filter(None, postsandurls)

            postsrposted = {pnu.split('\t')[0]:pnu.split('\t')[1] for pnu in postsandurls}
    if image[1] not in postsrposted:
        redditlink = post_to_reddit(imgurlink, title='Deep-dream-ified: '+image[2], link_to_original=image[4], postto='deepdreamified')
        with open(rpostedfile, 'a') as donefile:
            donefile.write(image[1]+'\t' + str(redditlink)  +'\n')
    else:
        logging.info('Already posted to reddit; Skipping posting to reddit')
        redditlink = postsrposted[image[1]]


    # 5. Comment on original post
    ddinfolink = 'https://www.reddit.com/r/deepdreamified/comments/3di8qm/faq_aka_wtf_is_going_on_here/'
    commenttext = "Hi! I'm a dreamification bot, and I've deep-dream-ified your post [here](" + redditlink + ")  \n\nTo learn more about what this is, see [here](" + ddinfolink + ")   \n\nHope you enjoy the dreamified post, but if, for some reason, you're uncomfortable with this, drop me a PM, and I'll take it off."
    comment_on_post(image[1], commenttext)

    with open('records/done.txt', 'a') as donefile:
        donefile.write(image[1]+'\n')


logging.info('COMPLETE')
logging.info('**************************************')









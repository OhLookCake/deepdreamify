import webbrowser
import pyimgur
import pickle
from credentials import *

CLIENT_ID = IMGUR_CLIENT_ID
CLIENT_SECRET = IMGUR_CLIENT_SECRET

im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)
auth_url = im.authorization_url('pin')
print(auth_url)
#webbrowser.open(auth_url)
pin = raw_input('Enter pin: ')
im.exchange_pin(pin)

pickle.dump(im, open('records/im.ser', 'wb' ) )



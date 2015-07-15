import webbrowser
import pyimgur
from credentials import *

CLIENT_ID = IMGUR_CLIENT_ID
CLIENT_SECRET = IMGUR_CLIENT_SECRET

im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)
auth_url = im.authorization_url('pin')
webbrowser.open(auth_url)
pin = raw_input("What is the pin? ")

im.exchange_pin(pin)
im.create_album("An authorized album", "Cool stuff!")

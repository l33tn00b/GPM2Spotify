#python > v3
#doooh.
#this is ugly.
#but it is meant to be a quick hack for getting necessary permissions for playlist import

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
import sys
from bottle import route, run, request
from spotipy import oauth2
import pprint


#prepare pretty printing (debug)
pp = pprint.PrettyPrinter(indent=2)

#set spotify username
username = ""
#client id and client secret for spotify
clientid = ""
clientsecret = ""

#you need to generate these via the spotify developer console: developer.spotify.com
#do not forget to set a callback url for your application!
#which needs to be exactly the same as below (including port and http:// or https://)
#if your browser displays "INVALID_CLIENT: Invalid redirect URI" after trying the authorization
#you need to check the callback url in the developer console.
    
#we need two scopes:
#user-read-private for country data (so we may leave out unavailable versions)
#user-modify-private for creating playlists
scope = 'playlist-modify-private,user-read-private'


#create credetial manager instance
client_credentials_manager = SpotifyClientCredentials(client_id=clientid,
                                                      client_secret=clientsecret)
#create spotify instance with above credentials manager
#spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

token = spotipy.util.prompt_for_user_token(username,scope,client_id=clientid,client_secret=clientsecret,
                                   redirect_uri='http://localhost/')
if token:
    spotify = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)
    sys.exit()

cuser = spotify.current_user()
print(cuser)
#sys.exit()

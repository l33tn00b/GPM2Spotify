#python > v3
#doooh.
#this is ugly.
#but it is meant to be a quick hack for getting google play playlists (exported to json, e.g. via gmusicapi)
#transferred to spotify.
#we'll load the google playlist and search spotify for results with regard to the
#combination of artist and song title.
#if there is one result, we'll just add that
#if there is more than one result, we'll let the user choose which one to add

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
import sys
from spotipy import oauth2
import pprint


#prepare pretty printing (debug)
pp = pprint.PrettyPrinter(indent=2)

#set filename of google play playlist (dumped to json)
fname = "playlist_4.json"
#set spotify username
username = ""
#client id and client secret for spotify
#you need to generate these via the spotify developer console: developer.spotify.com
#do not forget to set a callback url for your application!
clientid = ""
clientsecret = ""

#we need two scopes:
#user-read-private for country data (so we may leave out unavailable versions)
#user-modify-private for creating playlists
scope = 'playlist-modify-private,user-read-private'




#cut and paste auth variant
###create credetial manager instance
client_credentials_manager = SpotifyClientCredentials(client_id=clientid,
                                                      client_secret=clientsecret)
#create spotify instance with above credentials manager
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

print("prompt for user token")
token = spotipy.util.prompt_for_user_token(username,scope,client_id=clientid,client_secret=clientsecret,
                                   redirect_uri='http://localhost/')
if token:
    spotify = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)
    sys.exit()
print("Do OAuth2...")
token = util.oauth2.SpotifyClientCredentials(client_id=clientid, client_secret=clientsecret)
#print("Token Object: " + str(token))

cache_token = token.get_access_token()
#print("Cache Token: " + str(cache_token))

#get user info to determine user's market
#some songs may not be available in certain markets
cuser = spotify.current_user()
#print(cuser)

#get google play music playlist from file
with open(fname, 'r', encoding='utf-8') as f:
    #read source (=google) playlist
    gplaylist = json.load(f)
    #create spotify playlist with currently signed on user's id
    #copy description and name from google playlist
    #for reasons of privacy we keep it private. you may change this via spotify's app/web interface at any time
    result = spotify.user_playlist_create(cuser['id'], gplaylist['name'], public=False)
    print("Created Playlist: ")
    pp.pprint(result)
    #make new list for spotify playlist
    newplaylist = []
    print("Number of elements in original playlist: " + str(len(gplaylist["tracks"])))
    numelems = len(gplaylist["tracks"])
#keep track of skipped songs
skiplist = []
#number of items processed
currelem = 0
#walk through playlist
for elem in gplaylist["tracks"]:
        currelem = currelem + 1
        print("******************************************************************************")
        print("Item " + str(currelem) + " of " + str(numelems))
        #display current item from googe playlist
        if "track" in elem:
            try:
                print("Song from Google Playlist: " + elem["track"]["artist"] + " - " + elem["track"]["title"])
            except:
                print("There was an error accessing song data from the original playlist.")
                pp.pprint(elem)
                break
            #search spotify for results
            print("Searching Spotify for that song...")
            try:
                results = spotify.search(q='artist:' + elem["track"]["artist"]+" track:"+elem["track"]["title"], type='track')
            except:
                print("There was an error searching for results.")
                pp.pprint(elem)
                break
            print("Number of Results: " + str(len(results["tracks"]['items'])))
             
            #tracks is a dict
            #items thereof are a list
            #each item of that list is a dict
            #print(type(results["tracks"]['items']))
            #number of items = number of versions of that song (from google playlist) found on spotify
            #print(results["tracks"]['items'])
            #print(json.dumps(results["tracks"]['items'], sort_keys=True, indent=4, separators=(',', ': ')))  
            #length counter
            lc = 0
            #make empty list for results
            reslist = []
            #did we find something?
            if len(results["tracks"]['items']) > 0:
                for item in results["tracks"]['items']:
                    #print(type(item))
                    #print(item)
                    #print(cuser['country'])
                    if cuser['country'] in item['album']['available_markets']:
                        lc = lc + 1
                        print("")
                        print("["+str(lc)+"]")
                        try:
                            print('Song Name: ' + item['name'])
                        except:
                            print("Sorry, seems like we have a song name that is not printable?")
                        try:
                            print('Album Name: ' + item['album']['name'])
                        except:
                            print("Sorry, seems like we have an album name that is not printable?")
                        try:
                            print('Album Date: ' + item['album']['release_date'])
                        except:
                            print("Sorry, seems like we have an album date that is not printable?")
                        #print(item)
                    else:
                        print("There is a result which is not available in your market. Skipping.")
                        addtrack = False
                        additem = None
                #print all songs found so as to let user choose...
                if lc > 1:
                    #more than one result. let user choose which one to add.
                    my_input = input('Choose version (by number): ')
                    #is it a number?
                    try:
                        number=int(my_input)
                        addtrack = True
                        additem = results['tracks']['items'][number]
                    except ValueError:
                        print ("Not a number. Must type a number. Skipping.")
                        addtrack = False
                        additem = None
                    if my_input == "q":
                        break
                #there was only one song
                else:
                    #add the only (one) result found to playlist
                    print('using the only result available.')
                    addtrack = True
                    additem = results["tracks"]['items'][0]
                #finally add the chosen song (or the only one available)
                if addtrack == True:
                    #pp.pprint(additem)
                    print("Adding ID " + additem['id'])
                    newplaylist.append(additem['id'])
                    #print(newplaylist)
            else:
                #print("No result. Retry with relaxed criteria (y/n)?")
                print("No result.")
                skiplist.append(elem["track"]["artist"]+" track:"+elem["track"]["title"])
        #wtf? there was no "track" key in our current elem
        #pas de bras, pas de chocolat
        else:
            #just do nothing and skip
            print("Skipped an entry from input file because it contained no track information.")
            if "trackId" in elem:
                print(elem["trackId"])
                skiplist.append(elem["trackId"])
#write collected/chosen tracks to playlist
spotify.user_playlist_add_tracks(cuser['id'], result['id'], tracks=newplaylist)
print("Skipped songs (no results on Spotify):")
pp.pprint(skiplist)

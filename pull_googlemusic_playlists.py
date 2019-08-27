#!/usr/bin/env python3
#basically, this is nothing but a slightly extended version of the
#example form the gmusicapi
#see https://unofficial-google-music-api.readthedocs.io/en/latest/reference/mobileclient.html
#dump all of the user's playlists to json files
#dump the user's entire library to a json file

import os
import argparse
import json
from gmusicapi import Mobileclient
import codecs
import random
import pprint 

#prepare pretty printing (debug)
pp = pprint.PrettyPrinter(indent=2)

G = Mobileclient()
playlist = "51d6ea84-a1db-4202-aa5b-afb0fcb7b94d"
content = "playlist"

def login():
    """logs in to gmusic"""
    mc = Mobileclient()
    #mc.perform_oauth()
    G.oauth_login(Mobileclient.FROM_MAC_ADDRESS)

def getlibrary():
    """get all library from library"""
    library = G.get_all_songs()
    return library

def removesongs():
    """removes old music"""
    playlists = G.get_all_user_playlist_contents()
    return playlists

def savelibrary(playlists):
    """saves the library to a file"""
    count = 0
    if not os.path.exists(content):
        #print(f'File \'{content}\' not found. Creating it.')
        for elem in playlists:
            contcount = content + "_" + str(count) + ".json"
            with open(contcount, 'w', encoding='utf-8') as f:
                json.dump(elem, f, sort_keys=True, indent=2)
            count = count + 1
    else:
        print("Library exists")

def main():
    login()
    mylibrary = getlibrary()
    playlists = removesongs()
    savelibrary(playlists)
    #this will give us everything that has been stored/downloaded/added
    #to a playlist when logged in with an account
    #we need that data because some tracks are present in a playlist
    #with an uuid only (and lacking song name / artist)
    result = G.get_all_songs()
    #dump to file
    #pp.pprint(result)
    filename="account_library.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, sort_keys=True, indent=2)
if __name__ == '__main__':
    main()

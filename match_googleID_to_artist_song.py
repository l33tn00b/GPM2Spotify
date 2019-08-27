#python > v3
#doooh.
#this is ugly.
#but it is meant to be a quick hack for getting google play playlists (exported to json, e.g. via gmusicapi)
#transferred to spotify.

#kind of a bonus hack for identifying tracks that have been added to a playlist via UUID (not Track ID)
#instead of artist / title
#I guess that happens when adding an entire album/CD to a playlist

#we need a dump of the user's entire google play music library
#as a reference in json format (get it from the google play music export script)

#furthermore, there has to be a list of UUIDs hardcoded into this script to be identified

#admittedly, I could have done this in the original spotify import sscript
#but i realized the fact (of playlist elements being identified via UUID) only after
#having imported most of the playlists.

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
import sys
from spotipy import oauth2
import pprint

#prepare pretty printing (debug)
pp = pprint.PrettyPrinter(indent=2)

#list of UUIDs to be identified
#just copy and paste from spotify playlist import script
idlist = [ '4d563eed-5da0-37b1-95fd-d105409e6859',
  'a5ed77e5-98f5-32cb-aa23-75224447cc55',
  '6dab3328-55e6-3e2f-9e31-190dc3a0b0e3',
  'ba39782a-3fac-386c-8af6-1f27ff5e3ad0',
  '6f9b8f26-8313-34a2-b970-c02a9e6b75c0',
  '2b1bf32e-411b-3643-88f3-9f010c3f8b9b',
  'a54c6b06-26eb-36dd-9445-c3fea6c4d46c',
  '72e1d7b7-c1ce-3a74-85c6-e40fc25da73c',
  '1346af71-2e7a-34e0-8240-d8cd8ea29ead',
  'd930a107-cb5d-3e8d-b4bd-cf6a819415dc',
  '905ace48-d3e0-352f-88a1-70a486574fa6',
  '52e36682-35c0-366a-891b-a27031d556f5',
  '4b62e4f0-060e-3d23-9234-97ce35633a92',
  '7f47f858-205a-365f-b76a-093f4c706dd4',
  '99e89390-ac92-3250-8a45-929bdcd59f09',
  '97f4f9a0-4996-3335-815c-f2a158631c31',
  '559356d8-7151-3661-844f-187bf3893207',
  'c09b5e10-7a27-3032-9886-5ca6939daf1b',
  'eafa61a0-a828-3298-a1c7-5507452310cc',
  'a2d060a9-b43f-385c-baa2-d67a75964ee4',
  '2938d5a1-01f6-388a-a4ef-70ca27ed0ad5',
  '2b9334d5-06e2-3d47-a107-237620d502fa',
  '01b25b89-610e-3115-adea-acfe156dbd2e',
  '5facbbac-ae1f-3d8a-a5d1-a07060a03350',
  'cf128d0c-8514-318d-8140-822e5de1690c',
  '29f21f31-7f12-3d76-96b3-6e5baecc8e66',
  '03a9df8a-b549-3882-964c-8f9726d99061',
  'c2ed0f23-9c2e-3de5-ae7d-39ca28b9cc2a',
  'dfc579d3-ec6c-3b6b-8b4d-736834964b6d',]


#open reference (google play music library dump)
filename="account_library.json"
with open(filename, 'r', encoding='utf-8') as f:
    result = json.load(f)
#pp.pprint(result)

#keep track of number of successful (reverse) identifications
#if we can't identify then maybe google has removed that song from its catalogue?
elemcounter = 0
for elem in result:
    if elem["id"] in idlist:
        elemcounter = elemcounter + 1
        print("ID: \t" + elem["id"])
        print("Artist:\t" + elem["artist"])
        print("Title: \t" + elem["title"])
        print()
print("Found " + str(elemcounter) + " IDs out of " + str(len(idlist)))
sys.exit()

#now, add the missiing songs via spotify's web player (or whatever alternative you like)

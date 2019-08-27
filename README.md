# GPM2Spotify
Tools for transferring playlists from Google Play Music to Spotify

0. Very First step:
Install dependencies (see gmusicapi and spotipy documentation)

1. First step:
* Execute pull_googlemusic_playlists.py
-> Will give you a bunch of json files (one for each playlist and a big one for the user's entire library)  
Now, you can happily terminate your Google Play Music Subscription (e.g. because they don't have Rammstein available).

2. Second step:
* Sign up for the Spotify developer console: http://developer.spotify.com
* Go to Dashboard
* Create an App
* Enter whatever you like (I prefer "I don't know") and accept the consequences
* Enter Redirect URL: http://localhost/ (this is not a joke)
* Note Client ID and Client Secret


3. Third Step: Edit get_permissions.py
* To contain your (newly created) app's Client ID and Client Secret
* To contain your user name

4. Fourth Step: Sign in to Spotify with your browser
* If you're not already signed in because of the previous developer console session
* This makes requesting permissions (c.f.) just a little it easier (you could skip this step and it would be done during the next one)

5. Fifth Step: Run get_permissions.py
* Will authenticate against Spotify and request necessary permissions for playlist creation
* Acknowledge the dialogue
* Don't be surprised if the next thing you see is a blank page in your browser
* Copy the entire address shown in the browser's address line to the Python dialogue
* If successful, some cryptic data will be shown (e.g. containing your displayed name in Spotify)
* If not successful, check for incomplete copy and paste and repeat this step
* Still not successful? Check Client ID and Client Secret.
* No luck, still? Check, re-check, and double-check redirect-URL in the developer console and get_permissions.py being identical

6. Sixth Step: 

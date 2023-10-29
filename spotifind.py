import praw
import spotipy
from spotipy import SpotifyClientCredentials
import time
import string
import os

reddit_client_id = os.environ['REDDIT_ID']
reddit_secret_id = os.environ['REDDIT_SECRET']
reddit_password = os.environ['REDDIT_PASSWORD']
spotify_client_id = os.environ['SPOTIFY_ID']
spotify_secret_id = os.environ['SPOTIFY_SECRET']

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_secret_id,
    user_agent="<console:SPOTIFIND:1.0>",
    username="Spotifind",
    password=reddit_password,
)

sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
        client_id=spotify_client_id,
        client_secret=spotify_secret_id,
    )
)

# Subreddits to check comments within. 
# Blank for now, insert whatever is wanted
subreddits = []

# Loop that runs forever
# print('Running...')
while True:

    # Keep track of time to know when to sleep
    start_time = time.time()

    # Go through each selected subreddit
    # print("Checking recent posts...")
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        comments = subreddit.comments(limit=10)

        # Iterate through comments and return true if keyword is found
        for comment in comments:
            if "!spotifind" in comment.body.lower():
                # Check if comment is saved. Bot saves each comment after replying so it doesn't double-dip
                if not comment.saved:
                    print(f'Keyword found in comment: {comment.body}')
                    # Set query as the remainder of the comment
                    query = comment.body.lower().replace("!spotifind", "").strip()
                    # If query is empty, skip post
                    if len(query) == 0:
                        comment.save()
                        print('Query is empty. Skipping...')
                        continue
                    # Initialize reply text
                    reply_text = "Artist results for **{query}**:  \n\n".format(query=string.capwords(query))
                    print('Searching artists...')
                    search_artists = sp.search(q=query, limit=3, type="artist")
                    # Spotipy packages artists as nested dictionaries, this just makes it easier to iterate through keys
                    artists = search_artists['artists']['items']

                    # If there are no artists, give a message
                    if len(artists) == 0:
                        print('No artists found...')
                        reply_text += 'No artists found!  \n'
                    else:
                        print('Artists found!')
                        # Add artists to reply
                        for artist in artists:
                            print(artist['name'])
                            reply_text += '**[{name}]({url})**  \n'.format(name=artist['name'],
                                                                           url=artist['external_urls']['spotify'])
                    print('Searching tracks...')
                    reply_text += "  \nSong results for **{query}**:  \n\n".format(query=string.capwords(query))
                    search_tracks = sp.search(q=query, limit=3, type="track")
                    # Same logic as the artists variable
                    tracks = search_tracks['tracks']['items']

                    # If there are no tracks, give a message
                    if len(tracks) == 0:
                        print('No tracks found...')
                        reply_text += 'No tracks found!  \n'
                    else:
                        print('Tracks found!')
                        for track in tracks:
                            print(track['name'])
                            # Add tracks to reply
                            reply_text += '**[{name}]({url})**  \n'.format(name=track['name'],
                                                                           url=track['external_urls']['spotify'])

                    # Save comment as replied to
                    comment.save()
                    # Send reply
                    comment.reply(reply_text)

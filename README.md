# u/Spotifind
This is a small Reddit bot that searches for artists and songs on Spotify while providing links

[u/Spotifind](https://www.reddit.com/u/Spotifind) will reply to comments under certain subreddits when users include the text "!spotifind" in their comment. The bot relies on [Spotipy](https://github.com/spotipy-dev/spotipy) and [PRAW](https://github.com/praw-dev/praw).

The bot is hosted on Replit, but is not currently deployed because I don't want to pay for the reserved VM lol

## Usage
In order to call on the bot, include the text "!spotifind" anywhere in the post.
* The bot will automatically search for all text within the comment except for "!spotifind".
* The bot only searches for the first 100 characters that don't include the "!spotifind" phrase for simplicity
* The bot and use of the "!spotifind" command is not case sensitive and is detected regardless of capitalizaiton.
* If your query yields no results, Spotifind will still reply and explain this.
* Spotifind only reports the first 3 songs and first 3 artists. If there are less than 3 results it will report all of them.

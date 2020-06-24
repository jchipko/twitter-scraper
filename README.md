# twitter-scraper

Extract tweets from Twitter and store them in a database.

## Installation

- `pip3 install -r requirements.txt`

## Setup

- Sign up for a [Twitter developer account](https://developer.twitter.com/en).
- [Create an application](https://developer.twitter.com/en/apps).
- Create a file named `private.py` and add the keys below to it using the values from your app:
	- `TWITTER_KEY`
	- `TWITTER_SECRET`
 	- `TWITTER_APP_KEY`
	- `TWITTER_APP_SECRET` 
- Set the `CONNECTION_STRING` key in `private.py` (you can use sqlite:///tweets.db as a default).
- Update `TRACK_TERMS` in `settings.py` with the terms you want to search for.

## How To Use

- Run `python3 twitter-scraper`. Use `Ctrl + C` to stop it. 

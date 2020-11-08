import imagehash
import logging
import requests
import sqlite3
import os
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

# given a reddit user, leverage pushshift to iterate through content and archive
USER = "" # TODO - make this a commandline arg
URL = f"https://api.pushshift.io/reddit/search/submission/"

# create user directory
if not os.path.exists(USER):
	logging.debug(f" User: {USER} does not exist, creating folder.")
	os.mkdir(USER)

if not os.path.exists(f'{USER}/posts.db'):
	logging.debug(f" User: {USER} does not have a post record. Creating.")
	# create DB for reference
	conn = sqlite3.connect(f'{USER}/posts.db')
	c = conn.cursor()
	c.execute('''
		CREATE TABLE posts (id text, created_utc integer, title text, hash text, duplicate integer)
		''')
	conn.commit()
	conn.close()

# check db for most recent record
# "SELECT * FROM posts ORDER BY created_utc DESC LIMIT 1"

	# iterate through pushshift and last record till current time
	# check if post is duplicate
		# if not, download image and check if hash already exists and dedupe
			# save hash
		# Add title text to bottom of image
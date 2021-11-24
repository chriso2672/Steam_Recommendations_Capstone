# standard library imports
import csv
import datetime as dt
import json
import os
import statistics
import time
import pickle

# third-party imports
import numpy as np
import pandas as pd
import requests

api_key = '9C34DB5DC9F6FB662853AC6217BC048F'

def steam_request(endpoint: str, params):
	"""Generic method to perform a request to Steam's public API.
	Parameters
	----------
	endpoint : str
		The endpoint to hit
	params : dict[str, str]
		The query parameters to pass to requests
	
	Returns
	-------
	any
		The JSON-decoded body of the returned response
	Raises
	------
	requests.RequestException
		If any failures occurred while making the request
	"""
	r = requests.get(
		f'https://api.steampowered.com/{endpoint}/',
		{
			**params,
			**{
				'key': api_key,
				'format': 'json'
			}
		}
	)
	r.raise_for_status()

	body = r.json()
	return body

def get_games_for_steamid(steamid: str):
	"""Gets the games owned by a Steam user
	Parameters
	----------
	steamid : str
		The user's 64-bit Steam ID
	
	Returns
	-------
	set[tuple[int, str]]
		The set of games this user owns, in tuples of appid and game name
	"""
	body = steam_request('IPlayerService/GetOwnedGames/v0001', params={
		'include_appinfo': True, 'steamid': steamid
	
	})
	if not body['response']:
		return None
	else:
		return set((game['appid'], game['name'], game['playtime_forever']) for game in body['response']['games'])
    

def print_games(games):
	"""Helper function to print a list of games"""
	for game in sorted(games, key=lambda g: g[1]):
		print(f' - {game[1]}')
	print()



with open('trui.pickle', 'rb') as handle:
   top_rated_user_ids = pickle.load(handle)



steamid_games = { steamid: get_games_for_steamid(str(steamid)) for steamid in top_rated_user_ids }

print(steamid_games)

# Store data (serialize)
with open('top_rated_user_libraries.pickle', 'wb') as handle:
    pickle.dump(steamid_games , handle, protocol=pickle.HIGHEST_PROTOCOL)
#!/usr/bin/python

import requests
from urllib import urlretrieve
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib.offsetbox import OffsetImage
import pandas as pd
from IPython.display import display

def get_player_id(player):
	"""
	Loads a pandas DataFrame, numpy array, or int with the desired player ID(s)
	from an online repository.
	The player IDs are used to identify players in the NBA stats api.
	Parameters
	----------
	player : str
		The desired player's name in 'Last Name, First Name' format. Passing in
		a single name returns a numpy array containing all the player IDs
		associated with that name.
		Passing "SHOTS" returns a DataFrame with all the players and their IDs
		that have shot chart data.
		Passing in "ALL" returns a DataFrame with all the available player IDs
		used by the NBA stats API, along with additional information.
		The column information for this DataFrame is as follows:
			PERSON_ID: The player ID for that player
			DISPLAY_LAST_COMMA_FIRST: The player's name.
			ROSTERSTATUS: 0 means player is not on a roster, 1 means he's on a
						  roster
			FROM_YEAR: The first year the player played.
			TO_YEAR: The last year the player played.
			PLAYERCODE: A code representing the player. Unsure of its use.
	"""
	if player == "SHOTS":
		return pd.read_csv("data/players2001.csv")
	elif player == "ALL":
		return pd.read_csv("data/player_id.csv")
	else:
		df = pd.read_csv("data/player_id.csv")
		player_id = df[df.DISPLAY_LAST_COMMA_FIRST == player].PERSON_ID
		if len(player_id) == 1:
			return player_id.values[0]
		if len(player_id) == 0:
			raise NoPlayerError('There is no player with that name.')
		return player_id.values

def get_response(player_id, league_id="00", season="2014-15",
			 season_type="Regular Season", team_id=0, game_id="",
			 outcome="", location="", month=0, season_segment="",
			 date_from="", date_to="", opp_team_id=0, vs_conference="",
			 vs_division="", position="", rookie_year="", game_segment="",
			 period=0, last_n_games=0, clutch_time="", ahead_behind="",
			 point_diff="", range_type="", start_period="", end_period="",
			 start_range="", end_range="", context_filter="",
			 context_measure="FGA"):

	base_url = "http://stats.nba.com/stats/shotchartdetail?"

	# TODO: Figure out what all these parameters mean for NBA stats api
	#       Need to figure out and include CFID and CFPARAMS, they are
	#       associated w/ContextFilter somehow
	url_paramaters = {
							"LeagueID": league_id,
							# Season: season in which data is collected (eg 2014-2015)
							"Season": season,
							# SeasonType: regular season or playoffs
							"SeasonType": season_type,
							# TeamID: data collected only for when player is playing on this team
							"TeamID": team_id,
							# PlayerID: the player the data is being collected for
							"PlayerID": player_id,
							# GameID: data only collected for this specific game
							"GameID": game_id,
							# Outcome: games where player's team won or lost
							"Outcome": outcome,
							# Location: data collected at specific stadium
							"Location": location,
							# Month: specify the month that data is collected from
							"Month": month,
							# SeasonSegment: not sure
							"SeasonSegment": season_segment,
							# DateFrom: to select data from a specific segment of dates
							"DateFrom": date_from,
							# DateTo: to select data from a specific segment of dates
							"DateTo": date_to,
							# OpponentTeamID: data collected only when the Player is playing a certain opponent
							"OpponentTeamID": opp_team_id,
							# VsConference: data collected only when player is playing teams from certain conference
							"VsConference": vs_conference,
							# VsDivision: data collected only when player is playing teams from certain division
							"VsDivision": vs_division,
							# Position: data collected when player is playing at a certain postion
							# (eg if Draymond Green is playing PF or C)
							"Position": position,
							# RookieYear: not sure
							"RookieYear": rookie_year,
							# GameSegment: not sure
							"GameSegment": game_segment,
							# Period: what period data is collected during (eg 1, 2, 3, 4)
							"Period": period,
							# LastNGames: data will only be collected from the last n games in a specified time period
							"LastNGames": last_n_games,
							# ClutchTime: During 4th or OT, less than 5 min left, neither team ahead by more than 5
							"ClutchTime": clutch_time,
							# AheadBehind: data collected only if the player's team is behind or ahead
							"AheadBehind": ahead_behind,
							# PointDiff: not sure
							"PointDiff": point_diff,
							# RangeType: not sure
							"RangeType": range_type,
							# StartPeriod: the point during a game when data starts being collected
							"StartPeriod": start_period,
							# EndPeriod: the point during a game when data stops being collected
							"EndPeriod": end_period,
							# StartRange: not sure
							"StartRange": start_range,
							# EndRange: not sure
							"EndRange": end_range,
							"ContextFilter": context_filter, # unsure of what this does
							"ContextMeasure": context_measure
						}

	return requests.get(base_url, params=url_paramaters)


def draw_court(color='white', lw=2, outer_lines=True):
	# Create the various parts of an NBA basketball court

	# There is a conversion between inches to graph units of 6":5u

	# Create the basketball hoop
	# Diameter of a hoop is 18" so it has a radius of 9", which is a value
	# 7.5 in our coordinate system
	hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

	# Create backboard
	backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

	# The paint
	# Create the outer box 0f the paint, width=16ft, height=19ft
	outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
	# Create the inner box of the paint, widt=12ft, height=19ft
	inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

	# Create free throw top arc
	top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color)
	# Create free throw bottom arc
	bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, 
							color=color, linestyle='dashed')
	# Restricted Zone, it is an arc with 4ft radius from center of the hoop
	restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

	# Three point line
	# Create the side 3pt lines, they are 14ft long before they begin to arc
	corner_three_a = Rectangle((-220, -47.5), 0, 137, linewidth=lw, color=color)
	corner_three_b = Rectangle((220, -47.5), 0, 137, linewidth=lw, color=color)
	# 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
	# I just played around with the theta values until they lined up with the threes
	three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

	# Center Court
	center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
	center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

	# List of the court elements to be plotted onto the axes
	court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
					  bottom_free_throw, restricted, corner_three_a,
					  corner_three_b, three_arc, center_outer_arc,
					  center_inner_arc]

	if outer_lines:
		# Draw the half court line, baseline and side out bound lines
		outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
								color=color, fill=False)
		court_elements.append(outer_lines)

	fig = plt.gcf()

	# Add the court elements onto the axes
	for element in court_elements:
		fig.gca().add_artist(element)

print "Enter player"
playerName = raw_input(">> ")
lastFirst = ', '.join(reversed(playerName.split(' ')))
playerID = get_player_id(lastFirst)

print "enter year (in format yyyy-yy (e.g. 2014-15))"
year = raw_input(">> ")

# Get the webpage containing the data
response = get_response(playerID, league_id="00", season="2014-15",
			 season_type="Regular Season", team_id=0, game_id="",
			 outcome="", location="", month=0, season_segment="",
			 date_from="", date_to="", opp_team_id=0, vs_conference="",
			 vs_division="", position="", rookie_year="", game_segment="",
			 period=0, last_n_games=0, clutch_time="", ahead_behind="",
			 point_diff="", range_type="", start_period="", end_period="",
			 start_range="", end_range="", context_filter="",
			 context_measure="FGA")
# Grab the headers to be used as column headers for our DataFrame
headers = response.json()['resultSets'][0]['headers']
# Grab the shot chart data
shots = response.json()['resultSets'][0]['rowSet']
# League Averages
headersLA = response.json()['resultSets'][1]['headers']
# LA shotss
shotsLA = response.json()['resultSets'][1]['rowSet']

# Create pandas dataframe to store the shot data in a comprehensive way
shot_df = pd.DataFrame(shots, index=range(0,len(shots)), columns=headers)

leagueAvg_df = pd.DataFrame(shotsLA, columns=headersLA)

# print out dataframe info using IPython module
with pd.option_context('display.max_columns', None): display(shot_df.head())

with pd.option_context('display.max_columns', None): display(leagueAvg_df.head())

# custom color dict to define the range of colors to represent shot averages relative to league average
cdict = {'red': ((0,0,0),
				(.25,0,0),
				(.5,1,1),
				(.75,1,1),
				(1,1,1)),
		'green':((0,0,0),
				(.25,.75,.75),
				(.5,1,1),
				(.75,.5,.5),
				(1,0,0)),
		'blue': ((0,1,1),
				(.25,1,1),
				(.5,.75,.75),
				(.75,0,0),
				(1,0,0))}
# set the cmap to be used to utilize the cdict
cmap = LinearSegmentedColormap('MyColorDict', cdict)

def getFgStr(row):
	return row.SHOT_ZONE_BASIC+'-'+row.SHOT_ZONE_AREA+': '+row.SHOT_ZONE_RANGE

def getLgAvgZones(df):
	zoneAvgs = {}
 	for index, row in df.iterrows():
 		zoneAvgs[getFgStr(row)] = row.FG_PCT
 	return zoneAvgs

def getPlayerZones(df, lgAvgs):
	zoneAvgLists = {}
	for index, row in df.iterrows():
		zoneAvgLists.setdefault(getFgStr(row), []).append(row.SHOT_MADE_FLAG)
	zoneAvgs={}
	for z in lgAvgs:
		if z in zoneAvgLists:
			zoneAvgs[z] = sum(zoneAvgLists[z])/float(len(zoneAvgLists[z]))
		else:
			zoneAvgs[z] = 0
	return zoneAvgs

avgShotDict = getLgAvgZones(leagueAvg_df)
playerAverages = getPlayerZones(shot_df,avgShotDict)

shot_df['ZONE_AVG'] = [playerAverages[getFgStr(row)] for index, row in shot_df.iterrows()]

#1.07
#1.03
#0.98
#0.94
def compare(avgShots, playerShots):
	relativeShotDict = {}
	for zone in avgShots:
		if playerShots[zone]>avgShots[zone]*1.07:
			relativeShotDict[zone] = .9
		elif playerShots[zone]>avgShots[zone]*1.03:
			relativeShotDict[zone] = .7
		elif playerShots[zone]>avgShots[zone]*.97:
			relativeShotDict[zone] = .5
		elif playerShots[zone]>avgShots[zone]*.93:
			relativeShotDict[zone] = .3
		else:
			relativeShotDict[zone] = .1
	return relativeShotDict


meltedAvgs = compare(avgShotDict, playerAverages)
shot_df['ZONE_COLOR'] = [meltedAvgs[getFgStr(row)] for index, row in shot_df.iterrows()]

plt.figure(figsize=(11,9))

# plot the figure using matplotlib's hexbin plot methods
im = plt.hexbin(shot_df.LOC_X,shot_df.LOC_Y, C=shot_df.ZONE_COLOR, marginals=False,
		   bins='log', cmap=cmap, gridsize=85, edgecolors='#152435')

# draw the court lines on the current plot
draw_court()

# set the limits of the court to display the half court
plt.ylim([424.5,-49.5])
plt.xlim([-252,252])

# take off axis tick marks, no use for them in this context
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

#get the player's picture from nba.com
pic = urlretrieve("http://stats.nba.com/media/players/230x185/"+str(playerID)+".png", str(playerID)+".png")
player_pic = plt.imread(pic[0])
img = OffsetImage(player_pic, zoom=0.6)
img.set_offset((600,75))
plt.gca().add_artist(img)

# add a title
plt.title(playerName+' FGA \n'+year+' Reg. Season', fontsize=20, y=1.01)

# set the background color
plt.gca().set_axis_bgcolor('#152435')
plt.show()
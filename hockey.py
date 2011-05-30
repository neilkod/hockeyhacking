#!/use/bin/python

import json
import string
players = {}
nodes = []
hits = []
#sample url = 'http://live.nhl.com/GameData/20102011/2010020820/PlayByPlay.json'
# game_id = '2010021220' # panthers vs capitals 09-apr-2011
# game_id = '2010030317' # lightning vs bruins game 7
game_id = '2010020820' # buffalo vs panthers - lot of hits
game_data = game_id + '.json'
with open(game_data, 'r') as f:
	game_data = json.load(f)

home_team = game_data['data']['game']['hometeamname']
away_team = game_data['data']['game']['awayteamname']
home_team_id = game_data['data']['game']['hometeamid']
away_team_id = game_data['data']['game']['awayteamid']
plays = game_data['data']['game']['plays']['play']


# make a pass through the data to build the player list
# then make another pass to build the actual edge list.
# i should be able to consolidate these two passses - hey
# i'm just getting started!!

for play in plays:

	if play['type'] == 'Hit':
		# determine if the source player (pid1) is home or away
		# for purposes of retrieving team name
		if play['teamid'] == away_team_id:
			pid1_team = away_team
			pid2_team = home_team
		else:
			pid1_team = home_team
			pid2_team = away_team
		players[play['p1name']] = {"player_id" : play['pid1'], "team": pid1_team}
		players[play['p2name']] = {"player_id" : play['pid2'], "team": pid2_team}

# create the gephi file
f = open(game_id+'.gdf','w')
f.write('nodedef> name VARCHAR, label VARCHAR, team VARCHAR\n')

for k,v in players.iteritems():
	f.write('%s,%s,%s\n' % (v['player_id'],k, v['team']))

# create the edges
f.write('edgedef> source VARCHAR, target VARCHAR\n')


# iterate through the plays again and record the hits
for play in plays:
	if play['type'] == 'Hit':

		hits.append((play['pid2'], play['pid1'] ))


# one issue here is that gephi doesn't support dupes in the edge list
# this is unfortunate because it screws up the data. if player a hits player b twice,
# it'll only count as one.

for (source, target) in set(hits):
	f.write('%d,%d\n' % (source, target ))
f.close()
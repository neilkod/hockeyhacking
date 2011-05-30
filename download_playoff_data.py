#!/usr/bin/python

import time, urllib2, json
BASE_URL = 'http://live.nhl.com/GameData/20102011/%s/PlayByPlay.json'



def analyze_playoff_data(game1_id, games):
	players = {}
	nodes = []
	hits = []
	
	
	gameno = int(str(game1_id)[-1])
	game_id = game1_id
	while gameno <= games:
		game_data_file = '%s.json' % game_id
		with open(game_data_file, 'r') as f:
			game_data = json.load(f)
			home_team = game_data['data']['game']['hometeamname']
			away_team = game_data['data']['game']['awayteamname']
			home_team_id = game_data['data']['game']['hometeamid']
			away_team_id = game_data['data']['game']['awayteamid']
			plays = game_data['data']['game']['plays']['play']
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

			# iterate through the plays again and record the hits
			for play in plays:
				if play['type'] == 'Hit':

					hits.append((play['pid2'], play['pid1'] ))
			print "game is %s hits is %s" % (gameno,len(hits))
			game_id += 1
			gameno += 1

	# create the gephi file
	f = open('%s.gdf' % game1_id,'w')
	f.write('nodedef> name VARCHAR, label VARCHAR, team VARCHAR\n')
	for k,v in players.iteritems():
		f.write('%s,%s,%s\n' % (v['player_id'],k, v['team']))
	# create the edges
	f.write('edgedef> source VARCHAR, target VARCHAR\n')
	for (source, target) in set(hits):
		f.write('%d,%d\n' % (source, target ))
	f.close()



def download_playoff_game_data(game_id, games):
	"""hacky sample script to download all 7 games of tbl-bos series from 2011
		series went 7 games. unfortunately, boston won.
		note: that is the end of my social commentary in the code comments."""


	game_id = game_id # game 1 of bos-tbl

	gm = 1
	while gm <= 4:
		url = BASE_URL % game_id
		response = urllib2.urlopen(url)
		json_data = response.read()
		f = open('%d.json' % game_id, 'w')
		f.write(json_data)
		f.close()
		game_id += 1
		gm += 1
		# sleep for 2 seconds so we don't peg the nhl.com
		# servers with rate requests
		time.sleep(2)

def main():
	
	#game1_id = 2010030311 # tbl-bos
	game1_id = 2010030211 # tbl-was
	games = 4

	download_playoff_game_data(game1_id, games)
	analyze_playoff_data(game1_id,games)	
if __name__ == '__main__':
	main()
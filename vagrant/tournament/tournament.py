#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2



def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")

def deleteMatches():
	"""Remove all the match records from the database."""
	DB,cur = connect()

	cur.execute("DELETE FROM match;")

	DB.commit()
	DB.close()


def deletePlayers():
	"""Remove all the player records from the database."""
	DB,cur = connect()

	cur.execute("DELETE FROM player;")

	DB.commit()
	DB.close()


def countPlayers():
	"""Returns the number of players currently registered."""
	DB,cur = connect()

	cur.execute("SELECT count(*) FROM player;")

	nPlayers = cur.fetchone()[0]
	print nPlayers

	DB.close()

	return nPlayers


def registerPlayer(name):
	"""Adds a player to the tournament database.

	Args:
	  name: the player's full name (need not be unique).
	"""
	DB,cur = connect()

	cur.execute("INSERT INTO player(name) VALUES (%s);", (name,))

	DB.commit()
	DB.close() 

def playerStandings():
	"""Returns a list of the players and their win records, sorted by wins.

	The first entry in the list should be the player in first place, or a player
	tied for first place if there is currently a tie.

	Returns:
	  A list of tuples, each of which contains (id, name, wins, matches):
	    id: the player's unique id (assigned by the database)
	    name: the player's full name (as registered)
	    wins: the number of matches the player has won
	    matches: the number of matches the player has played
	"""
	DB,cur = connect()

	#use standing view
	cur.execute("SELECT * FROM standing;")

	posts = [(int(row[0]),str(row[1]),int(row[2]),int(row[3])) for row in cur.fetchall()]

	DB.close() 
	return posts


def reportMatch(winner, loser, draw='false'):
	"""Records the outcome of a single match between two players.

	Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
	  draw:  true if a draw
	"""

	DB,cur = connect()

	
	cur.execute("INSERT INTO match(winner,loser,isDraw) VALUES (%s,%s,%s)", (winner, loser, draw))

	DB.commit()
	DB.close() 


def swissPairings():
	"""Returns a list of pairs of players for the next round of a match.

	Assuming that there are an even number of players registered, each player
	appears exactly once in the pairings.  Each player is paired with another
	player with an equal or nearly-equal win record, that is, a player adjacent
	to him or her in the standings.

	Returns:
	  A list of tuples, each of which contains (id1, name1, id2, name2)
	    id1: the first player's unique id
	    name1: the first player's name
	    id2: the second player's unique id
	    name2: the second player's name
	"""

	#get current standings sorted from most to least wins
	standings = playerStandings()

	pairings = [] #output pairings
	curr_pair = [] #used to gather each pair

	
	for player in standings:
		#add each player to the current pairing.
		curr_pair.extend([player[0],player[1]])
		#when the curr_pair has two players pass contents to the pairings and clear
		if len(curr_pair)==4:
			pairings.append(curr_pair)
			curr_pair=[]

	
	#if odd players curr_pair will contain final player
	if len(curr_pair)>0:
		DB,cur = connect()
		cur.execute("INSERT INTO bye(player) VALUES (%s)", (curr_pair[0],))
		DB.commit()
		DB.close() 
	
	return pairings


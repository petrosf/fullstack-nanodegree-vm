#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")

def deleteMatches():
	"""Remove all the match records from the database."""
	DB = connect()
	cur = DB.cursor()

	cur.execute("DELETE FROM match;")

	DB.commit()
	DB.close()


def deletePlayers():
	"""Remove all the player records from the database."""
	DB = connect()
	cur = DB.cursor()

	cur.execute("DELETE FROM player;")

	DB.commit()
	DB.close()


def countPlayers():
	"""Returns the number of players currently registered."""
	DB = connect()
	cur = DB.cursor()

	cur.execute("SELECT count(*) FROM player;")

	nPlayers = cur.fetchall()[0][0]

	DB.close()

	return nPlayers


def registerPlayer(name):
	"""Adds a player to the tournament database.

	Args:
	  name: the player's full name (need not be unique).
	"""
	DB = connect()
	cur = DB.cursor()

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
	DB = connect()
	cur = DB.cursor()

	#Using scalar subqueries
	cur.execute("SELECT * FROM standing;")

	posts = [(int(row[0]),str(row[1]),int(row[2]),int(row[3])) for row in cur.fetchall()]

	DB.close() 
	return posts


def reportMatch(winner, loser, draw='false'):
	"""Records the outcome of a single match between two players.

	Args:
	  player1 & player2:  the id number of the player2
	  result:  0=draw, 1=player1 won, 2=player2 won
	  round: int number
	"""

	DB = connect()
	cur = DB.cursor()

	
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
	print standings

	pairings = [] #output pairings
	curr_pair = [] #used to gather each pair

	for player in standings:
		#add each player to the current pairing.
		curr_pair.extend([player[0],player[1]])
		#when the curr_pair has two players pass contents to the pairings and clear
		if len(curr_pair)==4:
			pairings.append(curr_pair)
			curr_pair=[]

	'''
	#if odd players curr_pair will contain final player
	DB = connect()
	cur = DB.cursor()
	cur.execute("INSERT INTO match(match,player,score) VALUES (NULL,%s,%s)", (curr_pair[0], 3))
	DB.commit()
	DB.close() 
	'''
	return pairings


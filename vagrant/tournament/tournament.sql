-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE player (
id serial PRIMARY KEY,
name text );

CREATE TABLE match (
id serial PRIMARY KEY,
winner int REFERENCES player(id),
loser int REFERENCES player(id),
isDraw boolean DEFAULT false
);

CREATE VIEW matchesPlayed AS
SELECT player.id as id, player.name as name, count(match.id) as nMatches
FROM player LEFT JOIN match
ON (player.id = match.winner OR player.id = match.loser)
GROUP BY player.id 
;

CREATE VIEW matchesWon AS
SELECT player.id as id, player.name as name, count(match.id) as nWins
FROM player LEFT JOIN match
ON (match.winner=player.id AND match.isDraw=false)
GROUP BY player.id 
;

CREATE VIEW matchesTied AS
SELECT id, name,
(SELECT count(id) FROM match WHERE (match.winner=player.id OR match.loser=player.id) AND match.isDraw=true) as tiePoints 
FROM player
;

CREATE VIEW standing AS
SELECT player.id, player.name, (matchesWon.nWins+0.5*matchesTied.tiePoints) as nWins, matchesPlayed.nMatches
FROM player, matchesPlayed, matchesWon, matchesTied
WHERE (player.id = matchesPlayed.id AND player.id = matchesWon.id AND player.id = matchesTied.id)
ORDER BY nWins DESC
;

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
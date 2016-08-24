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

CREATE TABLE players (
ID serial PRIMARY KEY,
name text );

CREATE TABLE matches (
ID serial PRIMARY KEY,
round int NOT NULL
);

CREATE TABLE results (
ID serial PRIMARY KEY,
match int  REFERENCES matches(ID), -- a bye will be NULL
player int REFERENCES players(ID),
score int NOT NULL -- lose=0, draw=1, win=3
);






# Swiss-style Tournament Planner
## Description
This python module uses a PostgreSQL database to keep track of players and matches in a game tournament.
The game tournament uses the Swiss system for pairing up players in each round: players are not eliminated, and each player is paired with another player with the same number of wins, or as close as possible.

The implementation has the following extra features:
- Support games where a draw (tied game) is possible.
- Does not assume an even number of players. If there is an odd number of players, assigns one player a “bye” (skipped round). A bye counts as a free win. *NOTE: no check implemented to ensure that a player has no more than one bye in a tournament.*

## Files
- **tournament.sql** - psql commands which create the database and the schema
- **tournament_test.py** - functions used to interact with database and implement the tournament planner
- **tournament.py** - code used to test the functions in tournament_test.py

## How to use
1. Use tournament.sql to create database
..*command: psql -f tournament.sql
2. Run tournament_test.py to test the code functionality
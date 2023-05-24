# infoDump
Python Neo4J Playbase

## Basic Description
For now, this is just me playing around with a Python front end that links to a Neo4J instance for the back end.
Started as a superhero database for Arrowverse, and ended up being a generic book/comic/TV/movie database
Haven't started the GUI (front end UI) work yet, so it's little better than using the Aura console.
Working on a Cypher statement builder, but casually (Don't expect big rapid improvements).

## Home Use
To use this on your own database, you will need to put the following into a .env file.

URI=<Your connection URI, from the Neo4J Console page, connection tab.>

N4USER= < Your user name. >
  
N4PASS= < password for above account. >

## Superhero database from Kaggle
heroes.csv and super_hero_powers.csv come from
the superheroAPI courtesy of Kaggle.com.

The super.csv file is an attempt to merge the two
using the pandas dataframe.  Given the way
the superhero API denominates powers, I decided 
a better way of describing them was needed.

# CSV Interface for stv
cstv.py runs stv based on votes in an input csv file.
* Expected format of the input csv is rows for voters, colums for candidates
* First column must be named 'voter'
* Other column headers are candidate names and must be unique
* Row headers ('voter' column values) must be unique
* Each row must contain a sequence of rank values starting at 1
* There can be no gaps in the ranks and no repeated ranks
* Rows that fail validation are dropped (so those votes don't count)
* If there are multiple votes for the same voter in the file, only the last one counts.

Command line: ```python cstv.py -f vote-file-path -n num-winners```
where vote-file-path is relative path to the input csv file
and num-winners parses to an int that is the number of winners to select.

[votes.csv](https://github.com/psteitz/steve/blob/trunk/pysteve/csv/votes.csv)
is a sample input file.  It is set up for an election where
voters have 5 votes each from among 10 candidates.  In this example,
all voters submit full ballots.

cstv.py uses the stv implementation in ../lib/plugins/stv.py

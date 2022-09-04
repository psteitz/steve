CSV Interface for pysteve
cstv.py runs stv based on votes in an input csv file.
* Expected format of the input csv is rows for voters, cols for candidates
* First col must be named 'voter'
* Other column headers are candidate names and must be unique
* Row headers (voter values) must be unique
* Each row must contain a sequence of rank values starting at 1
* There can be no gaps in the ranks and no repeated ranks

Command line: ```python cstv.py -f vote-file-path -n num-winners```
where vote-file-path is relative path to the input csv file
and num-winners parses to an int that is the number of winners to select.

[votes.csv](https://github.com/psteitz/steve/blob/trunk/pysteve/csv/votes.csv)
is a sample input file.  It is set up for an election where
voters have 5 votes each and 5 winners are selected.  In this example,
all voters submit full ballots.

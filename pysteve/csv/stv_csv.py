

import csv
import sys
import os.path

# Set the system path so we can get pysteve libraries
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from lib.plugins import stv

def validate_record(record, num_winners):
    # must have 'voter' key
    if 'voter' not in record:
        return False, 'missing voter key'
    # values must be 1,...,n for some n <= num_winners
    # get the values
    values = []
    for key in record:
        if record[key].isdigit():
            values.append(record[key])
    # check too many ranks
    if len(values) > num_winners:
        return False, 'too many ranks'
    # make sure values has no gaps
    for i in range(len(values)):
        if str(i + 1) not in values:
            return False, 'gap in ranks - missing ' + str(i)
    return True, None

def run(num_winners, votes_path):

    # list of voters pulled from the csv row headers
    voters = []

    # raw_votes is a dict keyed on voters with values vote dicts with candidate keys
    # so votes['phil'] has 'eat more cereal' if phil voted for 'eat more cereal'.
    # Values are ranks.
    raw_votes = {}

    # loved_ones are the candidates that are included in any vote
    loved_ones = []

    # read csv
    input_file = csv.DictReader(open(votes_path))

    '''
    Read the input csv
    Expected format is rows for voters, cols for candidates
    First col must be named 'voter'
    Other column headers are candidate names and must be unique
    Row headers (voter values) must be unique
    Each row must contain a sequence of rank values starting at 1
    There can be no gaps in the ranks and no repeated ranks
    '''
    for record in input_file:
        # Validate the record. If validation fails, print message and skip
        # this record.
        result, message = validate_record(record, num_winners)
        print("attempted record validate for " + record['voter'])
        if not result:
            print('Skipping record that failed validation due to ' + message)
            print(record)
            continue

        # add the voter to voters and create a raw_votes record for the voter
        voter = record['voter']
        voters.append(voter)
        raw_votes[voter] = {}
        # note that if this is a duplicate vote for this voter the effect is to
        # over-write the previous vote.

        for candidate in record:
            if candidate != "voter":  # skip name
                # record voter candidate rank
                raw_votes[record['voter']][candidate] = record[candidate]
                # add ranked candidate to loved ones
                if candidate not in loved_ones:
                    loved_ones.append(candidate)

    print("There are ", len(loved_ones), 'loved ones')
    print(loved_ones)

    # Create election issue
    issue = {}
    issue['type'] = 'stv' + str(num_winners)
    candidate_names = loved_ones
    issue['candidates'] = {}

    # candidates is a list of dicts with just 'name' property - one for each candidate
    candidate_list = []
    for candidate in candidate_names:
        new_candidate = {}
        new_candidate['name'] = candidate
        candidate_list.append(new_candidate)
    issue['candidates'] = candidate_list

    # create "letters" used to identify votes - may go into unprintable range, but that is OK
    # as they are not displayed anywhere
    letters = []
    for i in range(len(loved_ones)):
        letters.append(chr(ord('a')+i))

    # Now create votes - need to be lists of letters with letters standing for
    # candidates in priority order
    votes = {}
    for voter in voters:
        print(voter)
        vote = ""
        for i in range(num_winners):
            for raw_vote in raw_votes[voter]:  # keys are candidates
                if raw_votes[voter][raw_vote] == str(i):
                    print(voter, "preference", i, "is", raw_vote)
                    vote = ''.join([vote, letters[loved_ones.index(raw_vote)]])
                    votes[voter] = vote
        print("Vote is", vote)

    # return summary, winners from stv tally
    return stv.tallySTV(votes, issue, 1)



import sys
import os.path
import random

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from lib.plugins import stv

letters = ['a','b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

caps = ["AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK"]

def random_vote(length, bin_selector, weights):
    ret = ""
    letters_available = letters[:]
    for i in range(length):
        # print(len(letters_available), "letters available")
        bin = bin_selector(letters_available, weights)
        letter = letters_available[bin]
        ret = ret + letter
        letters_available.remove(letter)
    return ret


def select_uniform(letters_available, weights):
    rand = random.random()
    delta = float(1)/len(letters_available)
    return int(rand/delta)

def select_ballot_order(letters_available, weights):
    sum_wts = 0
    for letter in letters_available:
        sum_wts += weights[letter]
    n_wts = len(letters_available)
    print("sum wts", sum_wts)
    # Generate normalized weights
    wt = []
    for i in range(n_wts):
        wt.append(weights[letters_available[i]] / float(sum_wts))

    # Generate random value and compute bin
    rand = random.random()
    i = 0
    cum = 0.0
    done = False
    retval = None
    while not done:
        cum += wt[i]
        if cum > rand:
            done = True
            retval = i
        i += 1
    return retval

# test stv tally - 5 winners among 10 candidates
# Create test issue. Issue has list of candidates that just have name properties.
issue = {}
issue['type'] = 'stv5'
candidate_names = "bob", "esther", "frank", "alfred", "maria",\
    "james", "roberta", "alice", "elena", "anna"
issue['candidates'] = {}
# candidates is a list of dicts with just 'name' property - one for each candidate
candidate_list = []
for candidate in candidate_names:
    new_candidate = {}
    new_candidate['name'] = candidate
    candidate_list.append(new_candidate)
issue['candidates'] = candidate_list
#
# The following example currently results in 'very low quota'
# internal error in stv.
#
# Generate identical votes, all ordering the candidates as they appear
# in the list so bob is everyone's first choice, etc.
num_voters = 8
votes = {}
for i in range(num_voters):
    votes[str(i)] = "abcde"
print("Uniform preference election results")
#summary, winners = stv.tallySTV(votes, issue, 2)
#print(summary, winners)
#
# Probably orrect behavior but should be documented or if possible fixed.
#
# Uniform random votes
votes = {}
for i in range(num_voters):
    votes[str(i)] = random_vote(5, select_uniform, None)

print("Random election results")
summary, winners = stv.tallySTV(votes, issue, 2)
print(summary, winners)

#
# 10,9, ..., 1 weights for candidates
wt = {}
for i in range(10):
    wt[letters[i]] = 10 - i
votes = {}
for i in range(num_voters):
    votes[str(i)] = random_vote(5, select_ballot_order, wt)

print("weighted election results")
summary, winners = stv.tallySTV(votes, issue, 2)
print(summary, winners)


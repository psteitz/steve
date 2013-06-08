#####
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#####
#
# steve.py -- shared code for Apache Steve
#

import sys
import os
import hashlib
import re
import time

SCRIPT = os.path.basename(sys.argv[0])


def get_input_line(prompt, quittable=False):
  "Prompt and fetch a line of input."

  if quittable:
    prompt += ' (q=quit)'
  prompt += ': '
  while True:
    line = raw_input(prompt).strip()
    if quittable and line == 'q':
      sys.exit(0)
    if line:
      return line
    # loop until we get an answer


def get_group(fname):
  "Return the group of voters, as a set of email addresses."

  group = set()
  for line in open(fname).readlines():
    i = line.find('#')
    if i >= 0:
      line = line[:i]
    line = line.strip()
    if not line:
      continue
    if '@' not in line:
      print '%s: voter must be an Internet e-mail address.' % (SCRIPT,)
      sys.exit(1)
    group.add(line)

  return group


def filestuff(fname):
  "Compute a unique key for FNAME based on its file info."
  s = os.stat(fname)
  return '%d:%d' % (s.st_ino, s.st_mtime)


def get_hash_of(datum):
  "Compute the (hex) MD5 hash of the string DATUM."
  return hashlib.md5(datum).hexdigest()


def hash_file(fname):
  "Compute the (hex) MD5 hash of the file FNAME."
  return get_hash_of(open(fname).read())


_RE_TALLY = re.compile('] (\\S+) (\\S+)$')

def read_tally(fname):
  result = { }
  for line in open(fname).readlines():
    match = _RE_TALLY.search(line)
    if match:
      result[match.group(1)] = match.group(2)
    else:
      print 'WARNING: Invalid vote in tally:', line

  return result


def found_in_group(voter, fname):
  "Returns True if the given VOTER is in the group specified in FNAME."
  group = get_group(fname)
  return voter in group


def get_date():
  "Format and return the current time."
  return time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime())


def contains_duplicates(s):
  "Returns True if any characters in S are duplicated."
  return len(set(s)) != len(s)


def not_valid(votes, valid):
  "Returns True if any vote in VOTES is not in VALID."
  for v in votes:
    if v not in valid:
      return True
  return False


def randomize(text):
  ### todo

  prolog = [ ]
  choices = [ ]
  epilog = [ ]

  return prolog, choices, epilog


def ballots(text):
  ### todo

  ballots = [ ]

  return ballots

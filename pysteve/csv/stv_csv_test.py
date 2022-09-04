

import csv
import stv_csv


# test validate
# Load the test file
good_records = []
errors = {}
input_file = csv.DictReader(open('test-votes.csv'))
for record in input_file:
    good, error = stv_csv.validate(record)
    if good:
        good_records.append(record)
    else:
        errors[record] = error
print(len(good_records))
print(len(errors))
for record in errors:
    print(str(record) + " : " + str(errors[record]))




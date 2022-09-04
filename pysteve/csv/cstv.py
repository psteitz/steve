import argparse
import stv_csv

parser = argparse.ArgumentParser(description='Command line options.')
parser.add_argument('-f', '--file', dest='votes_path',
                    type=str, help='Path to csv votes file')
parser.add_argument('-n', '--num-winners', dest='num_winners',
                    type=int, help='Number of winners')
args = parser.parse_args()

num_winners = args.num_winners
votes_path = args.votes_path

print("Starting election with " + str(num_winners) +
      " winners using votes from " + votes_path)

summary, winners = stv_csv.run(num_winners, votes_path)
print(summary)
print(winners)
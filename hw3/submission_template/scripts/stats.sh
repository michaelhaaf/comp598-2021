#!/bin/sh



# Input: ($1) an error message
# Output: terminates the script, provides error message & script usage guide
bail_out() {
	message=$1
	echo "Usage: ./stats.sh filename" >&2
	echo "Error message: ${message}" >&2
	exit 1
}

datafile=$1

[ -f "$datafile" ] || bail_out "Invalid data file provided: ${datafile}"
[ "$(wc -l "$datafile")" -lt 10000 ] || bail_out "needs to be more than 10000 lines"



# input: a tweet file (similar to hw1)
# output: 
# - if less than 10,000 lines, an error message
# - else: 
# - number of lines
# - first line of the file
# - number of lines in the last 10,000 rows of the file that contain "potus" (case-insensitive)
# - rows 100-200 (inclusive) how many contain the word "fake"

# e.g. output
# $ stats.sh sample.csv
# 1000001
# col_1, col_2, col_3, col_4
# 1234
# 56


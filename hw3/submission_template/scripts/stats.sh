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

# Error handling
[ -f "$datafile" ] || bail_out "Invalid data file provided: ${datafile}"
[ "$(cat $datafile | wc -l)" -lt 10000 ] && bail_out "file '${datafile}' needs to have at least 10000 lines of data"

# report number of lines
echo "$(cat $datafile | wc -l)" 

# report first line of the file
cat $datafile | head -n 1

# report number of lines in the last 10,000 rows of the file that contain "potus" (case-insensitive)
tail -n 10000 $datafile | grep -i "potus" | wc -l

# - rows 100-200 (inclusive) how many contain the word "fake" (assuming case-sensitive)
head -n 200 $datafile | tail -n 101 | grep "fake" | wc -l

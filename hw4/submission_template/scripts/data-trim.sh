#!/bin/bash

# trim data by date.

# usage:
# $ ./data-trim.sh filename
#

# where:
# - filename is a .csv file
# - filename has a date column of the format "mm/dd/yyyy hh:mm:ss"

# behavior:
# - creates a new .csv file with the data trimmed to only data from 2020
# - uses grep to find lines with the following pattern: "xx/yy/2020" (xx and yy are variable)

datafile=$1
filename="$(echo "$datafile" | rev | cut -f 2- -d '.' | rev)"

year="2020"
regex="^[[:digit:]]+,[0-9]{2}/[0-9]{2}/$year [0-9]{2}:[0-9]{2}:[0-9]{2} [P|A]M"
grep -E "$regex" "$datafile"  > "$filename-trimmed.csv"



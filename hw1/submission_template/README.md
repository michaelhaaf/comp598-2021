There are tweets in our dataset that, while distinct tweets, are clearly duplicate in content -- these tweets are represented more than once in our dataset, distorting our count. For example, the 10th and 11th tweets in dataset.tsv are identical save for the correction of a single typo. Since the typo has nothing to do with mentioning "Trump" or not, this tweet is overrepresented in our analysis (counted "False" twice). 
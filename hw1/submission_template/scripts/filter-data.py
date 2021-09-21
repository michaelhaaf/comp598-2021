import pandas as pd

data_dir = "../data/"
number_of_tweets = 10000

# grab first 10k
dataset = pd.read_csv(data_dir + "IRAhandle_tweets_1.csv").head(number_of_tweets)
# filter by English
dataset = dataset[dataset['language'].eq("English")]
# filter by question
dataset = dataset[~dataset['content'].str.contains("?", regex=False)]
# filter columns (only keep: tweet_id, publish_date, content)
dataset = dataset[['tweet_id', 'publish_date', 'content']]

dataset.to_csv("../data/initial_filtered_dataset.tsv", sep="\t", index=False)

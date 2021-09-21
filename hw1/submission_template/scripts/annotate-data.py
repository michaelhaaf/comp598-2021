import pandas as pd
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')

data_dir = "../data/"
dataset = pd.read_csv(data_dir + "initial_filtered_dataset.tsv", sep="\t")

# Add "T/F" column based on following regex condition:
#   "Trump" preceded by start of line OR nonalphanumeric character AND
#   "Trump" followed by end of line OR nonalphanumeric character
dataset['trump_mention'] = dataset['content'].str.contains("(^|[^a-zA-Z0-9])Trump($|[^a-zA-Z0-9])", regex=True)

dataset.to_csv(data_dir + "dataset.tsv", sep="\t", index=False)
dataset.to_csv("../dataset.tsv", sep="\t", index=False)


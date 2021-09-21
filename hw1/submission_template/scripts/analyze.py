import pandas as pd
import math

data_dir = "../data/"
dataset = pd.read_csv(data_dir + "dataset.tsv", sep="\t")

true_count = dataset['trump_mention'].value_counts()[True]
total_count = dataset.shape[0]
fraction = true_count / total_count
fraction = math.trunc(10.0 ** 3 * fraction) / 10 ** 3

output = pd.DataFrame({"result": ["frac-trump-mentions"], "value": [fraction]})
output.to_csv(data_dir + "results.tsv", index=False, sep="\t")
output.to_csv("../results.tsv", index=False, sep="\t")

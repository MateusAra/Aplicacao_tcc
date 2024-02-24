import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import seaborn as sb
from sklearn.cluster import KMeans


data_frame = pd.read_csv("Dados.csv")

kmeans = KMeans(n_clusters=3, random_state=0)

X = np.array(data_frame.drop("Name", axis=1))

data_frame["K-classes"] = kmeans.fit(X).labels_

clusters = data_frame.values.tolist()

result = [line for line in clusters if line[4] == 1 or line[4] == 2]

print(result)

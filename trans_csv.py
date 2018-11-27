import pandas as pd


df = pd.read_csv("./QSRanking.csv")

df.T.to_csv("./QS_Ranking.csv", header=None)
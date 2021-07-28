import pandas as pd
from sklearn.neighbors import NearestNeighbors

class Clustering:

    def __init__(self):

        df = pd.read_csv("./dataset/train.csv")
        self.rows = [[row.user_id, row.item_id, row.rating] for row in df.itertuples()]

    def clustering(self):
        #kの数, 総当り, コサイン類似度
        nn = NearestNeighbors(n_neighbors = 10, algorithm = "brute", metric = "cosine")
        nn_model = nn.fit(self.rows[1:])
        #https://career-tech.biz/2020/02/24/knn-movie-userbase/
        distances, indices = nn_model.kneighbors(self.rows[0], 10)
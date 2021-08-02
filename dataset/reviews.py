import pandas as pd

class Reviews:

    def __init__(self):

        with open("./assets/reviews.json", "r") as f:

            df = pd.read_json(f)
            self.allreview = {}
            self.asinList = []

            for row in df.itertuples():
                reviewerId = row.reviews["reviewerID"]
                asin = row.reviews["asin"]
                if reviewerId not in self.allreview:
                    self.allreview[reviewerId] = {}
                #helpful(レビューが役に立ったかの判定数)はレビューによって異なる なので判定数の半分より役に立った判定が多ければ1 半分以下なら0とする
                #overallは音楽に対する評価点
                helpful = row.reviews["helpful"]
                self.allreview[reviewerId][asin] = {"overall": row.reviews["overall"], "helpful": 1 if helpful[1] / 2 < helpful[0] else 0}
                if asin not in self.asinList:
                    self.asinList.append(asin)

            #print(self.allreview)
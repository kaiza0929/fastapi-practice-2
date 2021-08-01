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
                #helpfulは[x, y]レビューを見た人の内x人中y人が役に立ったか?(後で使う?)
                #overallは音楽に対する評価点
                self.allreview[reviewerId][asin] = row.reviews["overall"]
                if asin not in self.asinList:
                    self.asinList.append(asin)
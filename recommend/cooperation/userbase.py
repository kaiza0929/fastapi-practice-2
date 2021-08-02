import numpy as np

class UserBase:

    @classmethod
    def recommend(self, reviews, targetReviewerId, asinList):

        targetReviewerReviewVector = self.createReviewVector(reviews[targetReviewerId], asinList)

        similarites = {}

        for reviewerId in reviews:
            if reviewerId == targetReviewerId:
                pass
            reviewVector = self.createReviewVector(reviews[reviewerId], asinList)
            #アイテムベースだと{対象ユーザーが購入したアイテム1のID: {比較対象アイテム1: 類似度, 比較対象アイテム2: 類似度,..},..}になりそう
            similarites[reviewerId] = np.dot(targetReviewerReviewVector, reviewVector) / (np.linalg.norm(targetReviewerReviewVector) * np.linalg.norm(reviewVector))
            reviews[targetReviewerId]["overall"] = targetReviewerReviewVector
            reviews[reviewerId]["overall"] = reviewVector

        topSimilarities = sorted(similarites.items(), key = lambda tup: tup[1], reverse = True)[1:11]

        #正規化定数 ユーザー類似度の和の逆数
        normalizingConstant = 1 / sum([tup[1] for tup in topSimilarities])
        recommendedItems = {}

        for i in range(len(asinList)):
            #対象ユーザーが未評価のアイテム
            if asinList[i] not in reviews:
                #推薦提示対象のユーザーのあるアイテムに対する推定評価 = (あるユーザーのあるアイテムに対する評価 * あるユーザーと推薦提示対象のユーザーの類似度)の総和 * 正規化定数
                recommendedItems[asinList[i]] =sum([reviews[tup[0]]["overall"][i] * tup[1] for tup in topSimilarities]) * normalizingConstant
        
        #上位10個のアイテム
        return sorted(recommendedItems.items(), key = lambda tup: tup[1], reverse = True)[:10]

    @classmethod
    def createReviewVector(self, perReviewerReviews, asinList):
        return np.array([perReviewerReviews[asin]["overall"] if asin in perReviewerReviews else 0 for asin in asinList])
#k-means(k平均法)
#教師なし学習(unsupervised)におけるクラスタリング
#データをグループに分ける(正解ラベルがない) <=> すでに決まっているグループにデータを当てはめるのがk近傍法(正解ラベルがある)

import numpy as np
from sklearn.cluster import KMeans

class Kmeans:

    @classmethod
    def recommend(self, reviews, targetReviewerId):

        helpfulList = []
        overallList = []

        indexList = []
        index = 0

        for reviewerId in reviews:
            for asin in reviews[reviewerId]:
                helpfulList.append(reviews[reviewerId][asin]["helpful"])
                overallList.append(reviews[reviewerId][asin]["overall"])
                if reviewerId == targetReviewerId:
                    indexList.append(index)
                index += 1
            
        #クラスタ数を人が決める必要がある 
        #Tは転置行列
        predict = list(KMeans(n_clusters = 4).fit_predict(np.array([helpfulList, overallList]).T))
        print(indexList)

        clusters = {}

        for i in range(len(predict)):
            if predict[i] not in clusters:
                clusters[predict[i]] = []
            clusters[predict[i]].append((helpfulList[i], overallList[i]))
            if i in indexList:
                #推薦提示対象のユーザーがひょうかしたアイテムがどのクラスターに属しているか
                print((helpfulList[i], overallList[i]))
        
        #print(clusters[0])
        return []
        '''

        #対象ユーザーが未評価のアイテム
        noWatchedMovies = []


        #2次元配列を引数にとるので空のリストの中に入れる
        xTrain = np.array([xTrain])
        yTrain = np.array([yTrain])

        nc = KNeighborsClassifier(n_neighbors = 5)
        nc.fit(xTrain, yTrain)
            
        return []
        '''
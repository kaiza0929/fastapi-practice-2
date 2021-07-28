#メモリベース推薦
#ユーザーベース協調フィルタリング
#あるユーザーに対して、そのユーザーと嗜好が近いユーザーのデータを用いて推薦を行う。
#参考 https://yolo-kiyoshi.com/2020/09/02/post-2267/#outline__2_1_1 

import pandas as pd
import math

class CollaborativeFiltering:

    def __init__(self):

        #ルートディレクトリからの相対パス
        datas = self.parseDataframe(pd.read_csv("./dataset/train.csv"))
        self.perUserMovieScores = datas["perUserMovieScores"]
        self.movieIdList = datas["movieIdList"]

    
    def parseDataframe(self, df):

        perUserMovieScores = {}
        movieIdList = []

        for row in df.itertuples():
            userId = row.user_id
            if userId not in perUserMovieScores:
                perUserMovieScores[userId] = {}
            #{ユーザー1のid: {アイテム1のid: アイテム1の評価値, アイテム2のid: アイテム2の評価値,.. },.. }
            #評価値は1 ~ 5のどれか
            perUserMovieScores[userId][row.item_id] = row.rating
            movieIdList.append(row.item_id)

        return {"perUserMovieScores": perUserMovieScores, "movieIdList": list(set(movieIdList))}


    def getScore(self, userId, movieId, perUserMovieScores):
        
        if movieId not in perUserMovieScores[userId]:
            #推薦提示対象のユーザーがその映画を見ていない場合は0を返す
            return 0
        else:
            return perUserMovieScores[userId][movieId]


    #cos類似度を使う方法
    #sim(x, y)は類似度関数 cos類似度はその１つ
    def calcSimilarityByCos(self, targetUserId):

        if targetUserId not in self.perUserMovieScores:
            print("指定されたユーザーIDが存在しません")
            return 

        similarities = {}

        for userId in self.perUserMovieScores:
            #ユーザーx(ここでは推薦提示対象のユーザー)の各映画に対する評価の2乗和(後に平方根を取る)
            userXscoreSumOfSquares = 0
            #ユーザーy(ここでは他のユーザー)の各映画に対する評価の2乗和(後に平方根を取る)
            userYscoreSumOfSquares = 0
            #ユーザーxのアイテムiに対する評価とユーザーyのアイテムiに対する評価の積の和
            usersScoreProductSum = 0

            for movieId in self.movieIdList:

                userXscore = self.getScore(targetUserId, movieId, self.perUserMovieScores)
                userYscore = self.getScore(userId, movieId, self.perUserMovieScores)

                usersScoreProductSum += userXscore * userYscore

                userXscoreSumOfSquares += userXscore ** 2
                userYscoreSumOfSquares += userYscore ** 2

            similarities[userId] = (usersScoreProductSum / (math.sqrt(userXscoreSumOfSquares) * math.sqrt(userYscoreSumOfSquares)))

        #[(ユーザーid, 対象ユーザーとの類似度)]
        #類似する上位x人のユーザーを取得 先頭は自身になる(cos類似度が1になる)ので飛ばす
        #x人の類似性の高いユーザーを取得 = k近傍法?(https://blog.brainpad.co.jp/entry/2017/05/23/153000)
        similarities = sorted(similarities.items(), key = lambda tup:tup[1], reverse = True)[1:6]
        print("コサイン類似度", similarities)

        #正規化定数 ユーザー類似度の和の逆数
        normalizingConstant = 1 / sum([tup[1] for tup in similarities])

        movieRecommendScores = {}

        for movieId in self.movieIdList:
            #推薦提示対象のユーザーが未評価のアイテムを探す
            if movieId not in self.perUserMovieScores[targetUserId]:
                #推薦提示対象のユーザーのあるアイテムに対する推定評価 = (あるユーザーのあるアイテムに対する評価 * あるユーザーと推薦提示対象のユーザーの類似度)の総和 * 正規化定数
                movieRecommendScores[movieId] = sum([self.getScore(tup[0], movieId, self.perUserMovieScores) * tup[1] for tup in similarities]) * normalizingConstant

        movieRecommendScores = list(sorted(movieRecommendScores.items(), key = lambda tup:tup[1], reverse = True))[:10]
        
        return [tup[0] for tup in movieRecommendScores]


    #予測精度の評価 正解との2乗誤差? 正解に何を使えばいいのかが分からない(映画の評価点?)
    def accuracyEvaluation(self):
        return 

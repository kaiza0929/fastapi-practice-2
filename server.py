from fastapi import FastAPI
from fastapi.responses import JSONResponse
from recommend.collaborative_filtering import CollaborativeFiltering
from recommend.clustering import Clustering

app = FastAPI()
collaborativeFiltering = CollaborativeFiltering()
clustering = Clustering()

@app.get("/api/collaborative")
def onGetCollaborative(userId: int):
    movieIds = collaborativeFiltering.calcSimilarityByCos(userId)
    return JSONResponse(status_code = 200, content = {"movieIds": movieIds})

@app.get("/api/clustering")
def onGetClustering(userId: int):
    clustering.clusteringUsers()
    return JSONResponse(status_code = 200, content = {})
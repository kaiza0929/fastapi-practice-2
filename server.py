from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from recommend.collaborative_filtering import CollaborativeFiltering
from recommend.clustering import Clustering

app = FastAPI()

origins = ["http://localhost:3000", "http://localhost:5000"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

collaborativeFiltering = CollaborativeFiltering()
clustering = Clustering()

@app.get("/api/collaborative")
def onGetCollaborative(userId: int):
    movies = collaborativeFiltering.calcSimilarityByCos(userId)
    return JSONResponse(status_code = 200, content = {"movies": movies})

@app.get("/api/clustering")
def onGetClustering(userId: int):
    clustering.clustering()
    return JSONResponse(status_code = 200, content = {})
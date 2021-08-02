from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dataset.reviews import Reviews
from recommend.cooperation.userbase import UserBase
from recommend.machine.unsupervised.kmeans import Kmeans

app = FastAPI()

origins = ["http://localhost:3000", "http://localhost:5000"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

reviews = Reviews()

userbase = UserBase()
kmeans = Kmeans()

@app.get("/api/reviewer")
def getreviewers():
    return {"reviewerIds": [id for id in reviews.allreview]}

@app.get("/api/reviewer/history")
def gethistroy(targetReviewerId: str = "A2IBPI20UZIR0U"):
    return {"history": reviews.allreview[targetReviewerId]}

@app.get("/api/music/recommend/cooperation/userbase")
def recommend(targetReviewerId: str = "A2IBPI20UZIR0U"):
    return {"recommended": userbase.recommend(reviews.allreview, targetReviewerId, reviews.asinList)}

@app.get("/api/music/recommend/machine/unsupervised/kmean")
def recommend(targetReviewerId: str = "A2IBPI20UZIR0U"):
    kmeans.recommend(reviews.allreview, targetReviewerId)
    return []
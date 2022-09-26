# Importing necessary libraries
from tokenize import String
import uvicorn
import pickle
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initializing the fast API server
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loading up the trained model


def prediction(lst):
    filename = './model/predictor.pkl'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst]).tolist()[0]
    return pred_value


# Defining the model input types
class Item(BaseModel):
    id: int
    month: int
    day: int
    time: int


# Setting up the home route
@app.get("/")
def read_root():
    return {"data": "Let's predict busy times"}


# Setting up the prediction route
@app.post("/prediction")
async def get_predict(data: Item):
    feature_list = []

    feature_list.append(int(data.id))
    feature_list.append(int(data.month))
    feature_list.append(int(data.day))
    feature_list.append(int(data.time))

    pred_value = prediction(feature_list)

    return {
        "data": {
            'prediction': pred_value
        }
    }


# Configuring the server host and port
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')

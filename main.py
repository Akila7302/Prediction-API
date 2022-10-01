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


# Loading up the trained model for get the busy count
def prediction(lst):
    filename = './model/predictor.pkl'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst]).tolist()[0]
    return pred_value


# Loading up the trained model for get the best time
def timesuggest(lst):
    filename = './model/bestTime.pkl'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst]).tolist()[0]
    return pred_value


# Loading up the trained model for get the best month
def monthsuggest(lst):
    filename = './model/bestMonth.pkl'
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


# Setting up the prediction route for busy count
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
            'prediction': pred_value,
            'status': 'Closed' if pred_value == 0 else 'Busy' if pred_value >= 75 else ('Not Too Busy' if pred_value < 75 and pred_value > 20 else 'Not Busy'),
        }
    }


# Setting up the prediction route for best time
@app.post("/timesuggest")
async def get_predict(data: Item):
    feature_list = []

    feature_list.append(int(data.id))
    feature_list.append(int(data.month))
    feature_list.append(int(data.day))
    feature_list.append(int(data.time))

    pred_value = timesuggest(feature_list)

    return {
        "data": {
            'prediction': pred_value,
            'best_time': '6AM' if pred_value == 6
            else '7AM' if pred_value == 7
            else '8AM' if pred_value == 8
            else '9AM' if pred_value == 9
            else '10AM' if pred_value == 10
            else '11AM' if pred_value == 11
            else '12PM' if pred_value == 12
            else '1PM' if pred_value == 13
            else '2PM' if pred_value == 14
            else '3PM' if pred_value == 15
            else '4PM' if pred_value == 16
            else '5PM' if pred_value == 17
            else '6PM' if pred_value == 18
            else '7PM' if pred_value == 19
            else '8PM' if pred_value == 20
            else 'Can visit anytime' if pred_value == 24
            else 'It is not the best time to visit!',
        }
    }


# Setting up the prediction route for best time
@app.post("/monthsuggest")
async def get_predict(data: Item):
    feature_list = []

    feature_list.append(int(data.id))
    feature_list.append(int(data.month))
    feature_list.append(int(data.day))
    feature_list.append(int(data.time))

    pred_value = monthsuggest(feature_list)

    return {
        "data": {
            'prediction': pred_value,
            'best_month': 'All months' if pred_value == 1
            else 'May-June' if pred_value == 2
            else 'April-September' if pred_value == 3
            else 'November-April' if pred_value == 4
            else 'March-May' if pred_value == 5
            else 'December-April' if pred_value == 6
            else 'January-September' if pred_value == 7
            else 'December-March' if pred_value == 8
            else 'June-July' if pred_value == 9
            else 'July-September' if pred_value == 10
            else 'January-March' if pred_value == 11
            else 'November-May' if pred_value == 12
            else 'February-September' if pred_value == 13
            else 'September-December' if pred_value == 14
            else 'November-March' if pred_value == 15
            else 'March-October' if pred_value == 16
            else 'January-April' if pred_value == 17
            else 'January-May' if pred_value == 18
            else 'October-January' if pred_value == 19
            else 'February-April' if pred_value == 20
            else 'May-September' if pred_value == 21
            else 'February-June' if pred_value == 22
            else 'December-January' if pred_value == 23
            else 'Temporarily closed' if pred_value == 50
            else '',
        }
    }


# Configuring the server host and port
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')

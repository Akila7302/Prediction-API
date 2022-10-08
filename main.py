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


# Loading up the trained model for get the alternative locations
def locationsuggest(lst):
    filename = './model/altlocation.pkl'
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
            else 'Can not visit on choosen day/month',
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


# Setting up the prediction route for best time
@app.post("/locationsuggest")
async def get_predict(data: Item):
    feature_list = []

    feature_list.append(int(data.id))
    feature_list.append(int(data.month))
    feature_list.append(int(data.day))
    feature_list.append(int(data.time))

    pred_value = locationsuggest(feature_list)

    return {
        "data": {
            'prediction': pred_value,
            'best_location': ["Bluefield Tea Gardens", "Bomburu Ella Waterfall", "Devon Falls", "Gregory Lake", "Hortan Plains", "Kothmale Dam", "Laxapana Falls", "Piduruthalagala", "Ramboda Falls", "Victoria Park"]
            if pred_value == 181
            else ["Archaeologiical Measeum", "Isurumuniya", "Jethawanaramaya", "Kalu Diya Pokuna Pond", "Lovamahapaya", "Mihintale", "Ranmasu Uyana", "Ritigala Forest Monastery", "Ruwanweliseya", "Sri Maha Bodhiya", "Thuparamaya"]
            if pred_value == 22
            else ["Baobab Tree", "Mannar Bird's Sanctuary", "Madhu Church", "Mannar Fort", "Thanthirimale", "The Doric at Arippu", "Thiruketheeswaram Kovil", "Yodha Wewa"]
            if pred_value == 133
            else ["Dambulla Royal Cave Temple", "Nalanda Gedige", "Pidurangala Royal Cave Temple", "Sigiriya", "Wasgamuwa National Park"]
            if pred_value == 144
            else [{"Bahiravakanda Temple"}, {"Ceylon Tea Measeum"}, {"International Buddhist Measeum"}, {"Kandy Lake"}, {"Knuckles Mountain Range"}, {"Lankathilaka Temple"}, {"Peradeniya Botanical Gardens"}, {"Pinnawala Elephant Orphanage"}, {"Temple Of The Tooth Relic"}, {"Udawattekele Sanctuary"}]
            if pred_value == 115
            else ["Abhayagiriya", "Isurumuniya", "Jethawanaramaya", "Kalu Diya Pokuna Pond", "Lovamahapaya", "Mihintale", "Ranmasu Uyana", "Ritigala Forest Monastery", "Ruwanweliseya", "Sri Maha Bodhiya", "Thuparamaya"]
            if pred_value == 26
            else ["Buddangala", "Crocodile Rock", "Deegavapi", "Gal Oya National Park", "Kumana National Park", "Lahugala Magul Maha Viharaya"]
            if pred_value == 17
            else ["Ambuluwawa", "Ceylon Tea Measeum", "International Buddhist Measeum", "Kandy Lake", "Knuckles Mountain Range", "Lankathilaka Temple", "Peradeniya Botanical Gardens", "Pinnawala Elephant Orphanage", "Temple Of The Tooth Relic", "Udawattekele Sanctuary"]
            if pred_value == 118
            else ["Bogoda Wooden Bridge", "Demodara Bridge", "Dhowa Rock Temple", "Dunhinda Falls", "Fox Hill", "Muthiyangana Temple", "Katharagama Dewalaya", "St.Mark s Church"]
            if pred_value == 39
            else ["Batticaloa Eco Park", "Batticaloa Lagoon", "Batticaloa Lighthouse", "Kallady Beach", "Kallady Bridge", "Pasikudah Beach"]
            if pred_value == 410
            else ["Batticaloa Eco Park", "Batticaloa Fort", "Batticaloa Lighthouse", "Kallady Beach", "Kallady Bridge", "Pasikudah Beach"]
            if pred_value == 411
            else ["Batticaloa Eco Park", "Batticaloa Fort", "Batticaloa Lagoon", "Kallady Beach", "Kallady Bridge", "Pasikudah Beach"]
            if pred_value == 412
            else ["Dutch Reformed Church", "Galle Dutch Fort", "Galle Harbour", "Galle Maritime Measeum", "Galle Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Jungle Beach", "Koggala Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 613
            else ["Colombo National Measeum", "Sri Lanka Planatarium", "Gangaramaya", "Mountlavinia Beach", "National Railway Measeum", "Pettah Floating Market", "Viharamahadevi Park"]
            if pred_value == 514
            else ["Hambanthota Hotsprings", "Mulkirigala Rock Monastery", "Sithulpawwa Temple", "Tangalle Beach", "Yala National Park"]
            if pred_value == 815
            else ["Abardeen Falls", "Castlereigh Reservoir", "Ceylon Tea Trails", "Christ Church Warleigh", "Devon Falls", "Horton Plains", "Laxapana Falls", "Mlesna Tea Castle", "Sri Padaya"]
            if pred_value == 2116
            else ["Arugambaybeach", "Crocodile Rock", "Deegavapi", "Gal Oya National Park", "Kumana National Park", "Lahugala Magul Maha Viharaya"]
            if pred_value == 117
            else ["Katharagama Dewalaya", "Katharagama Kiri Vehera", "Nine Arches Bridge", "Udawalawa National Park", "Yala National Park"]
            if pred_value == 1618
            else ["Dambakolapatuna Temple", "Delft Island", "Jaffna Fort", "Jaffna Library", "Keerimalai Hot springs", "Nagadeepa Temple", "Nallur Kovil"]
            if pred_value == 919
            else ["Ambuluwawa", "Bahiravakanda Temple", "International Buddhist Measeum", "Kandy Lake", "Knuckles Mountain Range", "Lankathilaka Temple", "Peradeniya Botanical Gardens", "Pinnawala Elephant Orphanage", "Temple Of The Tooth Relic", "Udawattekele Sanctuary"]
            if pred_value == 1120
            else ["Beire Lake", "Colombo National Measeum", "Dutch Hospital", "Gangaramaya", "Galle Face Green", "Kelaniya Raja Maha Vihara", "Lotus Tower", "Mountlavinia Beach", "National Railway Measeum", "Pettah Floating Market", "Sri Lanka Planatarium", "Viharamahadevi Park"]
            if pred_value == 521
            else ["Beire Lake", "Dutch Hospital", "Gangaramaya", "Galle Face Green", "Kelaniya Raja Maha Vihara", "Lotus Tower", "Mountlavinia Beach", "National Railway Measeum", "Pettah Floating Market", "Sri Lanka Planatarium", "Viharamahadevi Park"]
            if pred_value == 522
            else ["Beire Lake", "Colombo National Measeum", "Dutch Hospital", "Gangaramaya", "Galle Face Green", "Kelaniya Raja Maha Vihara", "Lotus Tower", "Mountlavinia Beach", "National Railway Measeum", "Pettah Floating Market", "Viharamahadevi Park"]
            if pred_value == 523
            else ["Casuarina Beach", "Delft Island", "Jaffna Fort", "Jaffna Library", "Keerimalai Hot springs", "Nagadeepa Temple", "Nallur Kovil"]
            if pred_value == 924
            else ["Aluviharaya Cave Temple", "Nalanda Gedige", "Pidurangala Royal Cave Temple", "Sigiriya", "Wasgamuwa National Park"]
            if pred_value == 1425
            else ["Arugambaybeach", "Buddangala", "Crocodile Rock", "Gal Oya National Park", "Kumana National Park", "Lahugala Magul Maha Viharaya"]
            if pred_value == 126
            else ["Bambarakanda Falls", "Bogoda Wooden Bridge", "Dhowa Rock Temple", "Dunhinda Falls", "Fox Hill", "Muthiyangana Temple", "Katharagama Dewalaya", "St.Mark s Church"]
            if pred_value == 327
            else ["Abardeen Falls", "Bluefield Tea Gardens", "Bomburu Ella Waterfall", "Gregory Lake", "Hortan Plains", "Kothmale Dam", "Laxapana Falls", "Piduruthalagala", "Ramboda Falls", "Victoria Park"]
            if pred_value == 1828
            else ["Bambarakanda Falls", "Bogoda Wooden Bridge", "Demodara Bridge", "Dhowa Rock Temple", "Fox Hill", "Muthiyangana Temple", "Katharagama Dewalaya", "St.Mark s Church"]
            if pred_value == 329
            else ["Benthota Beach", "Galle Dutch Fort", "Galle Harbour", "Galle Maritime Measeum", "Galle Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Jungle Beach", "Koggala Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 630
            else ["Koneswaram Kovil", "Marble Beach", "Navel History Measeum", "Nilaveli Beach", "Pigeon Island", "Seruwawila Temple", "Trincomalee Harbour", "Uppuveli Beach"]
            if pred_value == 2231
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Harbour", "Galle Maritime Measeum", "Galle Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Jungle Beach", "Koggala Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 632
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Dutch Fort", "Galle Maritime Measeum", "Galle Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Jungle Beach", "Koggala Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 633
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Dutch Fort", "Galle Harbour", "Galle Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Jungle Beach", "Koggala Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 634
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Dutch Fort", "Galle Harbour", "Galle Maritime Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Jungle Beach", "Koggala Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 635
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Dutch Fort", "Galle Harbour", "Galle Maritime Measeum", "Galle Measeum", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Jungle Beach", "Koggala Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 636
            else ["Kings Counsil Chamber", "Kirivehera", "Lotus Pond Polonnaruwa", "Minneriya Park", "Nissankalathamandapaya", "Parakrama Samudraya", "Pothgul Viharaya", "Sathmal Prasadaya", "Somawathiya", "Statue Of King Prakramabahu", "Vatadage"]
            if pred_value == 1937
            else ["Beire Lake", "Colombo National Measeum", "Dutch Hospital", "Galle Face Green", "Kelaniya Raja Maha Vihara", "Lotus Tower", "Mountlavinia Beach", "National Railway Measeum", "Pettah Floating Market", "Sri Lanka Planatarium", "Viharamahadevi Park"]
            if pred_value == 538
            else ["Abardeen Falls", "Bluefield Tea Gardens", "Bomburu Ella Waterfall", "Devon Falls", "Hortan Plains", "Kothmale Dam", "Laxapana Falls", "Piduruthalagala", "Ramboda Falls", "Victoria Park"]
            if pred_value == 1839
            else ["Attanagalla Raja Maha Viharaya", "Colombo National Measeum", "Colombo Planatarium", "Henerathgoda Botanical Garden", "Lenawara Rajamaha Viharaya", "National Railway Measeum Colombo"]
            if pred_value == 740
            else ["Birds Research Center", "Mulkirigala Rock Monastery", "Sithulpawwa Temple", "Tangalle Beach", "Yala National Park"]
            if pred_value == 841
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Dutch Fort", "Galle Harbour", "Galle Maritime Measeum", "Galle Measeum", "Galle Turtle Hatchery", "Japaneese Peace Pagoda", "Jungle Beach", "Koggala Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 642
            else ["Bodhinagala Forest Hermitage", "Fa Hien Caves", "Kaluthara Beach", "Kalutara Bodhiya", "Richmond Castle", "Thudugala Ella", "West Coast Tattoo Studio"]
            if pred_value == 1043
            else ["Abardeen Falls", "Bluefield Tea Gardens", "Bomburu Ella Waterfall", "Devon Falls", "Gregory Lake", "Kothmale Dam", "Laxapana Falls", "Piduruthalagala", "Ramboda Falls", "Victoria Park"]
            if pred_value == 1844
            else ["Ambuluwawa", "Bahiravakanda Temple", "Ceylon Tea Measeum", "Kandy Lake", "Knuckles Mountain Range", "Lankathilaka Temple", "Peradeniya Botanical Gardens", "Pinnawala Elephant Orphanage", "Temple Of The Tooth Relic", "Udawattekele Sanctuary"]
            if pred_value == 1145
            else ["Abhayagiriya", "Archaeologiical Measeum", "Jethawanaramaya", "Kalu Diya Pokuna Pond", "Lovamahapaya", "Mihintale", "Ranmasu Uyana", "Ritigala Forest Monastery", "Ruwanweliseya", "Sri Maha Bodhiya", "Thuparamaya"]
            if pred_value == 246
            else ["Casuarina Beach", "Dambakolapatuna Temple", "Delft Island", "Jaffna Library", "Keerimalai Hot springs", "Nagadeepa Temple", "Nallur Kovil"]
            if pred_value == 947
            else ["Casuarina Beach", "Dambakolapatuna Temple", "Delft Island", "Jaffna Fort", "Keerimalai Hot springs", "Nagadeepa Temple", "Nallur Kovil"]
            if pred_value == 948
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Dutch Fort", "Galle Harbour", "Galle Maritime Measeum", "Galle Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Jungle Beach", "Koggala Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 649
            else ["Abhayagiriya", "Archaeologiical Measeum", "Isurumuniya", "Kalu Diya Pokuna Pond", "Lovamahapaya", "Mihintale", "Ranmasu Uyana", "Ritigala Forest Monastery", "Ruwanweliseya", "Sri Maha Bodhiya", "Thuparamaya"]
            if pred_value == 250
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Dutch Fort", "Galle Harbour", "Galle Maritime Measeum", "Galle Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Koggala Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 651
            else ["Batticaloa Eco Park", "Batticaloa Fort", "Batticaloa Lagoon", "Batticaloa Lighthouse", "Kallady Bridge", "Pasikudah Beach"]
            if pred_value == 452
            else ["Batticaloa Eco Park", "Batticaloa Fort", "Batticaloa Lagoon", "Batticaloa Lighthouse", "Kallady Beach", "Pasikudah Beach"]
            if pred_value == 453
            else ["Dutch Church Kalpitiya", "Kite Center Sri Lanka", "Kudawa Beach", "Munneswaram Kovil", "Wilpaththu National Park"]
            if pred_value == 2054
            else ["Bodhinagala Forest Hermitage", "Fa Hien Caves", "Hollycross Church", "Kalutara Bodhiya", "Richmond Castle", "Thudugala Ella", "West Coast Tattoo Studio"]
            if pred_value == 1055
            else ["Bambarakanda Falls", "Bogoda Wooden Bridge", "Demodara Bridge", "Dhowa Rock Temple", "Dunhinda Falls", "Fox Hill", "Muthiyangana Temple", "St.Mark s Church"]
            if pred_value == 1656
            else ["Gal Viharaya", "Kirivehera", "Lotus Pond Polonnaruwa", "Minneriya Park", "Nissankalathamandapaya", "Parakrama Samudraya", "Pothgul Viharaya", "Sathmal Prasadaya", "Somawathiya", "Statue Of King Prakramabahu", "Vatadage"]
            if pred_value == 1957
            else ["Gal Viharaya", "Kings Counsil Chamber", "Lotus Pond Polonnaruwa", "Minneriya Park", "Nissankalathamandapaya", "Parakrama Samudraya", "Pothgul Viharaya", "Sathmal Prasadaya", "Somawathiya", "Statue Of King Prakramabahu", "Vatadage"]
            if pred_value == 1958
            else ["Ambuluwawa", "Bahiravakanda Temple", "Ceylon Tea Measeum", "International Buddhist Measeum", "Kandy Lake", "Lankathilaka Temple", "Peradeniya Botanical Gardens", "Pinnawala Elephant Orphanage", "Temple Of The Tooth Relic", "Udawattekele Sanctuary"]
            if pred_value == 1159
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Dutch Fort", "Galle Harbour", "Galle Maritime Measeum", "Galle Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Jungle Beach", "Sinharaja Forest", "Unawatuna"]
            if pred_value == 660
            else ["Fort Fedric", "Marble Beach", "Navel History Measeum", "Nilaveli Beach", "Pigeon Island", "Seruwawila Temple", "Trincomalee Harbour", "Uppuveli Beach"]
            if pred_value == 2261
            else ["Arugambaybeach", "Buddangala", "Crocodile Rock", "Deegavapi", "Gal Oya National Park", "Lahugala Magul Maha Viharaya"]
            if pred_value == 162
            else ["Ambuluwawa", "Bahiravakanda Temple", "Ceylon Tea Measeum", "International Buddhist Measeum", "Kandy Lake", "Knuckles Mountain Range", "Peradeniya Botanical Gardens", "Pinnawala Elephant Orphanage", "Temple Of The Tooth Relic", "Udawattekele Sanctuary"]
            if pred_value == 1163
            else ["Abardeen Falls", "Bluefield Tea Gardens", "Bomburu Ella Waterfall", "Devon Falls", "Gregory Lake", "Hortan Plains", "Kothmale Dam", "Piduruthalagala", "Ramboda Falls", "Victoria Park"]
            if pred_value == 1864
            else ["Gal Viharaya", "Kings Counsil Chamber", "Kirivehera", "Minneriya Park", "Nissankalathamandapaya", "Parakrama Samudraya", "Pothgul Viharaya", "Sathmal Prasadaya", "Somawathiya", "Statue Of King Prakramabahu", "Vatadage"]
            if pred_value == 1965
            else ["Abhayagiriya", "Archaeologiical Measeum", "Isurumuniya", "Jethawanaramaya", "Kalu Diya Pokuna Pond", "Mihintale", "Ranmasu Uyana", "Ritigala Forest Monastery", "Ruwanweliseya", "Sri Maha Bodhiya", "Thuparamaya"]
            if pred_value == 266
            else ["Adams Bridge", "Baobab Tree", "Mannar Bird's Sanctuary", "Madhu Church", "Thanthirimale", "The Doric at Arippu", "Thiruketheeswaram Kovil", "Yodha Wewa"]
            if pred_value == 1367
            else ["Fort Fedric", "Koneswaram Kovil", "Navel History Measeum", "Nilaveli Beach", "Pigeon Island", "Seruwawila Temple", "Trincomalee Harbour", "Uppuveli Beach"]
            if pred_value == 2268
            else ["Hiriketiya Beach", "Medawatta Beach", "Mirissa Beach", "Paraviduwa Temple", "Point Dewundara", "Snake Farm", "Star Fort", "Weligama Beach"]
            if pred_value == 1569
            else ["Gal Viharaya", "Kings Counsil Chamber", "Kirivehera", "Lotus Pond Polonnaruwa", "Nissankalathamandapaya", "Parakrama Samudraya", "Pothgul Viharaya", "Sathmal Prasadaya", "Somawathiya", "Statue Of King Prakramabahu", "Vatadage"]
            if pred_value == 1970
            else ["Matara Beach Park", "Hiriketiya Beach", "Medawatta Beach", "Paraviduwa Temple", "Point Dewundara", "Snake Farm", "Star Fort", "Weligama Beach"]
            if pred_value == 1571
            else ["Beire Lake", "Colombo National Measeum", "Dutch Hospital", "Gangaramaya", "Galle Face Green", "Kelaniya Raja Maha Vihara", "Lotus Tower", "National Railway Measeum", "Pettah Floating Market", "Sri Lanka Planatarium", "Viharamahadevi Park"]
            if pred_value == 572
            else ["Birds Research Center", "Hambanthota Hotsprings", "Sithulpawwa Temple", "Tangalle Beach", "Yala National Park"]
            if pred_value == 873
            else ["Dutch Church Kalpitiya", "Kalpitiya Diving Center", "Kite Center Sri Lanka", "Kudawa Beach", "Wilpaththu National Park"]
            if pred_value == 2074
            else ["Bambarakanda Falls", "Bogoda Wooden Bridge", "Demodara Bridge", "Dhowa Rock Temple", "Dunhinda Falls", "Fox Hill", "Katharagama Dewalaya", "St.Mark s Church"]
            if pred_value == 375
            else ["Casuarina Beach", "Dambakolapatuna Temple", "Delft Island", "Jaffna Fort", "Jaffna Library", "Keerimalai Hot springs", "Nallur Kovil"]
            if pred_value == 976
            else ["Aluviharaya Cave Temple", "Dambulla Royal Cave Temple", "Pidurangala Royal Cave Temple", "Sigiriya", "Wasgamuwa National Park"]
            if pred_value == 1477
            else ["Casuarina Beach", "Dambakolapatuna Temple", "Delft Island", "Jaffna Fort", "Jaffna Library", "Keerimalai Hot springs", "Nagadeepa Temple"]
            if pred_value == 978
            else ["Beire Lake", "Colombo National Measeum", "Dutch Hospital", "Gangaramaya", "Galle Face Green", "Kelaniya Raja Maha Vihara", "Lotus Tower", "Mountlavinia Beach", "Pettah Floating Market", "Sri Lanka Planatarium", "Viharamahadevi Park"]
            if pred_value == 579
            else ["Fort Fedric", "Koneswaram Kovil", "Marble Beach", "Nilaveli Beach", "Pigeon Island", "Seruwawila Temple", "Trincomalee Harbour", "Uppuveli Beach"]
            if pred_value == 2280
            else ["Bird watch in Muthurajawela", "Negombo Dutch Fort", "Negombo Lagoon", "Browns Beach", "St.Mary s Church", "St.Sebastian s Church", "St.Stephen s Anglican Church"]
            if pred_value == 1781
            else ["Fort Fedric", "Koneswaram Kovil", "Marble Beach", "Navel History Measeum", "Pigeon Island", "Seruwawila Temple", "Trincomalee Harbour", "Uppuveli Beach"]
            if pred_value == 2282
            else ["Gal Viharaya", "Kings Counsil Chamber", "Kirivehera", "Lotus Pond Polonnaruwa", "Minneriya Park", "Parakrama Samudraya", "Pothgul Viharaya", "Sathmal Prasadaya", "Somawathiya", "Statue Of King Prakramabahu", "Vatadage"]
            if pred_value == 1983
            else ["Deduru Oya Reservoir", "Ethagala", "Granite Samadhi Buddha statue", "Silver Temple", "Yapahuwa Rock Fortress"]
            if pred_value == 1284
            else ["Gal Viharaya", "Kings Counsil Chamber", "Kirivehera", "Lotus Pond Polonnaruwa", "Minneriya Park", "Nissankalathamandapaya", "Pothgul Viharaya", "Sathmal Prasadaya", "Somawathiya", "Statue Of King Prakramabahu", "Vatadage"]
            if pred_value == 1985
            else ["Matara Beach Park", "Hiriketiya Beach", "Medawatta Beach", "Mirissa Beach", "Point Dewundara", "Snake Farm", "Star Fort", "Weligama Beach"]
            if pred_value == 1586
            else ["Batticaloa Eco Park", "Batticaloa Fort", "Batticaloa Lagoon", "Batticaloa Lighthouse", "Kallady Beach", "Kallady Bridge"]
            if pred_value == 487
            else ["Ambuluwawa", "Bahiravakanda Temple", "Ceylon Tea Measeum", "International Buddhist Measeum", "Kandy Lake", "Knuckles Mountain Range", "Lankathilaka Temple", "Pinnawala Elephant Orphanage", "Temple Of The Tooth Relic", "Udawattekele Sanctuary"]
            if pred_value == 1188
            else ["Beire Lake", "Colombo National Measeum", "Dutch Hospital", "Gangaramaya", "Galle Face Green", "Kelaniya Raja Maha Vihara", "Lotus Tower", "Mountlavinia Beach", "National Railway Measeum", "Sri Lanka Planatarium", "Viharamahadevi Park"]
            if pred_value == 589
            else ["Aluviharaya Cave Temple", "Dambulla Royal Cave Temple", "Nalanda Gedige", "Sigiriya", "Wasgamuwa National Park"]
            if pred_value == 1490
            else ["Abardeen Falls", "Bluefield Tea Gardens", "Bomburu Ella Waterfall", "Devon Falls", "Gregory Lake", "Hortan Plains", "Kothmale Dam", "Laxapana Falls", "Ramboda Falls", "Victoria Park"]
            if pred_value == 1891
            else ["Fort Fedric", "Koneswaram Kovil", "Marble Beach", "Navel History Measeum", "Nilaveli Beach", "Seruwawila Temple", "Trincomalee Harbour", "Uppuveli Beach"]
            if pred_value == 2292
            else ["Ambuluwawa", "Bahiravakanda Temple", "Ceylon Tea Measeum", "International Buddhist Measeum", "Kandy Lake", "Knuckles Mountain Range", "Lankathilaka Temple", "Peradeniya Botanical Gardens", "Temple Of The Tooth Relic", "Udawattekele Sanctuary"]
            if pred_value == 1193
            else ["Matara Beach Park", "Hiriketiya Beach", "Medawatta Beach", "Mirissa Beach", "Paraviduwa Temple", "Snake Farm", "Star Fort", "Weligama Beach"]
            if pred_value == 1594
            else ["Gal Viharaya", "Kings Counsil Chamber", "Kirivehera", "Lotus Pond Polonnaruwa", "Minneriya Park", "Nissankalathamandapaya", "Parakrama Samudraya", "Sathmal Prasadaya", "Somawathiya", "Statue Of King Prakramabahu", "Vatadage"]
            if pred_value == 1995
            else ["Abardeen Falls", "Bluefield Tea Gardens", "Bomburu Ella Waterfall", "Devon Falls", "Gregory Lake", "Hortan Plains", "Kothmale Dam", "Laxapana Falls", "Piduruthalagala", "Victoria Park"]
            if pred_value == 1896
            else ["Bodhinagala Forest Hermitage", "Fa Hien Caves", "Hollycross Church", "Kaluthara Beach", "Kalutara Bodhiya", "Thudugala Ella", "West Coast Tattoo Studio"]
            if pred_value == 1097
            else ["Abhayagiriya", "Archaeologiical Measeum", "Isurumuniya", "Jethawanaramaya", "Kalu Diya Pokuna Pond", "Lovamahapaya", "Mihintale", "Ranmasu Uyana", "Ritigala Forest Monastery", "Sri Maha Bodhiya", "Thuparamaya"]
            if pred_value == 298
            else ["Gal Viharaya", "Kings Counsil Chamber", "Kirivehera", "Lotus Pond Polonnaruwa", "Minneriya Park", "Nissankalathamandapaya", "Parakrama Samudraya", "Pothgul Viharaya", "Somawathiya", "Statue Of King Prakramabahu", "Vatadage"]
            if pred_value == 1999
            else ["Fort Fedric", "Koneswaram Kovil", "Marble Beach", "Navel History Measeum", "Nilaveli Beach", "Pigeon Island", "Trincomalee Harbour", "Uppuveli Beach"]
            if pred_value == 22100
            else ["Aluviharaya Cave Temple", "Dambulla Royal Cave Temple", "Nalanda Gedige", "Pidurangala Royal Cave Temple", "Wasgamuwa National Park"]
            if pred_value == 14101
            else ["Deduru Oya Reservoir", "Ethagala", "Granite Samadhi Buddha statue", "Panduwasnuwara Temple", "Yapahuwa Rock Fortress"]
            if pred_value == 12102
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Dutch Fort", "Galle Harbour", "Galle Maritime Measeum", "Galle Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Jungle Beach", "Koggala Beach", "Unawatuna"]
            if pred_value == 6103
            else ["Birds Research Center", "Hambanthota Hotsprings", "Mulkirigala Rock Monastery", "Tangalle Beach", "Yala National Park"]
            if pred_value == 6104
            else ["Gal Viharaya", "Kings Counsil Chamber", "Kirivehera", "Lotus Pond Polonnaruwa", "Minneriya Park", "Nissankalathamandapaya", "Parakrama Samudraya", "Pothgul Viharaya", "Sathmal Prasadaya", "Statue Of King Prakramabahu", "Vatadage"]
            if pred_value == 21105
            else ["Abhayagiriya", "Archaeologiical Measeum", "Isurumuniya", "Jethawanaramaya", "Kalu Diya Pokuna Pond", "Lovamahapaya", "Mihintale", "Ranmasu Uyana", "Ritigala Forest Monastery", "Ruwanweliseya", "Thuparamaya"]
            if pred_value == 2106
            else ["Abardeen Falls", "Bopath Ella", "Castlereigh Reservoir", "Ceylon Tea Trails", "Christ Church Warleigh", "Devon Falls", "Horton Plains", "Laxapana Falls", "Mlesna Tea Castle"]
            if pred_value == 23107
            else ["Gal Viharaya", "Kings Counsil Chamber", "Kirivehera", "Lotus Pond Polonnaruwa", "Minneriya Park", "Nissankalathamandapaya", "Parakrama Samudraya", "Pothgul Viharaya", "Sathmal Prasadaya", "Somawathiya", "Vatadage"]
            if pred_value == 21108
            else ["Birds Research Center", "Hambanthota Hotsprings", "Mulkirigala Rock Monastery", "Sithulpawwa Temple", "Yala National Park"]
            if pred_value == 8109
            else ["Ambuluwawa", "Bahiravakanda Temple", "Ceylon Tea Measeum", "International Buddhist Measeum", "Kandy Lake", "Knuckles Mountain Range", "Lankathilaka Temple", "Peradeniya Botanical Gardens", "Pinnawala Elephant Orphanage", "Udawattekele Sanctuary"]
            if pred_value == 11110
            else ["Bodhinagala Forest Hermitage", "Fa Hien Caves", "Hollycross Church", "Kaluthara Beach", "Kalutara Bodhiya", "Richmond Castle", "West Coast Tattoo Studio"]
            if pred_value == 10111
            else ["Abhayagiriya", "Archaeologiical Measeum", "Isurumuniya", "Jethawanaramaya", "Kalu Diya Pokuna Pond", "Lovamahapaya", "Mihintale", "Ranmasu Uyana", "Ritigala Forest Monastery", "Ruwanweliseya", "Sri Maha Bodhiya"]
            if pred_value == 2112
            else ["Fort Fedric", "Koneswaram Kovil", "Marble Beach", "Navel History Measeum", "Nilaveli Beach", "Pigeon Island", "Seruwawila Temple", "Uppuveli Beach"]
            if pred_value == 24113
            else ["Buduruwagala", "Katharagama Dewalaya", "Katharagama Kiri Vehera", "Nine Arches Bridge", "Yala National Park"]
            if pred_value == 17114
            else ["Ambuluwawa", "Bahiravakanda Temple", "Ceylon Tea Measeum", "International Buddhist Measeum", "Kandy Lake", "Knuckles Mountain Range", "Lankathilaka Temple", "Peradeniya Botanical Gardens", "Pinnawala Elephant Orphanage", "Temple Of The Tooth Relic"]
            if pred_value == 11115
            else ["Benthota Beach", "Dutch Reformed Church", "Galle Dutch Fort", "Galle Harbour", "Galle Maritime Measeum", "Galle Measeum", "Galle Turtle Hatchery", "Hikkaduwa Beach", "Japaneese Peace Pagoda", "Jungle Beach", "Koggala Beach", "Sinharaja Forest"]
            if pred_value == 6116
            else ["Fort Fedric", "Koneswaram Kovil", "Marble Beach", "Navel History Measeum", "Nilaveli Beach", "Pigeon Island", "Seruwawila Temple", "Trincomalee Harbour"]
            if pred_value == 24117
            else ["Gal Viharaya", "Kings Counsil Chamber", "Kirivehera", "Lotus Pond Polonnaruwa", "Minneriya Park", "Nissankalathamandapaya", "Parakrama Samudraya", "Pothgul Viharaya", "Sathmal Prasadaya", "Somawathiya", "Statue Of King Prakramabahu"]
            if pred_value == 21118
            else ["Abardeen Falls", "Bluefield Tea Gardens", "Bomburu Ella Waterfall", "Devon Falls", "Gregory Lake", "Hortan Plains", "Kothmale Dam", "Laxapana Falls", "Piduruthalagala", "Ramboda Falls"]
            if pred_value == 20119
            else ["Beire Lake", "Colombo National Measeum", "Dutch Hospital", "Gangaramaya", "Galle Face Green", "Kelaniya Raja Maha Vihara", "Lotus Tower", "Mountlavinia Beach", "National Railway Measeum", "Pettah Floating Market", "Sri Lanka Planatarium"]
            if pred_value == 5120
            else ["Aluviharaya Cave Temple", "Dambulla Royal Cave Temple", "Nalanda Gedige", "Pidurangala Royal Cave Temple", "Sigiriya"]
            if pred_value == 15121
            else ["Dutch Church Kalpitiya", "Kalpitiya Diving Center", "Kite Center Sri Lanka", "Kudawa Beach", "Munneswaram Kovil"]
            if pred_value == 22122
            else ["Birds Research Center", "Hambanthota Hotsprings", "Mulkirigala Rock Monastery", "Sithulpawwa Temple", "Tangalle Beach"]
            if pred_value == 8123
            else ["Deduru Oya Reservoir", "Ethagala", "Granite Samadhi Buddha statue", "Panduwasnuwara Temple", "Silver Temple"]
            if pred_value == 13124
            else 'Something Went Wrong',
        }
    }

# Configuring the server host and port
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')

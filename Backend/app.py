from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal, List, Annotated
import joblib
import pandas as pd

CORSMiddleware_origins = ["*"]
class Passenger(BaseModel):
    age: Annotated[int, Field(gt=0,lte=120, description='Age of Passenger', example='16.0')]
    sibsp: Annotated[int,Field(gt=-1,description='Count of siblings or spouse of passenger',example='2')]
    parch: Annotated[int,Field(gt=-1,description='Count of parent and children of passenger',example='3')]
    sex: Annotated[Literal['male','female'], Field(description='Gender of Passenger', examples=['male','female'])]
    fare: Annotated[float, Field(gt=0, description='Fare of the passenger')]
    embarked: Annotated[Literal['C','Q','S'], Field(description='Port of Embarkation', examples=['C','Q','S'])]
    pclass: Annotated[Literal['First','Second','Third'], Field(description='Class of passenger', examples=['First','Second','Third'])]
    deck: Annotated[Literal['A','B','C','D','E','F','G'], Field(description='Passenger\'s Deck', examples=['A','B','C','D','E','F','G'])]
app = FastAPI()

@app.get('/')   
def index():
    return JSONResponse(status_code=200, content={'message':"Hello world this is a titanic survival predition api"})

@app.post('/random-forest/predict')
def rf_predict(passenger_data: Passenger):
    model_path = './models/random-forest.joblib'
    rf_model = joblib.load(model_path)
    data = passenger_data.model_dump()
    test_df = pd.DataFrame([data])
    prediction=rf_model.predict(test_df)[0]
    print(prediction)
    return JSONResponse(status_code=200, content={'prediction':prediction.item()})

@app.post('/logistic-regression/predict')
def lgr_predict(passenger_data: Passenger):
    model_path = './models/logistic-regression.joblib'
    lgr_model = joblib.load(model_path)
    data = passenger_data.model_dump()
    test_df = pd.DataFrame([data])
    prediction=lgr_model.predict(test_df)[0]
    print(prediction)
    return JSONResponse(status_code=200, content={'prediction':prediction.item()})

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from pydantic import ValidationError
from fastapi import Request

app = FastAPI()

# Load the saved pipeline
pipeline = joblib.load("model_pipeline.joblib")

# Define a Pydantic model for input data validation
class CustomerData(BaseModel):
    age: int
    gender: str
    tenure: int
    usage_frequency: int
    support_calls: int
    payment_delay: int
    subscription_type: str
    contract_length: str
    total_spend: int
    last_interaction: int

@app.post("/predict")
async def predict(request: Request, data: CustomerData):  # Include Request object
    try:
        # Convert input data to DataFrame
        input_df = pd.DataFrame([data.dict()])
        prediction = pipeline.predict(input_df)
        return {"prediction": int(prediction[0])}
    except ValidationError as e:  # Catch Pydantic validation errors
        error_message = f"Validation Error: {e}"
        print(error_message)  # Print to console for debugging
        raise HTTPException(status_code=422, detail=error_message)
    except Exception as e:
        error_message = f"An error occurred during prediction: {e}"
        print(error_message) # Log the error for debugging
        raise HTTPException(status_code=500, detail=error_message)

@app.get("/")
async def root():
    return {"message": "Customer Churn Prediction API"}
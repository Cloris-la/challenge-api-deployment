from fastapi import FastAPI, HTTPException, Request
from preprocessing.cleaning_data import preprocess
from predict.prediction import predict


app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "alive"}

@app.get("/predict")
def explain_prediction_format():
    return {
        "message": "POST to /predict with JSON like: { 'data': { 'area': 120, ... } }"
    }


@app.post("/predict")
def predict_route(request: dict):
    try:
        house_data = request.get("data")
        if not house_data:
            raise HTTPException(status_code=400, detail="Missing 'data' field")

        df_processed, warning = preprocess(house_data)

        if df_processed is None:
            raise HTTPException(status_code=400, detail=warning)

        prediction = predict(df_processed)

        response = {"prediction": prediction, "status_code": 200}
        if warning:
            response["warning"] = warning

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

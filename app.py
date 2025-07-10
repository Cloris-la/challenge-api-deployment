import sys
import os
import traceback
import uvicorn

print("🚀 Starting ImmoEliza API...")

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field, field_validator
    from typing import Optional
    import uvicorn
    
    # Import modules
    from preprocessing.cleaning_data import preprocess
    from predict.prediction import predict
    
    app = FastAPI(
        title="ImmoEliza House Price Prediction API",
        description="Simplified API - Contains only fields actually used by the model",
        version="2.0.0"
    )
    
    # Only fields actually needed by the model
    class HouseData(BaseModel):
        area: int
        property_type: str = Field(alias="property-type")
        bedrooms_number: int = Field(alias="bedrooms-number")
        zip_code: int = Field(alias="zip-code")
        
        # Optional fields
        garden: Optional[bool] = None
        swimming_pool: Optional[bool] = Field(None, alias="swimming-pool")
        terrace: Optional[bool] = None
        building_state: Optional[str] = Field(None, alias="building-state")
        parking: Optional[bool] = None
        lift: Optional[bool] = None
        epc_score: Optional[str] = Field(None, alias="epc-score")
        
        # Received but unused fields
        land_area: Optional[int] = Field(None, alias="land-area")
        garden_area: Optional[int] = Field(None, alias="garden-area")
        equipped_kitchen: Optional[bool] = Field(None, alias="equipped-kitchen")
        full_address: Optional[str] = Field(None, alias="full-address")
        furnished: Optional[bool] = None
        open_fire: Optional[bool] = Field(None, alias="open-fire")
        terrace_area: Optional[int] = Field(None, alias="terrace-area")
        facades_number: Optional[int] = Field(None, alias="facades-number")
    
    class PredictionRequest(BaseModel):
        data: HouseData
    
    class PredictionResponse(BaseModel):
        prediction: Optional[float]
        status_code: Optional[int]
    
    @app.get("/")
    def root():
        """
        Health check
        """
        return "alive"
    
    @app.get("/predict")
    def predict_info():
        """
        API Usage Guide
        """
        return {
            "message": "Use POST method to predict house prices",
            "version": "2.0.0 - Simplified API",
            "description": "Contains only fields actually used by the model for a cleaner user experience",
            
            "required_fields": {
                "area": "int - Living area in square meters (m²)",
                "property-type": "string - Property type: HOUSE | APARTMENT | OTHERS",
                "bedrooms-number": "int - Number of bedrooms",
                "zip-code": "int - Belgian postal code (1000-9999)"
            },
            "optional_fields_used_by_model": {
                "garden": "bool - Has garden",
                "swimming-pool": "bool - Has swimming pool",
                "terrace": "bool - Has terrace",
                "building-state": "string - Building condition",
                "parking": "bool - Has parking",
                "lift": "bool - Has elevator",
                "epc-score": "string - Energy certificate"
            },
            "example": {
                "data": {
                    "area": 120,
                    "property-type": "HOUSE",
                    "bedrooms-number": 3,
                    "zip-code": 1000,
                    "garden": True
                }
            }
        }
    
    @app.post("/predict", response_model=PredictionResponse)
    def predict_house_price(request: PredictionRequest):
        """
        Predict house price
        """
        try:
            from preprocessing.cleaning_data import preprocess
            from predict.prediction import predict
            
            house_data = request.data
            house_dict = house_data.model_dump(by_alias=True)
            
            print(f"🔄 Received prediction request (simplified): {house_dict}")
            
            # Preprocessing
            processed_data, preprocess_error = preprocess(house_dict)
            
            if processed_data is None:
                print(f"❌ Preprocessing failed: {preprocess_error}")
                return PredictionResponse(prediction=None, status_code=400)
            
            print(f"✅ Preprocessing successful: {processed_data.shape}")
            
            # Prediction
            predicted_price = predict(processed_data)
            
            if predicted_price is None:
                print("❌ Prediction failed")
                return PredictionResponse(prediction=None, status_code=500)
            
            print(f"✅ Prediction successful: €{predicted_price:,.2f}")
            
            return PredictionResponse(
                prediction=round(predicted_price, 2),
                status_code=200
            )
            
        except Exception as e:
            print(f"❌ Error: {e}")
            traceback.print_exc()
            return PredictionResponse(prediction=None, status_code=500)
    
    print("✅ API configuration completed")
    
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 10000))
        print(f"🎯 Starting server on port {port}")
        print(f"📖 Visit http://localhost:{port}/docs for API documentation")
        print("🎉 Users now only need to input fields actually used by the model!")
        
        uvicorn.run(app, host="0.0.0.0", port=port, reload=False)

except Exception as e:
    print(f"💥 Startup failed: {e}")
    traceback.print_exc()
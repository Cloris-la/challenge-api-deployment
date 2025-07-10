# ImmoEliza House Price Prediction API and APP

## 🏠 Project Overview

This is a **machine learning API** for predicting house prices in Belgium, developed for the real estate company "ImmoEliza". The API is built with FastAPI and deployed on Render using Docker. The interactive web interface for the **ImmoEliza House Price Prediction API**, built with Streamlit. It provides a user-friendly way to test the machine learning API.

### 🤝 Team Project Context
This project is part of a **three-person team collaboration**. Each team member developed their own implementation of the same API requirements, and build their own streamlit interactive web interface. This current API and interactive web interface is developed in the `Cloris_F_Chen_Deployment` branch to the team project.

## 🚀 Live API

**Base URL:** `https://immoeliza-api-cloris-f-chen.onrender.com`

**Interactive Documentation:** `https://immoeliza-api-cloris-f-chen.onrender.com/docs`

## 🚀 Live APP

**🌐 [Try the Interactive Demo](https://immoelizaapiclorisfchendemo-tektqwghdn2s458cdxgaxe.streamlit.app/)**

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.10 or higher
- pip package manager
- Git
- Docker (for containerized deployment)

### **Local Development Setup**
```bash
# Clone the repository
git clone https://github.com/Cloris-la/challenge-api-deployment.git
cd challenge-api-deployment

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API
python app.py
```

### **Docker Setup** (Recommended for Production)
```bash
# Build Docker image
docker build -t immoeliza-api .

# Run Docker container
docker run -p 10000:10000 immoeliza-api
```

### **Access the API**
- **Local URL**: http://localhost:10000
- **API Documentation**: http://localhost:10000/docs
- **Health Check**: http://localhost:10000/

### **Access the Application**

- **Local URL**: http://localhost:8501
- **Network URL**: http://your-local-ip:8501

### **Project Structure**
### Project Structure
```
├── app.py                      # FastAPI application
├── Aperol project/data         # Geo point data
│   └── georef-belgium-postal-codes@public.csv
├── preprocessing/
│   └── cleaning_data.py       # Data preprocessing pipeline
├── predict/
│   └── prediction.py          # ML prediction logic
├── model/
│   └── robocop_model.cbm     # Trained CatBoost model
├── requirements.txt           # Python dependencies
└── Dockerfile                # Docker configuration
└── streamlit_app.py          # streamlit interactive web interface
```

### **Dependencies**
Key dependencies include:
```
fastapi==0.115.14
uvicorn==0.35.0
pydantic==2.11.7
catboost==1.2.8
pandas==2.3.0
numpy==2.3.1
scikit-learn==1.7.0
requests==2.32.4
streamlit
requests
```

### **Environment Variables**
- `PORT`: Server port (default: 10000 for production, 8000 for development)

### **Deployment to Render**
1. **Connect GitHub Repository**:
   - Visit [render.com](https://render.com)
   - Connect your GitHub account
   - Select this repository

2. **Configure Build Settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: `Python 3`

3. **Environment Variables**:
   - `PORT`: Will be automatically set by Render

### **Testing the API**
```bash
# Health check
curl http://localhost:10000/

# Get API information
curl http://localhost:10000/predict

# Make a prediction
curl -X POST "http://localhost:10000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "data": {
         "area": 120,
         "property-type": "HOUSE",
         "bedrooms-number": 3,
         "zip-code": 1000
       }
     }'
```

### **Model Requirements**
- Ensure the trained model file `robocop_model.cbm` is in the `model/` directory
- The model expects 15 specific features (see preprocessing pipeline)

### **Troubleshooting**
- **Model loading errors**: Check if `model/robocop_model.cbm` exists
- **Import errors**: Ensure all dependencies are installed with correct versions
- **Port conflicts**: Modify the PORT environment variable
- **Memory issues**: The model requires sufficient RAM for CatBoost operations
- **Port already in use**: : Streamlit will automatically find another port
- **API connection issues**: Ensure the main API is running at the specified URL
- **Missing dependencies**: Run pip install -r requirements.txt again

## 📋 Available Endpoints

### 1. Health Check
- **Endpoint:** `GET /`
- **Description:** Check if the API server is alive
- **Response:** `"alive"`

### 2. API Information
- **Endpoint:** `GET /predict`
- **Description:** Get detailed information about how to use the prediction endpoint
- **Response:** JSON with API usage guide, required fields, and examples

### 3. House Price Prediction
- **Endpoint:** `POST /predict`
- **Description:** Predict the price of a house based on its characteristics
- **Content-Type:** `application/json`

## 📝 Request Format

### Required Fields
```json
{
  "data": {
    "area": 120,                    // int - Living area in m²
    "property-type": "HOUSE",       // string - "APARTMENT" | "HOUSE" | "OTHERS"
    "bedrooms-number": 3,           // int - Number of bedrooms
    "zip-code": 1000               // int - Belgian postal code (1000-9999)
  }
}
```

### Optional Fields (Improve Prediction Accuracy)
```json
{
  "data": {
    "area": 120,
    "property-type": "HOUSE",
    "bedrooms-number": 3,
    "zip-code": 1000,
    "garden": true,                 // bool - Has garden
    "swimming-pool": false,         // bool - Has swimming pool
    "terrace": true,                // bool - Has terrace
    "building-state": "GOOD",       // string - "NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO BE DONE UP" | "TO REBUILD"
    "parking": true,                // bool - Has parking space
    "lift": false,                  // bool - Has elevator
    "epc-score": "C"               // string - "A++" | "A+" | "A" | "B" | "C" | "D" | "E" | "F" | "G"
  }
}
```

## 📤 Response Format

### Successful Prediction
```json
{
  "prediction": 450000.00,
  "status_code": 200
}
```

### Error Response
```json
{
  "prediction": null,
  "status_code": 400  // or 500 for server errors
}
```

## 🔧 Usage Examples

### CURL Example
```bash
curl -X POST "https://immoeliza-api-cloris-f-chen.onrender.com/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "data": {
         "area": 150,
         "property-type": "HOUSE",
         "bedrooms-number": 4,
         "zip-code": 1000,
         "garden": true,
         "building-state": "GOOD"
       }
     }'
```

### Python Example
```python
import requests

url = "https://immoeliza-api-cloris-f-chen.onrender.com/predict"
data = {
    "data": {
        "area": 120,
        "property-type": "APARTMENT",
        "bedrooms-number": 2,
        "zip-code": 2000,
        "terrace": True,
        "epc-score": "B"
    }
}

response = requests.post(url, json=data)
result = response.json()
print(f"Predicted price: €{result['prediction']:,.2f}")
```

## 🏠 How to Use app

### 1. **Required Fields**
Fill in the mandatory information:
- **Living Area**: Property size in square meters
- **Property Type**: HOUSE, APARTMENT, or OTHERS
- **Bedrooms**: Number of bedrooms
- **ZIP Code**: Belgian postal code (1000-9999)

### 2. **Optional Fields** (Improve Accuracy)
Add additional details for better predictions:
- Garden, Swimming Pool, Terrace
- Parking, Elevator
- Building State, EPC Score

### 3. **Get Prediction**
- Click "Predict Price" button
- View the predicted price and analysis
- See the API request/response data

## 🏗️ Technical Architecture

### Key Features
- **FastAPI Framework:** High-performance, automatic API documentation
- **Machine Learning:** CatBoost regression model for price prediction
- **Data Validation:** Pydantic models for request/response validation
- **Docker Deployment:** Containerized application on Render
- **Error Handling:** Comprehensive error responses with status codes
- **Geographic Intelligence:** Region-based features (Brussels, Flanders, Wallonia)
- **Streamlit** - Web interface framework
- **Requests** - API communication
- **Python 3.10+** - Programming language

## 🛠️ Technology Stack

- **Backend:** FastAPI (Python)
- **ML Model:** CatBoost Regressor
- **Data Processing:** Pandas, NumPy, Scikit-learn
- **Deployment:** Docker + Render
- **Documentation:** Automatic OpenAPI/Swagger generation

## 📊 Model Features

The prediction model uses the following features:
- **Property characteristics:** Area, bedrooms, property type
- **Location data:** ZIP code, geographic region, coordinates
- **Amenities:** Garden, swimming pool, terrace, parking, elevator
- **Building condition:** Energy performance certificate, building state
- **Encoded categorical variables:** Property type, building condition, EPC score

## 🔍 API Documentation

For complete interactive documentation with the ability to test endpoints directly in your browser, visit:

**📖 [Interactive API Documentation](https://immoeliza-api-cloris-f-chen.onrender.com/docs)**

The documentation includes:
- Complete endpoint descriptions
- Request/response schemas
- Interactive testing interface
- Example requests and responses
- Error code explanations

## 🚨 Important Notes

- **Case Sensitivity:** All string inputs are case-insensitive
- **Required Fields:** `area`, `property-type`, `bedrooms-number`, `zip-code` are mandatory
- **ZIP Code Range:** Must be between 1000-9999 (Belgian postal codes)
- **Response Time:** First request after inactivity may take 30-60 seconds (free tier limitation)
- **Rate Limiting:** Reasonable usage expected for free tier deployment

## 🤝 Team Development

The implementation focuses on:
- Clean, maintainable code structure
- Comprehensive error handling
- User-friendly API and APP design
- Professional documentation
- Robust data validation

**Contributors:** Jordi(https://github.com/bljordi78.git)
                  Mouske(https://github.com/Mouske.git)
                  Cloris_F_Chen(https://github.com/Cloris-la.git)
**Developer:** Cloris F. Chen  
**Branch:** `Cloris_F_Chen_Deployment`  
**Deployment:** Render  Streamlit
**Last Updated:** July 2025
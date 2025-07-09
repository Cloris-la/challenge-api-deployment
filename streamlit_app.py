import streamlit as st
import requests

st.title("🏠 Property Price Prediction")

# Required fields
area = st.number_input("Area (m²)", min_value=1)
property_type = st.selectbox("Property Type", ["House", "Apartment", "Others"])
rooms_number = st.number_input("Number of Rooms", min_value=0)
zip_code = st.number_input("Zip Code", min_value=1000, max_value=9999)

# Optional fields (checkboxes default to False)
garden = st.checkbox("Garden")
lift = st.checkbox("Lift")
swimmingpool = st.checkbox("Swimming Pool")
terrace = st.checkbox("Terrace")
parking = st.checkbox("Parking")

if st.button("Predict Price"):
    payload = {
        "area": area,
        "property_type": property_type,
        "rooms_number": rooms_number,
        "zip_code": zip_code,
        # optional fields
        "garden": garden,
        "lift": lift,
        "swimmingpool": swimmingpool,
        "terrace": terrace,
        "parking": parking
    }
    
    api_url = "https://challenge-api-deployment-sjcv.onrender.com/predict"
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if "prediction" in data:
            st.success(f"Estimated price: {data['prediction']} €")
        else:
            st.warning(f"Unexpected response: {data}")
    except Exception as e:
        st.error(f"Error calling API: {e}")

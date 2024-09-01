import streamlit as st
import numpy as np
import pickle
import json

# Load the model and columns data
def load_model():
    with open('banglore_home_prices_model.pickle', 'rb') as f:
        model = pickle.load(f)
    with open('columns.json', 'r') as f:
        data_columns = json.load(f)['data_columns']
        locations = data_columns[3:]  # first 3 columns are sqft, bath, bhk
    return model, data_columns, locations

model, data_columns, locations = load_model()

# Function to predict price
def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(model.predict([x])[0], 2)

# Function to format price
def format_price(price):
    if price >= 100:
        return f"{price / 100:.2f} Crores"
    else:
        return f"{price} Lakhs"

# Streamlit UI
def main():
    st.title("Bangalore Home Price Prediction")

    # Input fields
    sqft = st.text_input("Total Square Feet", "1000")
    bhk = st.selectbox("BHK", [1, 2, 3, 4, 5])
    bath = st.selectbox("Bath", [1, 2, 3, 4, 5])
    location = st.selectbox("Location", locations)

    if st.button("Estimate Price"):
        # Convert input values
        sqft = float(sqft)
        bhk = int(bhk)
        bath = int(bath)

        # Predict price
        estimated_price = get_estimated_price(location, sqft, bhk, bath)
        formatted_price = format_price(estimated_price)
        st.success(f"The estimated price is {formatted_price}")

if __name__ == "__main__":
    main()

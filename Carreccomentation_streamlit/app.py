import streamlit as st
import pandas as pd

# Load the CSV file containing car rental data
@st.cache
def load_data():
    return pd.read_csv('car_rental_data.csv')

# Function to filter car recommendations based on user input
def filter_cars(data, category=None, price=None, seats=None, air_condition=None, fuel_type=None):
    if category:
        data = data[data['Category'] == category]
    if price:
        data = data[data['Price Per Day (INR)'] <= price]
    if seats:
        data = data[data['Number of Seats'] == seats]
    if air_condition:
        data = data[data['Air Conditioning'] == air_condition]
    if fuel_type:
        data = data[data['Fuel Type'] == fuel_type]
    
    return data

def main():
    # Set the background image and custom styling using HTML and CSS
    st.markdown(
        """
        <style>
        .main {
            background-image: url('https://wallpapercrafter.com/th800/14002-car-sunset-night-movement-speed-4k.jpg');
            background-size: cover;
            background-position: center;
            padding: 20px;
            font-family: 'Arial', sans-serif;
        }
        .title {
            font-size: 50px;
            color: #ffffff;
            text-align: center;
            font-weight: bold;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
            margin-bottom: 40px;
        }
        .stSelectbox, .stNumberInput, .stRadio {
            color: #ffffff;
            font-size: 18px;
        }
        .stButton>button {
            background-color: #ff6600;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            margin-top: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
        }
        .stButton>button:hover {
            background-color: #e65c00;
        }
        .stDataFrame {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title of the application
    st.markdown("<div class='title'>CAR for me</div>", unsafe_allow_html=True)

    # Load data from CSV
    car_data = load_data()

    # Split the page into two columns: Left for inputs and right for outputs
    col1, col2 = st.columns(2)

    # Input fields for car rental preferences on the left side
    with col1:
        st.markdown("### Select Your Preferences")
        category = st.selectbox("Select car category (optional)", ["", "Vintage", "Luxury", "SUV", "Off-Road", "Hatchback", "Electric"])
        price_per_day = st.number_input("Maximum budget per day in rupees (optional)", min_value=500, max_value=50000, step=100)
        num_seats = st.selectbox("Number of seats (optional)", ["", 4, 5, 6, 7])
        air_conditioning = st.radio("Do you need air conditioning? (optional)", ["", "Yes", "No"])
        fuel_type = st.selectbox("Fuel type (optional)", ["", "Petrol", "Diesel", "Electric", "Hybrid"])

    # Results on the right side
    with col2:
        st.markdown("### Recommended Cars")

        if st.button("Generate Recommendations"):
            with st.spinner("Finding the best matches..."):
                filtered_cars = filter_cars(
                    car_data,
                    category=category if category != "" else None,
                    price=price_per_day if price_per_day else None,
                    seats=num_seats if num_seats != "" else None,
                    air_condition=air_conditioning if air_conditioning != "" else None,
                    fuel_type=fuel_type if fuel_type != "" else None
                )

                if not filtered_cars.empty:
                    st.success(f"{len(filtered_cars)} cars found:")
                    
                    # Display each recommendation with a number and details
                    for idx, row in filtered_cars.iterrows():
                        st.markdown(f"**{idx + 1}. {row['Car Name']}**")
                        st.markdown(f"- **Category**: {row['Category']}")
                        st.markdown(f"- **Price per Day**: ₹{row['Price Per Day (INR)']}")
                        st.markdown(f"- **Seats**: {row['Number of Seats']}")
                        st.markdown(f"- **Air Conditioning**: {row['Air Conditioning']}")
                        st.markdown(f"- **Fuel Type**: {row['Fuel Type']}")
                        st.markdown("---")
                else:
                    st.warning("No cars match your criteria. Try adjusting your filters.")

if __name__ == "__main__":
    main()

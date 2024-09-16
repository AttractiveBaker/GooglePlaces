import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Function to get all possible place types supported by the Google Places API
def get_all_possible_place_types():
    return [
        "accounting", "airport", "amusement_park", "aquarium", "art_gallery", "atm", "bakery", "bank", "bar",
        "beauty_salon", "bicycle_store", "book_store", "bowling_alley", "bus_station", "cafe", "campground", "car_dealer",
        "car_rental", "car_repair", "car_wash", "casino", "cemetery", "church", "city_hall", "clothing_store",
        "convenience_store", "courthouse", "dentist", "department_store", "doctor", "electrician", "electronics_store",
        "embassy", "fire_station", "florist", "funeral_home", "furniture_store", "gas_station", "gym", "hair_care",
        "hardware_store", "hindu_temple", "home_goods_store", "hospital", "insurance_agency", "jewelry_store", "laundry",
        "lawyer", "library", "light_rail_station", "liquor_store", "local_government_office", "locksmith", "lodging",
        "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater", "moving_company", "museum",
        "night_club", "painter", "park", "parking", "pet_store", "pharmacy", "physiotherapist", "plumber", "police",
        "post_office", "primary_school", "real_estate_agency", "restaurant", "roofing_contractor", "rv_park",
        "school", "secondary_school", "shoe_store", "shopping_mall", "spa", "stadium", "storage", "store",
        "subway_station", "supermarket", "synagogue", "taxi_stand", "tourist_attraction", "train_station",
        "transit_station", "travel_agency", "university", "veterinary_care", "zoo"
    ]

# Function to get places within a radius from a given lat/lng for multiple place types
def get_places_nearby_multiple_types(lat, lng, radius=1609, place_types=None):
    API_KEY = "AIzaSyBB1tMYFZbrhqOxXMlt3lltsZmjHmc_H9w"
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    all_places = []

    for place_type in place_types:
        params = {
            'location': f'{lat},{lng}',
            'radius': radius,
            'type': place_type,
            'key': API_KEY
        }
        while True:
            response = requests.get(endpoint_url, params=params)
            if response.status_code == 200:
                places_data = response.json()
                if 'results' in places_data:
                    for place in places_data['results']:
                        place_info = {
                            'name': place.get('name'),
                            'address': place.get('vicinity'),
                            'location': place.get('geometry', {}).get('location'),
                            'rating': place.get('rating', None),
                            'user_ratings_total': place.get('user_ratings_total', None),
                            'place_id': place.get('place_id'),
                            'type': place_type
                        }
                        all_places.append(place_info)
                if 'next_page_token' in places_data:
                    params['pagetoken'] = places_data['next_page_token']
                    import time
                    time.sleep(2)
                else:
                    break
            else:
                st.error(f"Error for place type '{place_type}': {response.status_code}")
                break

    return pd.DataFrame(all_places)

# Streamlit app
st.title("Google Places API Explorer")

if st.button("List All Possible Place Types"):
    place_types = get_all_possible_place_types()
    st.write(place_types)

lat = st.number_input("Latitude", format="%.6f")
lng = st.number_input("Longitude", format="%.6f")
radius = st.number_input("Radius (meters)", value=1609)
selected_place_types = st.multiselect("Place Types", get_all_possible_place_types())

if st.button("Get Places Nearby"):
    if lat and lng and selected_place_types:
        df = get_places_nearby_multiple_types(lat, lng, radius, selected_place_types)
        st.write(df.head())
        csv = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name='places.csv', mime='text/csv')
    else:
        st.error("Please provide latitude, longitude, and select at least one place type.")
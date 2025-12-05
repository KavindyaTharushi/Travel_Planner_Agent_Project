import streamlit as st
import json
import os
from serpapi import GoogleSearch 
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# -------------------------------
# CONFIGURE GEMINI
# -------------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

# -------------------------------
# STREAMLIT UI
# -------------------------------

st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")
st.markdown("""
<style>
    .title { text-align:center; font-size:36px; font-weight:bold; color:#ff5733; }
    .subtitle { text-align:center; font-size:20px; color:#555; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">✈️ AI-Powered Travel Planner</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plan your dream trip with AI! Get personalized recommendations for flights, hotels, and activities.</p>', unsafe_allow_html=True)

# -------------------------------
# USER INPUTS
# -------------------------------
st.markdown("### 🌍 Where are you headed?")
airports = {
    "Colombo, Sri Lanka (CMB)": "CMB",
    "Mumbai, India (BOM)": "BOM",
    "Delhi, India (DEL)": "DEL",
    "Bangalore, India (BLR)": "BLR",
    "Chennai, India (MAA)": "MAA",
    "Melbourne, Australia (MEL)": "MEL",
    "Sydney, Australia (SYD)": "SYD",
    "London, UK (LHR)": "LHR",
    "New York, USA (JFK)": "JFK"
}

departure_label = "🛫 Departure City (IATA Code)"
source_display = st.selectbox(departure_label, list(airports.keys()))
source = airports[source_display]  

destination_label = "🛬 Destination (IATA Code)"
destination_display = st.selectbox(destination_label, list(airports.keys()))
destination = airports[destination_display] 

st.markdown("### 📅 Plan Your Adventure")
num_days = st.slider("🕒 Trip Duration (days):", 1, 14, 5)
travel_theme = st.selectbox(
    "🎭 Select Your Travel Theme:",
    ["💑 Couple Getaway", "👨‍👩‍👧‍👦 Family Vacation", "🏔️ Adventure Trip", "🧳 Solo Exploration"]
)

st.markdown("---")

st.markdown(f"""
<div style="
    text-align:center;
    padding:15px;
    background-color:#ffecd1;
    border-radius:10px;
    margin-top:20px;">
    <h3>🌟 Your {travel_theme} to {destination} is about to begin! 🌟</h3>
    <p>Let's find the best flights, stays, and experiences for your unforgettable journey.</p>
</div>
""", unsafe_allow_html=True)

activity_preferences = st.text_area(
    "🌍 What activities do you enjoy?",
    "Relaxing on the beach, exploring historical sites"
)

departure_date = st.date_input("Departure Date")
return_date = st.date_input("Return Date")

# -------------------------------
# SIDEBAR OPTIONS
# -------------------------------
st.sidebar.title("🌎 Travel Assistant")
st.sidebar.subheader("Personalize Your Trip")

budget = st.sidebar.radio("💰 Budget Preference:", ["Economy", "Standard", "Luxury"])
flight_class = st.sidebar.radio("✈️ Flight Class:", ["Economy", "Business", "First Class"])
hotel_rating = st.sidebar.selectbox("🏨 Preferred Hotel Rating:", ["Any", "3⭐", "4⭐", "5⭐"])

st.sidebar.subheader("🎒 Packing Checklist")
packing_list = ["👕 Clothes", "🩴 Footwear", "🕶️ Sunglasses", "📖 Guidebook", "💊 Medicines"]
for item in packing_list:
    st.sidebar.checkbox(item, value=True)

st.sidebar.subheader("🛂 Travel Essentials")
visa_required = st.sidebar.checkbox("🛃 Check Visa Requirements")
travel_insurance = st.sidebar.checkbox("🛡️ Get Travel Insurance")

# -------------------------------
# UTILITIES
# -------------------------------

def format_datetime(iso_string):
    try:
        dt = datetime.strptime(iso_string, "%Y-%m-%d %H:%M")
        return dt.strftime("%b-%d, %Y | %I:%M %p")
    except:
        return "N/A"

def fetch_flights(source, destination, departure_date, return_date):
    params = {
        "engine": "google_flights",
        "departure_id": source,
        "arrival_id": destination,
        "outbound_date": str(departure_date),
        "return_date": str(return_date),
        "hl": "en",
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    return search.get_dict()

def extract_cheapest_flights(flight_data):
    best_flights = flight_data.get("best_flights", [])
    return sorted(best_flights, key=lambda x: x.get("price", float("inf")))[:3]

# -------------------------------
# MANUAL AI FUNCTIONS (NO AGENTS)
# -------------------------------

def run_researcher(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    instructions = """
    You are an expert Travel Researcher.
    Gather information on:
    - climate
    - culture
    - safety
    - top attractions
    - ideal activities
    Provide structured insights.
    """
    response = model.generate_content(instructions + "\n\n" + prompt)
    return response.text

def run_hotel_finder(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    instructions = """
    You specialize in finding:
    - best hotels
    - best restaurants
    Consider budget, rating, style.
    Provide clear recommendations.
    """
    response = model.generate_content(instructions + "\n\n" + prompt)
    return response.text

def run_planner(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    instructions = """
    You are a travel itinerary creator.
    Generate a detailed, day-wise plan including timings, food, transport, and costs.
    """
    response = model.generate_content(instructions + "\n\n" + prompt)
    return response.text

# -------------------------------
# MAIN EXECUTION
# -------------------------------

if st.button("🚀 Generate Travel Plan"):
    with st.spinner("✈️ Fetching flight data..."):
        flight_data = fetch_flights(source, destination, departure_date, return_date)
        cheapest_flights = extract_cheapest_flights(flight_data)

    # Research
    with st.spinner("🔍 Researching destination..."):
        research_prompt = (
            f"Research {destination} for a {num_days}-day {travel_theme} trip. "
            f"Activities: {activity_preferences}. Budget: {budget}. Hotel Rating: {hotel_rating}."
        )
        research_results = run_researcher(research_prompt)

    # Hotels + Restaurants
    with st.spinner("🏨 Finding best hotels and restaurants..."):
        hotel_prompt = (
            f"Find top hotels and restaurants in {destination}. Budget: {budget}. "
            f"Rating: {hotel_rating}. Activities: {activity_preferences}."
        )
        hotel_restaurant_results = run_hotel_finder(hotel_prompt)

    # Itinerary
    with st.spinner("🗺️ Preparing itinerary..."):
        itinerary_prompt = (
            f"Create a {num_days}-day itinerary for a {travel_theme}. "
            f"Destination: {destination}. Activities: {activity_preferences}. "
            f"Budget: {budget}. Flight Class: {flight_class}. "
            f"Flights: {json.dumps(cheapest_flights)}. "
            f"HotelSuggestions: {hotel_restaurant_results}. "
            f"Research: {research_results}."
        )
        itinerary = run_planner(itinerary_prompt)

    # -------------------------------
    # DISPLAY OUTPUT
    # -------------------------------

    st.subheader("✈️ Cheapest Flight Options")
    if cheapest_flights:
        cols = st.columns(len(cheapest_flights))
        for idx, flight in enumerate(cheapest_flights):
            with cols[idx]:
                airline_logo = flight.get("airline_logo", "")
                flights_info = flight.get("flights", [{}])
                airline_name = flights_info[0].get("airline", "Unknown Airline")
                price = flight.get("price", "N/A")
                
                departure_time = format_datetime(flights_info[0].get("departure_airport", {}).get("time", "N/A"))
                arrival_time = format_datetime(flights_info[-1].get("arrival_airport", {}).get("time", "N/A"))

                st.markdown(f"""
                <div style="
                    border:2px solid #ddd; padding:15px; border-radius:10px;
                    background:#f9f9f9; text-align:center;">
                    <img src="{airline_logo}" width="100" />
                    <h3>{airline_name}</h3>
                    <p><b>Departure:</b> {departure_time}</p>
                    <p><b>Arrival:</b> {arrival_time}</p>
                    <h2 style="color:#008000;">💰 {price}</h2>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No flights available.")

    st.subheader("🏨 Hotels & Restaurants")
    st.write(hotel_restaurant_results)

    st.subheader("🗺️ Your Personalized Itinerary")
    st.write(itinerary)

    st.success("✅ Travel plan generated successfully!")

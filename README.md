
=======
# Travel_Planner_Agent_Project

# 🌍 AI Travel Planner Agent

An AI-assisted Streamlit experience that turns a few travel preferences into a curated itinerary. The app blends live data (via SerpAPI) with multi-agent reasoning (powered by Agno + Gemini) to surface flight options, hotels, restaurants, and a personalized day-by-day plan.

## ✨ Highlights
- **Immersive Streamlit UI** with hero layout, moodboard tabs, and contextual highlights.
- **Live flight lookups** using the Google Flights SerpAPI engine.
- **Multi-agent orchestration** (Researcher, Planner, Hotel & Restaurant Finder) for richer recommendations.
- **Packing & essentials assistant** baked into the sidebar for quick trip prep.

## 🧱 Tech Stack
- Python 3.11+
- Streamlit for the UI
- SerpAPI for real-time flight data
- Agno Agents + Google Gemini models for reasoning
- python-dotenv for local environment variables

## 📁 Project Structure
```
Travel_Planner_Agent_Project/
├── main.py           # Streamlit entry point
├── requirements.txt  # Python dependencies
├── README.md         # You are here
└── venv/             # (optional) local virtual environment
```

## ✅ Prerequisites
1. Python 3.11 (or newer).
2. SerpAPI key with access to the Google Flights engine.
3. Google API key compatible with the Gemini model used via Agno.
4. (Optional) A virtual environment such as `python -m venv venv`.

## ⚙️ Setup
```bash
# 1. Clone or unzip the project
cd Travel_Planner_Agent_Project

# 2. Create & activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the project root:
```
SERPAPI_KEY=your_serpapi_key
GOOGLE_API_KEY=your_google_api_key
```

## 🚀 Running the App
```bash
streamlit run main.py
```
The browser will open automatically (or visit http://localhost:8501).

## 🧭 Using the Planner
1. Fill out the **Trip Blueprint** inputs (departure, destination, dates, theme, duration).
2. Dial in the **Travel Moodboard** (budget, flight class, hotel rating).
3. Describe your preferred activities in the **Activity Palette** tab.
4. Click **“🚀 Generate Travel Plan”**.
5. Review:
   - Cheapest flight cards
   - Hotel & restaurant insights
   - AI-generated itinerary
6. Tweak preferences and regenerate as needed.

## 🧠 Agent Architecture
| Agent | Role |
| --- | --- |
| Researcher | Collects destination intel, climate, attractions, and safety notes. |
| Planner | Crafts the day-by-day itinerary using itinerary prompts + research + flights/hotels. |
| Hotel & Restaurant Finder | Surfaces hospitality options around the planned activities. |

All agents run sequentially inside `main.py`, sharing context through the prompts.

## 🔧 Customization Ideas
- Swap the Gemini model IDs or temperature settings in the agent definitions.
- Extend the `packing_list` dictionary for specific personas.
- Augment the UI with additional sections (budget breakdown, map embeds, etc.).
- Add caching (`st.cache_data`) around API calls to reduce repeated costs in development.

## 🧪 Troubleshooting
- **Streamlit crashes on launch** → ensure the correct Python interpreter/venv is active.
- **Flight data empty** → verify the SerpAPI key quota and that the departure/destination codes exist.
- **Agent errors** → double-check `GOOGLE_API_KEY` permissions and network connectivity.
- **Environment variables not loading** → confirm `.env` exists and restart the Streamlit app so `load_dotenv()` reruns.

=======



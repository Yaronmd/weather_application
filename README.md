# Weather Application 🌦️

A PyQt5-based weather application that provides location suggestions and displays weather information for a selected location. The app fetches data using APIs for location autocomplete and weather details.

## Features ✨

- **Location Autocomplete**: Provides location suggestions as you type.
- **Weather Data**: Displays real-time weather information, including temperature, humidity, and more.
- **Multi-Page Navigation**: Smooth transition between input and weather details screens.
- **Asynchronous API Calls**: Ensures a responsive user experience.
- **User-Friendly UI**: Optimized for usability.

## Requirements 📋

- Python 3.8+
- `PyQt5`
- `asyncio`
- `requests`
- API access to:
  - **Google Places API** for location suggestions
  - **Weather API** for fetching weather data (e.g., OpenWeatherMap)

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/weather-app.git
   cd weather-app
   ```
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a .env file in the root directory with the following content:
     ```
     GOOGLE_API_KEY=your_google_api_key
     WEATHER_API_KEY=your_weather_api_key
     ```
     

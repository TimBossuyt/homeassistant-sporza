# 🏆 Sporza Calendar Integration for Home Assistant

A custom Home Assistant integration that brings Belgian sports events from [sporza.be](https://sporza.be) directly into your Home Assistant calendar.

## 📖 Overview

This integration fetches sports schedules from the Sporza API and creates calendar events in Home Assistant for various sports including cycling, football (soccer), Formula 1, and basketball. The integration automatically updates with the latest schedules and provides event details.

## ✨ Features
- **Automated Sports Calendar**: Fetches upcoming sports events for the next 7 days
- **Multiple Sports Support**: Currently supports:
  - 🚴‍♂️ **Cycling**
  - ⚽️ **Football/Soccer**
  - 🏎️ **Formula 1**
  - 🎾 **Tennis**
  - 🏀 **Basketball** (In development)
- **Home Assistant Calendar Integration**: Events appear in your HA calendar view
- **Rich Event Details**: Each event includes sport-specific information and direct links to the main article on [sporza.be](https://sporza.be)

## 🏗️ Architecture
#### 1. **API Client** (`api.py`)
- `SporzaApiClient`: Main API client for fetching data from Sporza
- Supports fetching games by day and retrieving detailed game metadata
- Handles different sport-specific endpoints

#### 2. **Data Models** (`models.py`)
- **Base `Game` class**: Generic sports event with common properties
- **`CyclingGame`**: Cycling events with stage and route details
- **`SoccerGame`**: Soccer matches with team information
- **`FormulaOneGame`**: F1 races with location and session details
- **`TennisGame`**: Tennis matches per tournament

(More models coming soon)

#### 3. **Calendar Entity** (`calendar.py`)
- Different Home Assistant calender entities for each sport type
- Converts game objects to Home Assistant `CalendarEvent` format

#### 4. **Configuration Flow** (`config_flow.py`)
- One-click installation through Home Assistant UI

#### 5. **Data Coordinator** (`coordinator.py`)
- Fetches data from via the API Client with a fixed time interval
- Handles caching and exceptions

### 📁 Integration File Structure
```
custom_components/sporza_calendar/
├── __init__.py         # Integration setup and entry points
├── api.py              # Sporza API client
├── calendar.py         # Calendar entity implementation
├── config_flow.py      # Configuration flow
├── const.py            # Constants and configuration
├── coordinator.py      # Data update coordinator
├── manifest.json       # Integration metadata
└── models.py           # Game data models
```

## 🚀 Installation

### Via HACS (Home Assistant Community Store)
1. Add this repository to HACS as a custom repository
2. Search for "Sporza Calendar" in HACS
3. Install the integration
4. Restart Home Assistant
5. Go to Settings → Devices & Services → Add Integration
6. Search for "Sporza Calendar" and add it

### Manual Installation
1. Copy the `custom_components/sporza_calendar` directory to your Home Assistant `custom_components` folder
2. Restart Home Assistant
3. Add the integration through the UI

## 📅 Usage

Once installed, the integration will:
1. Automatically fetch sports events for the coming week
2. Create a "Sporza Calendar" entity in Home Assistant
3. Display events in your calendar view with rich details
4. Update every few hours/minutes with the latest schedules

### Event Display Format
Examples:
- **Cycling**: `🚴‍♂️ Tour de France: Lille Métropole → Lille Métropole`
- **Football**: `⚽️ Jupiler Pro League: Club Brugge vs Anderlecht`
- **Formula 1**: `🏎️ Belgian Grand Prix @ Spa-Francorchamps`

## 🔮 Future Improvements
### ⚙️ Enhanced Functionality
- **Personalization Features**:
  - User-configurable sport preferences
  - Favorite competition filtering
- **Smart Notifications**:
  - Pre-event reminders
  - Live score updates integration
  - Result notifications
- **Advanced Calendar Features**:
  - Multiple calendar support (separate calendar per sport)
  - Event categorization and filtering

### 🔧 Technical Improvements
- **API Enhancements**:
  - Real-time event updates
  - Live score integration
  - Historical data support
- **User Experience**:
  - Custom event naming patterns

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues & Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/TimBossuyt/homeassistant-sporza/issues) page
2. Create a new issue with detailed information
3. Include Home Assistant logs if relevant

---
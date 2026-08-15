# Weather App

A small Python command-line utility that looks up a city and prints weather-related location information using the OpenWeather API.

## Features

- Accept a city name from the command line
- Query OpenWeather geocoding data
- Let the user choose among multiple matching locations when needed
- Optional imperial temperature output flag
- Reads the API key from a `.env` file

## Requirements

- Python 3
- `requests`
- `python-dotenv`

Install the dependencies with:

```bash
pip install requests python-dotenv
```

## Configuration

Create a `.env` file in the project root with your OpenWeather API key:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

## Usage

```bash
python weather.py "London"
python weather.py "New York" --imperial
```

If multiple cities match the provided name, the script asks you to choose the correct one.

## Notes

This project is a simple example for learning how to combine CLI argument parsing, environment variables, and API requests in Python.

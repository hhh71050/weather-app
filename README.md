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

You can provide a city name as a command-line argument:

```bash
python weather.py "London"
python weather.py "New York" --imperial
```

You can also run the app without arguments and type the city name directly when prompted:

```bash
python weather.py
```

If multiple cities match the provided name, the script asks you to choose the correct one.

> If the city contains an apostrophe, use quotes in the terminal, for example:
>
> ```bash
> python weather.py "Lu'an"
> ```
>
> The shell treats an apostrophe as a quote character, so it must be protected when passing the city name on the command line.

## Notes

This project is a simple example for learning how to combine CLI argument parsing, environment variables, and API requests in Python.

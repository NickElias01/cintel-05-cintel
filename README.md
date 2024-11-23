# Elias Analytics- 
### PyShiny Real-Time Data Visualization App

## Overview
This app demonstrates live, randomized temperature and barometric pressure data from Antarctica, updating every 10 seconds. The app visualizes data in real-time with temperature in Celsius, Fahrenheit, and Kelvin, and barometric pressure in hPa.

## Features
- **Live Data Updates**: Real-time updates every 10 seconds.
- **Temperature Units**: Displays in Celsius, Fahrenheit, and Kelvin.
- **Dynamic Descriptions**: Temperature categorized as "Colder", "Warmer", etc.
- **Barometric Pressure**: Displayed in hPa.
- **Interactive Plot**: Scatter plot of temperature with a regression line.
- **Recent Readings Table**: Displays the most recent data.

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/NickElias01/cintel-05-cintel.git

2. Install Dependencies:
    ```bash
    pip install -r requirements.txt

3. Run the App:
    ```python
    shiny run --reload --launch-browser dashboard/app.py
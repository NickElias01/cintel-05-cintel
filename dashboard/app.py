# --------------------------------------------
# Elias Analytics- Real-Time Data Visualization App
# --------------------------------------------
#
# This PyShiny app demonstrates live temperature and barometric pressure readings
# from Antarctica. The app generates randomized data every 10 seconds, including:
# - Temperature in Celsius, Fahrenheit, and Kelvin
# - Barometric pressure in hPa
# 
# The app displays:
# 1. The current date and time of the most recent reading
# 2. The current temperature with a description based on value ranges
# 3. The barometric pressure in hPa
# 4. A table showing the most recent readings
# 5. A plot of the latest temperature readings with a regression line
#
# The UI is designed using Shiny Express, and the app updates automatically
# to reflect the latest data, providing a real-time data visualization experience.
# --------------------------------------------


# --------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# --------------------------------------------

# From shiny, import just reactive and render
from shiny import reactive, render

# From shiny.express, import just ui and inputs if needed
from shiny.express import ui

# Standard Python libraries
import random
from datetime import datetime
from collections import deque
import pandas as pd

# Plotly for data visualization
import plotly.express as px
from shinywidgets import render_plotly

# SciPy for statistical regression
from scipy import stats

# Custom theme for UI
from shinyswatch import theme

# --------------------------------------------
# Import icons as needed
# --------------------------------------------
from faicons import icon_svg

# --------------------------------------------
# Initialization
# --------------------------------------------

# Time interval for live data updates (in seconds)
UPDATE_INTERVAL_SECS: int = 10

# Initialize a REACTIVE VALUE using a deque (a queue with a fixed length)
DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

# --------------------------------------------
# Reactive Calculation for Live Data
# --------------------------------------------
@reactive.calc()
def reactive_calc_combined():
    # Invalidate the calculation every UPDATE_INTERVAL_SECS to refresh data
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic for temperature and barometric pressure
    temp = round(random.uniform(-18, -16), 1)  # Random temperature in Celsius
    timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")  # Current timestamp
    barometric_pressure = round(random.uniform(990, 1020), 1)  # Random barometric pressure in hPa

    # New data entry
    new_entry = {
        "temp": temp,
        "temp_fahrenheit": round(temp * 9 / 5 + 32, 1),  # Temperature in Fahrenheit
        "temp_kelvin": round(temp + 273.15, 1),  # Temperature in Kelvin
        "barometric_pressure_hpa": barometric_pressure,  # Barometric pressure in hPa
        "timestamp": timestamp,
    }

    # Append new entry to the reactive deque
    reactive_value_wrapper.get().append(new_entry)

    # Return the full deque, a DataFrame for display, and the latest entry
    deque_snapshot = reactive_value_wrapper.get()
    df = pd.DataFrame(deque_snapshot)
    latest_dictionary_entry = new_entry

    return deque_snapshot, df, latest_dictionary_entry

# --------------------------------------------
# UI Page Layout Configuration
# --------------------------------------------
ui.page_opts(
    title="Elias Analytics: PyShiny Live Data", 
    fillable=True,
    style="max-height: 90vh; overflow-y: scroll; padding: 10px;",
    fullwidth=True,
    theme=theme.lux  # Set theme for the app
)

# Sidebar for additional information and links
with ui.sidebar(open="open"):
    ui.h2("Temp Readings in Antarctica", class_="text-center")
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )
    ui.hr()
    ui.h6("Links:")
    ui.a("GitHub", href="https://github.com/NickElias01/cintel-05-cintel", target="_blank")
    ui.a("GitHub App", href="https://denisecase.github.io/cintel-05-cintel/", target="_blank")
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("PyShiny Express", href="https://shiny.posit.co/blog/posts/shiny-express/", target="_blank")

# --------------------------------------------
# Main Content: Cards with Data Display
# --------------------------------------------

# Card displaying the current timestamp
with ui.card(full_screen=False):
    ui.card_header("Current Date and Time")

    @render.text
    def display_time():
        """Fetch and display the latest timestamp"""
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
        return f"{latest_dictionary_entry['timestamp']}"

# Card displaying the current temperature with description
with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("snowflake"),
        theme="bg-gradient-blue-green",
    ):
        "Current Temperature"
        
        @render.text
        def display_temp():
            """Fetch and display the latest temperature with description based on Celsius"""
            deque_snapshot, df, latest_entry = reactive_calc_combined()
            temp = latest_entry["temp"]

            # Temperature description logic
            if temp < -17.5:
                description = "Much Colder than Usual"
            elif -17.5 <= temp < -17.0:
                description = "Colder than Usual"
            elif -17.0 <= temp < -16.5:
                description = "Warmer than Usual"
            else:
                description = "Much Hotter than Usual"

            return f"{temp} °C - {description}"

# Card displaying the current barometric pressure
with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("flask"),
        theme="bg-gradient-green-blue",
    ):
        "Barometric Pressure"

        @render.text
        def display_pressure():
            """Display the latest barometric pressure reading in hPa"""
            _, _, latest_entry = reactive_calc_combined()
            pressure = latest_entry["barometric_pressure_hpa"]
            return f"{pressure} hPa"

# Card displaying the most recent readings in a table
with ui.card(full_screen=True):
    ui.card_header("Most Recent Readings")

    @render.data_frame
    def display_df():
        """Display the latest readings in a table"""
        _, df, _ = reactive_calc_combined()
        return df[["timestamp", "temp", "temp_fahrenheit", "temp_kelvin", "barometric_pressure_hpa"]]


# Card displaying the latest temperature readings with a regression line
with ui.card():
    ui.card_header("Latest Temperature Readings w/ Regression Line")

    @render_plotly
    def display_plot():
        # Fetch from the reactive calc function
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

        # Ensure the DataFrame is not empty before plotting
        if not df.empty:
            # Convert the 'timestamp' column to datetime for better plotting
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # Create scatter plot for readings
            # pass in the df, the name of the x column, the name of the y column,
            # and more
        
            fig = px.scatter(
            df,
            x="timestamp",
            y="temp",
            title="Temperature Readings with Regression Line",
            labels={"temp": "Temperature (°C)", "timestamp": "Time"},
            color_discrete_sequence=["blue"] )
            
            # Linear regression - we need to get a list of the
            # Independent variable x values (time) and the
            # Dependent variable y values (temp)
            # then, it's pretty easy using scipy.stats.linregress()

            # For x let's generate a sequence of integers from 0 to len(df)
            sequence = range(len(df))
            x_vals = list(sequence)
            y_vals = df["temp"]

            slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
            df['best_fit_line'] = [slope * x + intercept for x in x_vals]

            # Add the regression line to the figure
            fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line')

            # Update layout as needed to customize further
            fig.update_layout(xaxis_title="Time",yaxis_title="Temperature (°C)")

        return fig
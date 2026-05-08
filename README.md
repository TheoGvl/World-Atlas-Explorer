# World Atlas Explorer

A sleek, modern desktop and web application built entirely in Python using the Flet framework. This app connects to the free [REST Countries API](https://restcountries.com/) to instantly fetch and display accurate geographical and demographic data for any country in the world.

## Features

* **Instant Search:** Type a country name (e.g., "Japan", "Greece", "Brazil") to instantly pull up its data.
* **Smart Data Parsing:** Safely navigates complex, nested JSON data to extract precise information like currency names and symbols, and automatically formats large population numbers with commas.
* **Dynamic Flag Display:** Fetches and displays the official high-resolution flag of the searched country.
* **Modern UI:** Features a clean, dark-themed interface with a beautifully organized results card.
* **Cross-Platform:** Can be run as a standalone native desktop application or deployed as a web app with zero changes to the codebase.

## Tech Stack

* **Language:** Python 3.x
* **UI Framework:** Flet Builds interactive web, desktop, and mobile apps in Python.
* **API Handling:** `requests` library.
* **External API:** [REST Countries API](https://restcountries.com/).

## How to Run Locally

**Clone or Download the Project:**
   Save the `atlas.py` file to your local machine.
   **Install Dependencies:**
   Ensure you have Python installed, then install the required libraries using pip:
   ```
   pip install flet requests
   ```

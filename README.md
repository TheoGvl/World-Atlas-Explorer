# World Atlas Explorer

A premium, modern desktop and web application built entirely in Python using the Flet framework (v0.80+). This app connects to the free [REST Countries API](https://restcountries.com/) to instantly fetch and display comprehensive geographical, demographic, and cultural data for any country in the world.

## Features

* **Comprehensive Data:** Instantly fetches Capital, Population, Region, Currencies, Languages, Total Area (km²), and Timezones.
* **Smart Parsing:** Safely navigates complex, nested JSON data to extract precise information and automatically formats large numbers with commas.
* **Google Maps Integration:** Includes a quick-access button to view the exact location of the searched country directly on Google Maps.
* **Polished UI:** Features a clean, dark-themed interface with material icons, loading animations (Progress Ring), and dynamic high-resolution flag displays.
* **Cross-Platform:** Built with modern Flet syntax, it can be run as a standalone native desktop application or deployed as a web app with zero changes to the codebase.

## Tech Stack

* **Language:** Python 3.x
* **UI Framework:** Flet Modern v0.80+ syntax utilizing `ft.Icons`, `ft.Colors`, and `ft.BoxFit`.
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

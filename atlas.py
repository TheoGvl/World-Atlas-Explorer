import flet as ft
import requests

def main(page: ft.Page):
    # --- Window Configuration ---
    page.title = "World Atlas Explorer"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40
    page.window.width = 600
    page.window.height = 750
    page.bgcolor = "#0a0a1a" # Deep dark background

    # --- UI Elements: Search Bar ---
    search_input = ft.TextField(
        label="Enter a country name (English)",
        hint_text="e.g., Japan, Brazil, Greece...",
        width=300,
        border_color="blue400",
        on_submit=lambda e: fetch_country(e) # Allows pressing 'Enter' to search
    )

    search_btn = ft.ElevatedButton(
        "Search", 
        on_click=lambda e: fetch_country(e), 
        bgcolor="blue700", 
        color="white",
        height=50
    )

    # --- UI Elements: Results Card ---
    # The flag image starts hidden until we fetch a valid URL.
    # We use the string "contain" to bypass Pylance type-checking errors.
    flag_image = ft.Image(src="", width=200, height=120, fit="contain", visible=False)
    
    country_name = ft.Text("", size=30, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER)
    error_text = ft.Text("", color="red400", size=16, visible=False)

    # Dynamic text variables for the country stats
    capital_val = ft.Text("", size=16, color="white", weight=ft.FontWeight.W_500)
    population_val = ft.Text("", size=16, color="white", weight=ft.FontWeight.W_500)
    region_val = ft.Text("", size=16, color="white", weight=ft.FontWeight.W_500)
    currency_val = ft.Text("", size=16, color="white", weight=ft.FontWeight.W_500)

    # Helper function to align the labels and values nicely in a row
    def create_info_row(label, value_control):
        return ft.Row(
            [
                ft.Text(label, size=16, color="grey400", weight=ft.FontWeight.BOLD, width=100),
                value_control
            ],
            alignment=ft.MainAxisAlignment.START
        )

    # A column holding all the stats. Starts hidden.
    info_column = ft.Column([
        create_info_row("Capital:", capital_val),
        create_info_row("Population:", population_val),
        create_info_row("Region:", region_val),
        create_info_row("Currency:", currency_val),
    ], visible=False)

    # The main card container to hold the results
    result_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    flag_image,
                    country_name,
                    ft.Divider(color="transparent", height=10),
                    info_column,
                    error_text
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=30,
            width=450,
            border_radius=15,
            bgcolor="#15152a",
            border=ft.Border.all(1, "#2a2a4a") # Modern Flet Border Syntax
        ),
        elevation=10,
        margin=ft.margin.only(top=30)
    )

    # --- API Logic ---
    def fetch_country(e):
        query = search_input.value.strip()
        if not query:
            return

        # 1. Reset UI to a loading/blank state
        error_text.visible = False
        flag_image.visible = False
        info_column.visible = False
        country_name.value = "Searching..."
        page.update()

        # 2. Call the REST Countries API
        url = f"https://restcountries.com/v3.1/name/{query}?fullText=false"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                # The API returns a list of matches. We take the first (best) match.
                data = response.json()[0] 
                
                # 3. Extract data safely using .get() to prevent crashes if data is missing
                name = data.get("name", {}).get("common", "Unknown")
                flag_url = data.get("flags", {}).get("png", "")
                
                # Capital is usually a list, so we take the first item safely
                capital_list = data.get("capital", [])
                capital = capital_list[0] if capital_list else "Unknown"
                
                # Format population with commas (e.g., 1000000 -> 1,000,000)
                population = f"{data.get('population', 0):,}" 
                region = data.get("region", "Unknown")
                
                # Extracting currencies requires looping through a nested dictionary
                currencies_data = data.get("currencies", {})
                currencies = ", ".join([f"{v.get('name')} ({v.get('symbol', '')})" for k, v in currencies_data.items()])
                if not currencies:
                    currencies = "Unknown"

                # 4. Update the UI with the fetched data
                country_name.value = name
                flag_image.src = flag_url
                flag_image.visible = True
                
                capital_val.value = capital
                population_val.value = population
                region_val.value = region
                currency_val.value = currencies
                info_column.visible = True

            else:
                # Handle 404 Not Found
                country_name.value = ""
                error_text.value = f"Country '{query}' not found. Try again!"
                error_text.visible = True

        except Exception as ex:
            # Handle internet connection issues
            country_name.value = ""
            error_text.value = "Connection error. Please check your internet."
            error_text.visible = True

        # Refresh the page to show the final result
        page.update()

    # --- Final Layout ---
    page.add(
        ft.Text("🌍 World Atlas", size=35, weight=ft.FontWeight.BOLD, color="white"),
        ft.Text("Discover data and flags for any country.", size=16, color="grey400"),
        ft.Divider(height=20, color="transparent"),
        
        # Place the text input and button side-by-side
        ft.Row(
            [search_input, search_btn], 
            alignment=ft.MainAxisAlignment.CENTER
        ),
        
        result_card
    )

# Run the app (Type ignore prevents Pylance missing 'main' argument errors)
ft.run(main) # type: ignore
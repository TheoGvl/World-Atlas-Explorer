import flet as ft
import requests
import webbrowser

def main(page: ft.Page):
    # --- Window Configuration ---
    page.title = "World Atlas Explorer"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40
    page.window.width = 650
    page.window.height = 850
    page.bgcolor = "#0a0a1a"

    # --- UI Elements: Search Bar ---
    search_input = ft.TextField(
        label="Enter a country name (English)",
        hint_text="e.g., Japan, Brazil, Greece...",
        width=350,
        border_color=ft.Colors.BLUE_400,
        prefix_icon=ft.Icons.SEARCH, 
        on_submit=lambda e: fetch_country(e)
    )

    search_btn = ft.ElevatedButton(
        "Search", 
        on_click=lambda e: fetch_country(e), 
        bgcolor=ft.Colors.BLUE_700, 
        color=ft.Colors.WHITE,
        height=50,
        icon=ft.Icons.TRAVEL_EXPLORE 
    )

    # --- UI Elements: Results Card ---
    loading_ring = ft.ProgressRing(visible=False, color=ft.Colors.BLUE_400)
    
    flag_image = ft.Image(src="", width=250, height=150, fit=ft.BoxFit.CONTAIN, visible=False) 
    
    country_name = ft.Text("", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)
    error_text = ft.Text("", color=ft.Colors.RED_400, size=16, visible=False, text_align=ft.TextAlign.CENTER)

    # Dynamic text variables for the expanded country stats
    capital_val = ft.Text("", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
    population_val = ft.Text("", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
    region_val = ft.Text("", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
    currency_val = ft.Text("", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
    language_val = ft.Text("", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
    area_val = ft.Text("", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
    timezone_val = ft.Text("", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)

    current_map_url = ""

    def open_map(e):
        if current_map_url:
            webbrowser.open(current_map_url)

    map_btn = ft.OutlinedButton(
        "View on Google Maps", 
        icon=ft.Icons.MAP,
        on_click=open_map,
        visible=False
    )

    def create_info_row(icon_enum, label, value_control):
        return ft.Row(
            [
                ft.Icon(icon_enum, color=ft.Colors.BLUE_400, size=20),
                ft.Text(label, size=15, color=ft.Colors.GREY_400, weight=ft.FontWeight.BOLD, width=90),
                value_control
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )

    # A column holding all the stats 
    info_column = ft.Column([
        create_info_row(ft.Icons.LOCATION_CITY, "Capital:", capital_val),
        create_info_row(ft.Icons.PEOPLE, "Population:", population_val),
        create_info_row(ft.Icons.PUBLIC, "Region:", region_val),
        create_info_row(ft.Icons.ATTACH_MONEY, "Currency:", currency_val),
        create_info_row(ft.Icons.LANGUAGE, "Language:", language_val),
        create_info_row(ft.Icons.LANDSCAPE, "Area:", area_val),
        create_info_row(ft.Icons.ACCESS_TIME, "Timezone:", timezone_val),
        ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
        ft.Row([map_btn], alignment=ft.MainAxisAlignment.CENTER)
    ], visible=False, spacing=8)

    # The main card container
    result_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    loading_ring,
                    flag_image,
                    country_name,
                    ft.Divider(color="#2a2a4a", height=20),
                    info_column,
                    error_text
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=30,
            width=500,
            border_radius=15,
            bgcolor="#15152a",
            border=ft.Border.all(1, "#2a2a4a")
        ),
        elevation=10,
        margin=ft.margin.only(top=20)
    )

    # --- API Logic ---
    def fetch_country(e):
        nonlocal current_map_url
        query = search_input.value.strip()
        if not query:
            return

        # Show Loading State
        error_text.visible = False
        flag_image.visible = False
        info_column.visible = False
        map_btn.visible = False
        country_name.value = ""
        loading_ring.visible = True
        page.update()

        # Call the REST Countries API
        url = f"https://restcountries.com/v3.1/name/{query}?fullText=false"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()[0] 
                
                # Extract Data Safely
                name = data.get("name", {}).get("common", "Unknown")
                flag_url = data.get("flags", {}).get("png", "")
                
                capital_list = data.get("capital", [])
                capital = capital_list[0] if capital_list else "Unknown"
                
                population = f"{data.get('population', 0):,}" 
                region = data.get("region", "Unknown")
                area = f"{data.get('area', 0):,} km²"
                
                tz_list = data.get("timezones", [])
                timezone = tz_list[0] if tz_list else "Unknown"
                
                currencies_data = data.get("currencies", {})
                currencies = ", ".join([f"{v.get('name')} ({v.get('symbol', '')})" for k, v in currencies_data.items()])
                if not currencies: currencies = "Unknown"

                languages_data = data.get("languages", {})
                languages = ", ".join(languages_data.values()) if languages_data else "Unknown"

                current_map_url = data.get("maps", {}).get("googleMaps", "")

                # Update the UI
                country_name.value = name
                flag_image.src = flag_url
                flag_image.visible = True
                
                capital_val.value = capital
                population_val.value = population
                region_val.value = region
                currency_val.value = currencies
                language_val.value = languages
                area_val.value = area
                timezone_val.value = timezone
                
                if current_map_url:
                    map_btn.visible = True

                info_column.visible = True

            else:
                error_text.value = f"Country '{query}' not found. Try again!"
                error_text.visible = True

        except Exception as ex:
            error_text.value = "Connection error. Please check your internet."
            error_text.visible = True

        # Turn off loading ring and refresh
        loading_ring.visible = False
        page.update()

    # --- Final Layout ---
    page.add(
        ft.Text("World Atlas", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        ft.Text("Discover data and flags for any country.", size=16, color=ft.Colors.GREY_400),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        
        ft.Row(
            [search_input, search_btn], 
            alignment=ft.MainAxisAlignment.CENTER
        ),
        
        result_card
    )

ft.run(main) # type: ignore
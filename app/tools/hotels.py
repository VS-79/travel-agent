from langchain_core.tools import tool

MOCK_HOTELS = {
    "tokyo": [
        {"name": "Shinjuku Granbell Hotel", "price": "$80/night", "rating": "4.2", "area": "Shinjuku"},
        {"name": "Dormy Inn Asakusa", "price": "$65/night", "rating": "4.4", "area": "Asakusa"},
        {"name": "Park Hyatt Tokyo", "price": "$400/night", "rating": "4.8", "area": "Shinjuku"},
    ],
    "paris": [
        {"name": "Hotel des Arts Montmartre", "price": "$90/night", "rating": "4.3", "area": "Montmartre"},
        {"name": "Generator Paris", "price": "$45/night", "rating": "4.1", "area": "Canal Saint-Martin"},
        {"name": "Le Bristol Paris", "price": "$900/night", "rating": "4.9", "area": "8th arrondissement"},
    ],
    "singapore": [
        {"name": "Hotel 81", "price": "$50/night", "rating": "3.8", "area": "Geylang"},
        {"name": "Marina Bay Sands", "price": "$350/night", "rating": "4.7", "area": "Marina Bay"},
        {"name": "The Warehouse Hotel", "price": "$180/night", "rating": "4.6", "area": "Robertson Quay"},
    ],
}

@tool
def search_hotels(city: str, budget: str = "moderate") -> str:
    """Search for hotel recommendations in a city based on budget.
    Budget options: budget, moderate, luxury."""
    city_lower = city.lower()
    hotels = MOCK_HOTELS.get(city_lower, [
        {"name": f"Central Hotel {city}", "price": "$80/night", "rating": "4.0", "area": "City Center"},
        {"name": f"Budget Inn {city}", "price": "$40/night", "rating": "3.8", "area": "Downtown"},
    ])

    result = f"Hotel options in {city}:\n"
    for h in hotels:
        result += f"- {h['name']} | {h['price']} | Rating: {h['rating']} | Area: {h['area']}\n"

    return result
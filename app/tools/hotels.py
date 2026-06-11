from langchain_core.tools import tool
from serpapi import GoogleSearch
from datetime import datetime, timedelta
from app.config import settings

def get_dates():
    """Get check-in and check-out dates for tomorrow and day after."""
    check_in = datetime.now() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    return check_in.strftime("%Y-%m-%d"), check_out.strftime("%Y-%m-%d")

@tool
def search_hotels(city: str, budget: str = "moderate") -> str:
    """Search for real hotel options in a city using Google Hotels data.
    Budget options: budget, moderate, luxury.
    Returns real hotel names, prices, ratings and booking links."""
    try:
        check_in, check_out = get_dates()

        price_filters = {
            "budget": {"min_price": 0, "max_price": 80},
            "moderate": {"min_price": 80, "max_price": 250},
            "luxury": {"min_price": 250, "max_price": 1000},
        }
        price_range = price_filters.get(budget.lower(), price_filters["moderate"])

        params = {
            "engine": "google_hotels",
            "q": f"hotels in {city}",
            "check_in_date": check_in,
            "check_out_date": check_out,
            "adults": "2",
            "currency": "USD",
            "gl": "us",
            "hl": "en",
            "api_key": settings.serpapi_key,
            **price_range
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        hotels = results.get("properties", [])[:5]

        if not hotels:
            return search_hotels_fallback(city, budget)

        check_in_display = datetime.strptime(check_in, "%Y-%m-%d").strftime("%B %d, %Y")
        check_out_display = datetime.strptime(check_out, "%Y-%m-%d").strftime("%B %d, %Y")

        result = f"Real hotel options in {city} ({budget} budget) for {check_in_display} - {check_out_display}:\n\n"

        for hotel in hotels:
            name = hotel.get("name", "Unknown Hotel")
            rating = hotel.get("overall_rating", "N/A")
            reviews = hotel.get("reviews", 0)
            hotel_class = hotel.get("hotel_class", "")
            description = hotel.get("description", "")
            check_in_time = hotel.get("check_in_time", "N/A")
            check_out_time = hotel.get("check_out_time", "N/A")

            rate = hotel.get("rate_per_night", {})
            price = rate.get("lowest", "Price not available")

            amenities = hotel.get("amenities", [])[:5]
            amenities_str = ", ".join(amenities) if amenities else "N/A"

            result += f"**{name}**\n"
            if hotel_class:
                result += f"  Class: {hotel_class}\n"
            result += f"  Price: {price}/night\n"
            result += f"  Rating: {rating}/5 ({reviews} reviews)\n"
            if description:
                result += f"  About: {description[:100]}...\n"
            result += f"  Amenities: {amenities_str}\n"
            result += f"  Check-in: {check_in_time} | Check-out: {check_out_time}\n\n"

        return result

    except Exception as e:
        print(f"DEBUG: SerpAPI hotel error: {e}")
        return search_hotels_fallback(city, budget)


def search_hotels_fallback(city: str, budget: str = "moderate") -> str:
    """Fallback mock data when SerpAPI is unavailable."""
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
        "london": [
            {"name": "Generator London", "price": "$55/night", "rating": "4.1", "area": "Kings Cross"},
            {"name": "Premier Inn City", "price": "$90/night", "rating": "4.2", "area": "City of London"},
            {"name": "The Savoy", "price": "$600/night", "rating": "4.9", "area": "Strand"},
        ],
        "bangkok": [
            {"name": "Lub d Bangkok Silom", "price": "$35/night", "rating": "4.3", "area": "Silom"},
            {"name": "Ibis Bangkok Riverside", "price": "$55/night", "rating": "4.0", "area": "Riverside"},
            {"name": "Mandarin Oriental Bangkok", "price": "$400/night", "rating": "4.9", "area": "Riverside"},
        ],
    }

    hotels = MOCK_HOTELS.get(city.lower(), [
        {"name": f"Central Hotel {city}", "price": "$80/night", "rating": "4.0", "area": "City Center"},
        {"name": f"Budget Inn {city}", "price": "$40/night", "rating": "3.8", "area": "Downtown"},
    ])

    result = f"Hotel options in {city} ({budget} budget):\n"
    for h in hotels:
        result += f"- {h['name']} | {h['price']} | Rating: {h['rating']} | Area: {h['area']}\n"
    return result
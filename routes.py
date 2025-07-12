from flask import Blueprint, render_template, request, redirect, url_for
from app.weather import get_weather_data

main = Blueprint("main", __name__)


# In-memory list to store community posts
community_posts = []
def analyze_soil(soil_type, ph, moisture):
    recommendations = []


    # Example simple rules:
    if soil_type.lower() == "sandy":
        recommendations.append("Add organic matter to improve water retention.")
    elif soil_type.lower() == "clay":
        recommendations.append("Ensure proper drainage to avoid waterlogging.")
    else:
        recommendations.append("Soil type looks good.")

    try:
        ph = float(ph)
        if ph < 6.0:
            recommendations.append("Soil is acidic, consider adding lime.")
        elif ph > 7.5:
            recommendations.append("Soil is alkaline, consider adding sulfur.")
        else:
            recommendations.append("Soil pH is optimal.")
    except:
        recommendations.append("pH value is invalid or missing.")

    try:
        moisture = float(moisture)
        if moisture < 30:
            recommendations.append("Soil moisture is low, increase irrigation.")
        elif moisture > 70:
            recommendations.append("Soil moisture is high, reduce watering.")
        else:
            recommendations.append("Soil moisture level is good.")
    except:
        recommendations.append("Moisture value is invalid or missing.")

    return recommendations


@main.route("/")
def index():
    return render_template("index.html")
@main.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    weather_data = None
    soil_data = None
    soil_analysis = None
    calendar = None
    city = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "weather":
            city = request.form.get("city")
            weather_data = get_weather_data(city)

        elif action == "soil":
            soil_type = request.form.get("soil_type")
            ph = request.form.get("ph_level")
            moisture = request.form.get("moisture")

            soil_data = f"Type: {soil_type}, pH: {ph}, Moisture: {moisture}%"
            soil_analysis = analyze_soil(soil_type, ph, moisture)  # <-- Important!

        elif action == "calendar":
            crop = request.form.get("crop")
            calendar = get_crop_calendar(crop)

    return render_template(
        "dashboard.html",
        weather=weather_data,
        soil_data=soil_data,
        soil_analysis=soil_analysis,
        calendar=calendar,
        city=city
    )

def get_crop_calendar(crop):
    calendars = {
        "rice": [
            "Sowing: June 1–15",
            "Fertilize: July 5, August 10",
            "Harvest: October–November"
        ],
        "maize": [
            "Sowing: July 1–10",
            "Fertilize: August 1, September 5",
            "Harvest: November"
        ],
        "groundnut": [
            "Sowing: June 10–20",
            "Fertilize: July 15",
            "Harvest: September–October"
        ]
    }
    return calendars.get(crop, [])
@main.route("/crop-calendar", methods=["GET", "POST"])
def crop_calendar():
    calendar = None
    if request.method == "POST":
        crop = request.form.get("crop")
        location = request.form.get("location")
        if crop and location:
            calendar = {
                "Sowing": "June 1 - June 15",
                "Fertilizing": "July 1 - July 10",
                "Weeding": "August 1 - August 7",
                "Harvesting": "October 15 - October 30"
            }
    return render_template("crop_calendar.html", calendar=calendar)
@main.route("/community", methods=["GET", "POST"])
def community():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        if name and message:
            community_posts.append({
                "name": name,
                "message": message
            })
        return redirect(url_for("main.community"))

    return render_template("community.html", posts=community_posts)
chat_knowledge = {
    "fertilizer": "Use nitrogen-based fertilizer during early growth, switch to phosphorous and potassium during flowering.",
    "watering": "Water early morning or late evening. Drip irrigation is efficient for most crops.",
    "pests": "Use neem-based organic pesticides for aphids and whiteflies.",
    "soil improvement": "Add compost or green manure to improve soil health.",
    "organic": "Using organic farming methods improves long-term soil fertility and market value."
}

@main.route("/tools", methods=["GET", "POST"])
def tools():
    response = ""
    if request.method == "POST":
        user_input = request.form.get("question", "").lower()
        for keyword, answer in chat_knowledge.items():
            if keyword in user_input:
                response = answer
                break
        if not response:
            response = "Sorry, I don't have information on that topic yet. Try asking about fertilizer, watering, or pests."
    return render_template("tools.html", response=response)


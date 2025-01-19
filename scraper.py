import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import os
import requests

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the target website
url = "https://www.ticket-onlineshop.com/ols/haie/de/tageskarten/channel/shop/index"
driver.get(url)

# Wait for JavaScript to load
driver.implicitly_wait(10)

# Extract game elements with 'data-event-id'
game_elements = driver.find_elements(By.CSS_SELECTOR, '[data-event-id]')

# Prepare a dictionary to store games with their IDs
games = {}

# Iterate through the game elements and extract details
for game in game_elements:
    # Extract the unique game ID
    game_id = game.get_attribute('data-event-id')

    # Extract team names
    home_team = game.find_element(By.ID, "home-team-name").text.strip()
    away_team = game.find_element(By.ID, "guest-team-name").text.strip()

    # Extract date and time
    event_date = game.find_element(By.ID, "event-date").text.strip()
    event_time = game.find_element(By.ID, "event-time").text.strip()

    # Extract venue information
    venue_element = game.find_element(By.ID, "venue-name")
    venue = venue_element.text.strip() if venue_element else "N/A"

    # Extract ticket price (if available)
    ticket_price_element = game.find_elements(By.CLASS_NAME, "button")
    ticket_price = ticket_price_element[0].text.strip() if ticket_price_element else "N/A"

    # Extract ticket purchase link
    ticket_link_element = game.find_element(By.CLASS_NAME, "button")
    ticket_link = (
        ticket_link_element.get_attribute("href")
        if ticket_link_element else "N/A"
    )

    # Store all details in a dictionary under the unique ID
    games[game_id] = {
        "home_team": home_team,
        "away_team": away_team,
        "date": event_date,
        "time": event_time,
        "venue": venue,
        "ticket_price": ticket_price,
        "ticket_link": ticket_link,
    }

# Define the JSON file name
filename = "games.json"

# Load existing games from the JSON file if it exists
if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as json_file:
        existing_games = json.load(json_file)
else:
    existing_games = {}

# Check for new games and append them to the existing data if necessary
new_games_count = 0

for game_id, game_data in games.items():
    if game_id not in existing_games:
        existing_games[game_id] = game_data
        new_games_count += 1

        # Send a notification for each new game
        notification_message = (
            f"New Game Added:\n"
            f"{game_data['home_team']} vs {game_data['away_team']}\n"
            f"Date: {game_data['date']} Time: {game_data['time']}\n"
            f"Venue: {game_data['venue']}\n"
            f"Price: {game_data['ticket_price']}\n"
            f"Ticket Link: {game_data['ticket_link']}"
        )
        requests.post(
            "https://ntfy.sh/haie-tickets",
            data=notification_message.encode(encoding="utf-8"),
            headers={"Click": game_data["ticket_link"], "Title": "New Game Alert", "Tags": "triangular_flag_on_post,haie"},
        )

# Save updated data back to the JSON file
with open(filename, "w", encoding="utf-8") as json_file:
    json.dump(existing_games, json_file, ensure_ascii=False, indent=4)

# Notify CLI if no new games are found
if new_games_count == 0:
    print("No new games found.")

# Close the browser
driver.quit()

import json
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the target website
driver.get("https://www.ticket-onlineshop.com/ols/haie/de/tageskarten/channel/shop/index")

# Wait for JavaScript to load
driver.implicitly_wait(10)

# Extract data from sections containing games
events = driver.find_elements(By.CLASS_NAME, 'main-content__section')

# Prepare a dictionary to store game details with unique game IDs
games = {}

# Filter and extract game-related information
game_id = 1  # Start with game ID 1
for event in events:
    text = event.text.strip()
    # Split the block of text into individual games based on "Tickets ab"
    if "Tickets ab" in text:
        game_blocks = text.split("Tickets ab")
        for i, block in enumerate(game_blocks[:-1]):  # Exclude the last empty split
            # Re-add "Tickets ab" and clean up formatting
            game_details = block.strip() + "\nTickets ab" + game_blocks[i + 1].split("\n")[0].strip()
            # Save each game with a unique ID as the key
            games[f"game_{game_id}"] = {
                "details": game_details
            }
            game_id += 1

# Save all games to a JSON file
current_date = "2025-01-19"  # Example current date for filename or metadata
with open(f"games_{current_date}.json", "w", encoding="utf-8") as json_file:
    json.dump(games, json_file, ensure_ascii=False, indent=4)

# Close the browser
driver.quit()

print(f"Saved {len(games)} games to 'games_{current_date}.json'")

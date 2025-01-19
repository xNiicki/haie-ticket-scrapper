import time
import subprocess


def run_scraper():
    while True:
        # Run the scraping script
        print("Running scraper...")
        subprocess.run(['python', 'scraper.py'])

        # Wait for 5 minutes before running again
        print("Waiting for 5 minutes...")
        time.sleep(300)


# Start the scheduler
run_scraper()

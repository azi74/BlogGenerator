from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
import os

def generate_daily_post():
    keyword = "wireless earbuds"  # Default keyword for daily generation
    print(f"Generating daily post for keyword: {keyword} at {datetime.now()}")
    
    try:
        response = requests.get(
            f"http://localhost:5000/generate?keyword={keyword}",
            timeout=60
        )
        
        if response.status_code == 200:
            # Save to file
            with open(f"posts/{keyword.replace(' ', '_')}_{datetime.now().date()}.json", 'w') as f:
                f.write(response.text)
            print("Successfully generated and saved post")
        else:
            print(f"Error generating post: {response.text}")
    except Exception as e:
        print(f"Failed to generate daily post: {str(e)}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_daily_post, 'cron', hour=9, minute=0)  # Run daily at 9 AM
    scheduler.start()
    print("Scheduler started - will generate post daily at 9 AM")
import requests

from dotenv import load_dotenv
import os

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # Replace with your bot token
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Slack channel ID

def fetch_channel_history(channel_id):
    url = f"https://slack.com/api/conversations.history?channel={channel_id}"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        messages = response.json().get("messages", [])
        return messages
    else:
        print("Error fetching history:", response.json())
        return []

# Get channel messages
messages = fetch_channel_history(CHANNEL_ID)
for message in messages:
    print(message["text"])

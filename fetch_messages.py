import requests

SLACK_BOT_TOKEN = "xoxp-8497227385956-8495179320882-8494692807107-fa303b7ce900bbefa5339114d040990a"  # Your Slack OAuth token
CHANNEL_ID = "C08EK5D3GSW"  # Slack channel ID

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

import os
import time
import re
import json
import requests
from slack_bolt import App

from dotenv import load_dotenv
import os

load_dotenv()

# Slack API credentials
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # Replace with your bot token
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET") # Your Slack app's signing secret
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")  # Deepseek R1 endpoint
BOT_USER_ID = os.getenv("BOT_USER_ID")

# Initialize Slack Bolt App
app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

# Track last response time (cooldown mechanism)
last_response_time = 0

def should_process_message():
    """Check if 10 minutes (600 seconds) have passed since the last response."""
    global last_response_time
    current_time = time.time()
    if (current_time - last_response_time) >= 600:
        last_response_time = current_time  # Update last response time
        return True
    return False

def clean_ollama_response(response_text):
    """Extract and remove the <think> content from the AI response."""
    think_match = re.search(r"<think>(.*?)</think>", response_text, re.DOTALL)
    think_content = think_match.group(1).strip() if think_match else ""
    cleaned_response = re.sub(r"<think>.*?</think>\n?", "", response_text, flags=re.DOTALL).strip()
    return cleaned_response, think_content

def get_deepseek_response(user_message, extra_context=""):
    """Send a message to Deepseek API and get a response."""
    try:
        full_prompt = user_message
        if extra_context:
            full_prompt += f"\n\nAdditional context: {extra_context}"

        payload = {
            "model": "deepseek-llm",
            "messages": [{"role": "user", "content": full_prompt}]
        }
        response = requests.post(DEEPSEEK_API_URL, json=payload)

        if response.status_code == 200:
            response_json = response.json()
            suggested_reply = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
            cleaned_reply, think_content = clean_ollama_response(suggested_reply)
            return cleaned_reply, think_content
        else:
            print(f"Deepseek API Error: {response.status_code} - {response.text}")
            return "Sorry, I encountered an issue processing your request.", ""
    except Exception as e:
        print(f"Error communicating with Deepseek: {e}")
        return "Sorry, I encountered an issue processing your request.", ""

# 🔹 Automatically Open Modal When a Message is Sent
@app.event("message")
def handle_message_events(body, client):
    """Automatically opens a modal when a message is received."""
    global last_response_time
    event = body.get("event", {})
    user_id = event.get("user", "")
    text = event.get("text", "")
    channel_id = event.get("channel", "")

    # Ignore bot messages and prevent infinite loops
    if user_id == BOT_USER_ID:
        return

    # Ignore messages if within cooldown period
    if not should_process_message():
        print("Cooldown active. Ignoring message.")
        return

    trigger_id = body["event"]["ts"]  # Use timestamp as a trigger ID
    message_ts = event["ts"]

    # Open a modal for users to add additional context
    client.views_open(
        trigger_id=trigger_id,
        view={
            "type": "modal",
            "callback_id": "context_submission",
            "private_metadata": json.dumps({"channel_id": channel_id, "message_ts": message_ts, "original_text": text}),
            "title": {"type": "plain_text", "text": "Add More Context"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*Original Message:*\n>{text}"}
                },
                {
                    "type": "input",
                    "block_id": "context_input",
                    "label": {"type": "plain_text", "text": "Enter additional details"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "context",
                        "multiline": True,
                        "placeholder": {"type": "plain_text", "text": "Provide more details for a better response..."}
                    }
                }
            ],
            "submit": {"type": "plain_text", "text": "Regenerate Response"}
        }
    )

# 🔹 Handle Modal Submission
@app.view("context_submission")
def handle_context_submission(ack, body, client):
    """Processes the additional context and regenerates the response."""
    ack()

    # Extract user input
    user_id = body["user"]["id"]
    view_state = body["view"]["state"]["values"]
    extra_context = view_state["context_input"]["context"]["value"]

    # Extract metadata (channel ID & message TS)
    metadata = json.loads(body["view"]["private_metadata"])
    channel_id = metadata["channel_id"]
    message_ts = metadata["message_ts"]
    original_text = metadata["original_text"]

    # Call Deepseek API with the updated context
    response, _ = get_deepseek_response(original_text, extra_context)

    # Send updated response back in Slack thread
    client.chat_postMessage(
        channel=channel_id,
        text=f"💡 Updated suggestion: {response}",
        thread_ts=message_ts
    )

app.start(port=3000)

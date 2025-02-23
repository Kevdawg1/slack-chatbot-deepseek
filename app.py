from slack_bolt import App
import requests
import json
import re
import time
from dotenv import load_dotenv
import os

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # Replace with your bot token
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET") # Your Slack app's signing secret
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")  # Deepseek R1 endpoint
BOT_USER_ID = os.getenv("BOT_USER_ID")

app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

last_response_time = 0  # Track last response timestamp

def should_process_message():
    """Check if 10 minutes (600 seconds) have passed since the last response."""
    global last_response_time
    current_time = time.time()
    if (current_time - last_response_time) >= 600:
        return True
    return False

def generate_response(full_context):
    # Call Deepseek API with the updated context
    request_body = {
        "model": "deepseek-r1:1.5B",
        "messages": [
            {"role": "system", "content": "You are an assistant that provides useful response suggestions on the latest main topic based on the context provided. Keep your response limited to 50 words."},
            {"role": "user", "content": full_context}
        ],
        "stream": False
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(DEEPSEEK_API_URL, json=request_body, headers=headers)

    try:
        response_json = response.json()
        suggested_reply = response_json["message"]["content"]

        # Extract and clean the <think> part
        think_match = re.search(r"<think>(.*?)</think>", suggested_reply, re.DOTALL)
        llm_thought_process = think_match.group(1).strip() if think_match else ""
        cleaned_suggested_reply = re.sub(r"<think>.*?</think>\n?", "", suggested_reply, flags=re.DOTALL).strip()

        return cleaned_suggested_reply, llm_thought_process
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
        print(response.text)

# Function to fetch channel history
def fetch_channel_history(channel_id):
    url = f"https://slack.com/api/conversations.history?channel={channel_id}"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json().get("messages", [])

# Event listener for new messages in Slack
@app.event("message")
def handle_message(event, say):
    global last_response_time
    if not should_process_message():
        print("Cooldown active. Ignoring message.")
        return # Skip processing if cooldown is active
    print(event)
    if event.get("user") == BOT_USER_ID:
        return  # Skip bot messages
    if event.get("subtype") == "message_deleted":
        return # Skip deleted messages
    
    channel_id = event["channel"]
    
    # Fetch the full conversation history
    messages = fetch_channel_history(channel_id)
    context = "\n".join([msg["text"] for msg in messages])  # Combine previous messages into context
    
    user_message = event["text"]
    full_context = context + "\nUser: " + user_message  # Append user's new message to context
    # Call Deepseek R1 API for a suggested response
    
    try:
        suggested_reply, llm_thought_process = generate_response(full_context)

        print(f"Model Thought Process: {llm_thought_process}")
        current_time = time.time()
        last_response_time = current_time
        say(f"{suggested_reply}", thread_ts=event["ts"])
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
    

# Event listener for additional context (e.g., button press or input field)
@app.shortcut("add_context")
def handle_additional_context(ack, body, say):
    ack()  # Acknowledge the interaction
    
    user_context = body["message"]["text"]  # Get new context added by user
    message_thread_ts = body["message"]["ts"]
    
    # Fetch previous conversation context
    messages = fetch_channel_history(body["channel"]["id"])
    context = "\n".join([msg["text"] for msg in messages])  # Combine previous messages
    
    # Generate new message suggestion with additional context
    full_context = context + "\nUser: " + user_context
    
    # Call Deepseek R1 API with the updated context
    response = requests.post(DEEPSEEK_API_URL, json={
        "model": "deepseek-r1",
        "messages": [{"role": "user", "content": full_context}]
    }).json()

    suggested_reply = response["choices"][0]["message"]["content"]
    
    # Send the new suggested response
    say(f"💡 Updated suggestion: {suggested_reply}", thread_ts=message_thread_ts)

# 🔹 **Shortcut to Open Context Modal**
@app.shortcut("add_context")
def open_context_modal(ack, body, client):
    """Opens a modal where users can add more context."""
    ack()

    trigger_id = body["trigger_id"]
    message_ts = body["message"]["ts"]
    channel_id = body["channel"]["id"]

    # Open a Slack modal for users to add additional context
    view_response = client.views_open(
        trigger_id=trigger_id,
        view={
            "type": "modal",
            "callback_id": "context_submission",
            "private_metadata": json.dumps({"channel_id": channel_id, "message_ts": message_ts}),
            "title": {"type": "plain_text", "text": "Add More Context"},
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": "*Fetching past messages...*"}}
            ],
            "submit": {"type": "plain_text", "text": "Regenerate Response"}
        }
    )
    
    view_id = view_response["view"]["id"]
    
    messages = fetch_channel_history(channel_id)
    previous_context = "\n".join([msg["text"] for msg in messages])
    
    suggested_reply, _ = generate_response(previous_context)
    
    client.views_update(
        view_id=view_id,
        view={
            "type": "modal",
            "callback_id": "context_submission",
            "title": {"type": "plain_text", "text": "Add More Context"},
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": f"*AI Suggested Response:*\n{suggested_reply}"}},
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
    print("Context modal opened.")

# 🔹 **Handle Modal Submission**
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

    # Fetch previous conversation context
    messages = fetch_channel_history(channel_id)
    previous_context = "\n".join([msg["text"] for msg in messages])

    # Append additional user context
    full_context = previous_context + f"\nMy Perspective: {extra_context}"

    try:
        # Generate a new response based on the updated context
        suggested_reply, llm_thought_process = generate_response(full_context)
        # Send updated response back in Slack thread
        client.chat_postMessage(
            channel=channel_id,
            text=suggested_reply,
            thread_ts=message_ts,
            user=user_id
        )

        print(f"💡 Model Thought Process: {llm_thought_process}")

    except Exception as e:
        print(f"Error processing additional context: {e}")


app.start(port=3000)
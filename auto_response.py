from slack_bolt import App
import requests
import json
import re
import time

SLACK_BOT_TOKEN = "xoxp-8497227385956-8495179320882-8494692807107-fa303b7ce900bbefa5339114d040990a"
SLACK_SIGNING_SECRET = "fa764f343a37d410d578698f39b76e30"
DEEPSEEK_API_URL = "http://localhost:11434/api/chat"  # Deepseek R1 endpoint
BOT_USER_ID = "U08EK599ERY"

app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

last_response_time = 0  # Track last response timestamp

def should_process_message():
    """Check if 10 minutes (600 seconds) have passed since the last response."""
    global last_response_time
    current_time = time.time()
    if (current_time - last_response_time) >= 600:
        return True
    return False

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
    request_body = {
        "model": "deepseek-r1:1.5B",
        "messages": [
            {"role": "system", "content": "You are an assistant that provides useful response suggestions on the latest main topic based on the context provided. Keep your response limited to 50 words"},
            {"role": "user", "content": full_context}
        ],
        "stream": False
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(DEEPSEEK_API_URL, json=request_body, headers=headers)#.json()
    try:
        response_json = response.json()
        response_json = response.json()
        suggested_reply = response_json["message"]["content"]
        think_match = re.search(r"<think>(.*?)</think>", suggested_reply, re.DOTALL)
        llm_thought_process = think_match.group(1).strip() if think_match else ""

        print(f"Model Thought Process: {llm_thought_process}")
        cleaned_suggested_reply = re.sub(r"<think>.*?</think>\n?", "", suggested_reply, flags=re.DOTALL).strip()
        # print(cleaned_suggested_reply)
        current_time = time.time()
        last_response_time = current_time
        say(f"{cleaned_suggested_reply}", thread_ts=event["ts"])
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
        print(response.text)
    

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

# @app.command("/suggest_response")
# def handle_slash_command(ack, respond, command):
#     ack()  # Acknowledge the command
#     user_message = command["text"]
    
#     # Process the message and generate a response
#     suggested_reply = generate_response(user_message)
#     respond(f"Suggested reply: {suggested_reply}")


app.start(port=3000)
import os
import time
import re
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Slack API credentials
SLACK_BOT_TOKEN = "xoxp-8497227385956-8495179320882-8494692807107-fa303b7ce900bbefa5339114d040990a"  # Replace with your bot token
SLACK_SIGNING_SECRET = "fa764f343a37d410d578698f39b76e30"  # Replace with your Slack signing secret
SLACK_APP_TOKEN = "xapp-1-A08EM6W5H6Y-8494891668883-922b4aa135a8d9d1b5e028b14c6e054eb4e71bd2faca582bf0d218233c840d0c"  # Needed for Socket Mode
OLLAMA_API_URL = "http://localhost:11434/v1/chat"  # Ollama API URL
BOT_USER_ID = "U08EK599ERY"  # Replace with your bot's Slack User ID

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

def get_ollama_response(user_message, extra_context=""):
    """Send a message to Ollama and get a response."""
    try:
        full_prompt = user_message
        if extra_context:
            full_prompt += f"\n\nAdditional context: {extra_context}"

        payload = {
            "model": "deepseek-llm",  # Replace with your model
            "messages": [{"role": "user", "content": full_prompt}]
        }
        response = requests.post(OLLAMA_API_URL, json=payload)

        if response.status_code == 200:
            response_json = response.json()
            suggested_reply = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
            cleaned_reply, think_content = clean_ollama_response(suggested_reply)
            return cleaned_reply, think_content
        else:
            print(f"Ollama API Error: {response.status_code} - {response.text}")
            return "Sorry, I encountered an issue processing your request.", ""
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return "Sorry, I encountered an issue processing your request.", ""

@app.event("message")
def handle_message_events(body, client):
    """Handles messages posted in a Slack channel and opens a message draft modal."""
    global last_response_time
    event = body.get("event", {})
    user_id = event.get("user", "")
    text = event.get("text", "")
    channel = event.get("channel", "")

    # Ignore bot messages and prevent infinite loops
    if user_id == BOT_USER_ID:
        return

    # Ignore messages if within cooldown period
    if not should_process_message():
        print("Cooldown active. Ignoring message.")
        return

    # Process user messages
    if text:
        response, think_content = get_ollama_response(text)

        # Open a modal with the suggested response in a text input field
        client.views_open(
            trigger_id=body["event"]["ts"],  # Use the message timestamp as trigger_id
            view={
                "type": "modal",
                "callback_id": "message_draft",
                "private_metadata": f"{channel}|{text}",  # Store channel and original text
                "title": {"type": "plain_text", "text": "Edit Your Response"},
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "response_block",
                        "label": {"type": "plain_text", "text": "Suggested Reply"},
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "response_input",
                            "multiline": True,
                            "initial_value": response  # Prefill message draft
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "context_block",
                        "label": {"type": "plain_text", "text": "Add More Context (Optional)"},
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "context_input",
                            "multiline": True,
                            "placeholder": {"type": "plain_text", "text": "Add any extra details to refine the response..."}
                        }
                    }
                ],
                "submit": {"type": "plain_text", "text": "Send"},
                "close": {"type": "plain_text", "text": "Regenerate"},
            }
        )
        print(f"Extracted <think> content: {think_content}")

@app.view("message_draft")
def handle_message_submission(ack, body, client):
    """Handles the message submission when the user edits the draft or regenerates the response."""
    ack()  # Acknowledge the request

    user_id = body["user"]["id"]
    private_metadata = body["view"]["private_metadata"]
    channel, original_message = private_metadata.split("|")

    response_text = body["view"]["state"]["values"]["response_block"]["response_input"]["value"]
    extra_context = body["view"]["state"]["values"]["context_block"]["context_input"]["value"]

    if body["view"]["state"]["values"]["context_block"]["context_input"]["value"]:
        # Regenerate response with additional context
        new_response, _ = get_ollama_response(original_message, extra_context)

        # Reopen the modal with the updated response
        client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "callback_id": "message_draft",
                "private_metadata": private_metadata,
                "title": {"type": "plain_text", "text": "Edit Your Response"},
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "response_block",
                        "label": {"type": "plain_text", "text": "Suggested Reply"},
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "response_input",
                            "multiline": True,
                            "initial_value": new_response  # Updated response
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "context_block",
                        "label": {"type": "plain_text", "text": "Add More Context (Optional)"},
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "context_input",
                            "multiline": True,
                            "placeholder": {"type": "plain_text", "text": "Add any extra details to refine the response..."}
                        }
                    }
                ],
                "submit": {"type": "plain_text", "text": "Send"},
                "close": {"type": "plain_text", "text": "Regenerate"},
            }
        )
    else:
        # Send the final user-approved message
        client.chat_postMessage(channel=channel, text=response_text)

# Start the Slack bot using Socket Mode
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

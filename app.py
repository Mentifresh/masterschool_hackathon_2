import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
api_key = os.environ["api_key_sid"]
api_secret = os.environ["api_key_secret"]
account_sid = os.environ["account_sid"]
service_sid = os.environ["conversation_service_id"]

# Initialize the client
client = Client(api_key, api_secret, account_sid)

# Check for existing conversations
conversations = client.conversations.v1.services(service_sid).conversations.list(limit=20)
existing_conversation = None

print("Checking for existing conversations...")
for conv in conversations:
    print(f"Found conversation: {conv.sid} - {conv.friendly_name}")
    # We'll use the first conversation we find
    if not existing_conversation:
        existing_conversation = conv

# If no conversations exist, create a new one
if not existing_conversation:
    print("No existing conversations found. Creating a new one...")
    existing_conversation = client.conversations.v1.services(service_sid).conversations.create(
        friendly_name="WhatsApp Test Conversation"
    )
    
    print(f"Created new conversation with SID: {existing_conversation.sid}")
    
    # Add yourself as a WhatsApp participant to the new conversation
    try:
        participant = client.conversations.v1.services(service_sid).conversations(
            existing_conversation.sid
        ).participants.create(
            messaging_binding_address="whatsapp:+4917622933043",  # Your WhatsApp number
            messaging_binding_proxy_address="whatsapp:+493041736523"  # The hackathon WhatsApp number
        )
        print(f"Added participant with SID: {participant.sid}")
        
        print("===== IMPORTANT =====")
        print("Send a message from your WhatsApp now")
        print("Previous initiation of the conversation is required.")
        print("After you've sent a message, run this script again to send a response.")
        print("============================")
    except Exception as e:
        print(f"Error adding participant: {e}")
        print("This is expected if you're already a participant in another conversation.")

else:
    print(f"Using existing conversation with SID: {existing_conversation.sid}")
    
    # Try to send a message to the existing conversation
    try:
        message = client.conversations.v1.services(service_sid).conversations(
            existing_conversation.sid
        ).messages.create(
            body="Hello from the WhatsApp Hackathon Bot! This is an automated response."
        )
        print(f"Message sent! Message SID: {message.sid}")
    except Exception as e:
        print(f"Error sending message: {e}")
        print("Make sure you've already sent a message from your WhatsApp to +493041736523 first.")

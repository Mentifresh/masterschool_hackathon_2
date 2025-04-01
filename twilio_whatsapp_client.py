import os
import time
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class WhatsAppBot:
    def __init__(self, message_callback=None):
        # Load environment variables
        self.api_key = os.environ["api_key_sid"]
        self.api_secret = os.environ["api_key_secret"]
        self.account_sid = os.environ["account_sid"]
        self.service_sid = os.environ["conversation_service_id"]
        
        # Initialize the client
        self.client = Client(self.api_key, self.api_secret, self.account_sid)
        
        # Initialize conversation
        self.conversation = None
        self.last_processed_messages = set()  # Track messages by SID
        self.your_whatsapp = "whatsapp:+4917622933043"
        self.twilio_whatsapp = "whatsapp:+493041736523"
        
        # Store the callback function
        self.message_callback = message_callback
    
    def setup_conversation(self):
        """Sets up the conversation - finds existing or creates new one"""
        # Check for existing conversations
        conversations = self.client.conversations.v1.services(self.service_sid).conversations.list(limit=20)
        
        print("Checking for existing conversations...")
        for conv in conversations:
            print(f"Found conversation: {conv.sid} - {conv.friendly_name}")
            # We'll use the first conversation we find
            if not self.conversation:
                self.conversation = conv

        # If no conversations exist, create a new one
        if not self.conversation:
            print("No existing conversations found. Creating a new one...")
            self.conversation = self.client.conversations.v1.services(self.service_sid).conversations.create(
                friendly_name="WhatsApp Test Conversation"
            )
            
            print(f"Created new conversation with SID: {self.conversation.sid}")
            
            # Add yourself as a WhatsApp participant to the new conversation
            try:
                participant = self.client.conversations.v1.services(self.service_sid).conversations(
                    self.conversation.sid
                ).participants.create(
                    messaging_binding_address=self.your_whatsapp,  # Your WhatsApp number
                    messaging_binding_proxy_address=self.twilio_whatsapp  # The hackathon WhatsApp number
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
            print(f"Using existing conversation with SID: {self.conversation.sid}")
        
        return self.conversation
    
    def send_message(self, message_body):
        """Sends a message to the conversation"""
        if not self.conversation:
            print("No conversation available. Run setup_conversation() first.")
            return False
        
        try:
            message = self.client.conversations.v1.services(self.service_sid).conversations(
                self.conversation.sid
            ).messages.create(
                body=message_body
            )
            print(f"Message sent! Message SID: {message.sid}")
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            print("Make sure you've already sent a message from your WhatsApp to +493041736523 first.")
            return False
    
    def poll_for_new_messages(self, interval=5):
        """Polls for new messages every 'interval' seconds"""
        if not self.conversation:
            print("No conversation available. Run setup_conversation() first.")
            return
        
        print(f"Starting to poll for new messages every {interval} seconds...")
        print("Press Ctrl+C to stop polling.")
        
        # Get current messages to establish baseline
        messages = self.client.conversations.v1.services(self.service_sid).conversations(
            self.conversation.sid
        ).messages.list(limit=20)
        
        # Initialize with current message SIDs
        for message in messages:
            self.last_processed_messages.add(message.sid)
            
        print(f"Current message count: {len(self.last_processed_messages)}")
        
        try:
            while True:
                # Get latest messages
                messages = self.client.conversations.v1.services(self.service_sid).conversations(
                    self.conversation.sid
                ).messages.list(limit=20)
                
                # Check for new messages by comparing SIDs
                new_messages = []
                for message in messages:
                    if message.sid not in self.last_processed_messages:
                        new_messages.append(message)
                        self.last_processed_messages.add(message.sid)
                
                # Process and display new messages
                if new_messages:
                    print(f"New message! ({len(new_messages)} new messages)")
                    
                    # Process the new messages (newest first)
                    for message in new_messages:
                        print(f"From: {message.author if hasattr(message, 'author') else 'unknown'}, Body: {message.body}")
                        
                        # If a callback function is provided, call it with the message
                        if self.message_callback:
                            self.message_callback(message)
                
                # Wait for the next polling interval
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nStopped polling for messages.")


if __name__ == "__main__":
    bot = WhatsAppBot()
    bot.setup_conversation()
    
    # Test message
    # bot.send_message("Hello from the WhatsApp Bot!")
    
    # Start polling for new messages every 5 seconds
    bot.poll_for_new_messages(5)

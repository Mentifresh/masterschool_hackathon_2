from twilio_whatsapp_client import WhatsAppBot

# Message handler with business logic
def handle_message(message):
    """Process incoming WhatsApp messages and implement business logic"""
    # Skip messages from the bot itself
    if hasattr(message, 'author') and message.author == "system":
        return
    
    print(f"🔔 Processing message: {message.body}")
    

# Create the bot with our message handler
bot = WhatsAppBot(message_callback=handle_message)

if __name__ == "__main__":
    try:
        # Setup the WhatsApp conversation
        bot.setup_conversation()
        
        # Send a welcome message
        # bot.send_message("NutriScan is now active!")
        
        # Start polling for new messages (will run indefinitely)
        bot.poll_for_new_messages(5)  # Check every 5 seconds
    except Exception as e:
        print(f"Error in main application: {e}")






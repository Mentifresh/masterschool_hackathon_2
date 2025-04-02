from twilio_whatsapp_client import WhatsAppBot
from data_manager import DataManager

# Create data manager instance
data_manager = DataManager()

def handle_message(message):
    """Process incoming WhatsApp messages and implement business logic"""
    # Skip messages from the bot itself
    if hasattr(message, 'author') and message.author == "system":
        return
    
    # Handle text message
    if hasattr(message, 'body'):
        print(f"📱 Message received: {message.body}")
    
    # Handle images
    media_list = []
    if hasattr(message, 'media') and isinstance(message.media, list):
        media_list = message.media
    elif hasattr(message, 'media_items'):
        media_list = message.media_items
    
    # Process any images
    for media_item in media_list:
        # Extract media info consistently
        media_type = (
            media_item.get('content_type') if isinstance(media_item, dict)
            else getattr(media_item, 'content_type', 'unknown')
        )
        media_sid = (
            media_item.get('sid') if isinstance(media_item, dict)
            else getattr(media_item, 'sid', 'unknown')
        )
        
        # Only process images
        if media_type.startswith('image/'):
            print(f"📸 Processing image...")
            local_file = data_manager.save_media_to_img_folder(
                service_sid=bot.service_sid,
                media_sid=media_sid,
                api_key=bot.api_key,
                api_secret=bot.api_secret,
                content_type=media_type
            )
            
            if local_file:
                print(f"✅ Image saved: {local_file}")

# Create the bot with our message handler
bot = WhatsAppBot(message_callback=handle_message)

if __name__ == "__main__":
    try:
        # Setup the WhatsApp conversation
        bot.setup_conversation()
        
        print("\nStarting automatic message polling (every 5 seconds, last 50 messages)...")
        print("Press Ctrl+C to stop polling.")
        
        # Start automatic polling
        bot.poll_for_new_messages(interval=5, limit=50, reset_history=True)
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
    except Exception as e:
        print(f"Error in main application: {e}")






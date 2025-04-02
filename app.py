from twilio_whatsapp_client import WhatsAppBot
from data_manager import DataManager

# Create data manager instance
data_manager = DataManager()
# Flag to indicate initial message processing is done
initial_processing_complete = False
# Set to store message SIDs that arrived after initialization
new_message_sids = set()

def handle_message(message):
    """Process incoming WhatsApp messages and implement business logic"""
    global initial_processing_complete, new_message_sids
    
    # Skip messages from the bot itself
    if hasattr(message, 'author') and message.author == "system":
        return
    
    message_text = None
    image_location = None
    message_sid = getattr(message, 'sid', 'unknown')
    
    # Handle text message
    if hasattr(message, 'body'):
        print(f"📱 Message received: {message.body}")
        message_text = message.body
    
    # If we're in the initial processing phase, we only track message SIDs
    # but don't download any images
    if not initial_processing_complete:
        # Just record that we've seen this message
        if hasattr(message, 'media') or hasattr(message, 'media_items'):
            print(f"⏭️ Skipping media download during initial processing: {message_sid}")
        return
    
    # Once initial processing is complete, any new message should be fully processed
    # Add this message to the set of new messages
    new_message_sids.add(message_sid)
    
    # Handle images - only for messages that came in after initial processing
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
        
        # We can potentially extract any kind of media here
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
                image_location = local_file
    
    ############################
    # Here we can plug in OpenAI
    ############################
    if image_location:
        print(f"Image saved at: {image_location}")
    elif message_text:
        print(f"Text message: {message_text}")

# Create the bot with our message handler
bot = WhatsAppBot(message_callback=handle_message)

if __name__ == "__main__":
    try:
        # Setup the WhatsApp conversation
        bot.setup_conversation()
        
        print("\nStarting initial message processing (without downloading images)...")
        # Initial processing - process all messages but don't download images
        initial_messages = bot.process_recent_messages(limit=50)
        if not initial_messages:
            print("No messages found initially.")
        else:
            print(f"Processed {len(initial_messages)} message(s) during initialization.")
        
        # Set the flag to indicate we're done with initial processing
        initial_processing_complete = True
        print("\nInitial processing complete. Now downloading images for new messages only.")
        
        print("\nStarting automatic message polling (every 5 seconds, last 50 messages)...")
        print("Press Ctrl+C to stop polling.")
        
        # Start automatic polling - process all messages but images only for new ones
        bot.poll_for_new_messages(interval=5, limit=50, reset_history=False)
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
    except Exception as e:
        print(f"Error in main application: {e}")






# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

## First initialize the client
## Then create a conversation
## Then add a participant
## Then send a message from the phone
## Then we can send one from the code

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ["account_sid"]
# auth_token = os.environ["api_key_secret"]
# client = Client(account_sid, auth_token)

api_key = os.environ["api_key_sid"]
api_secret = os.environ["api_key_secret"]
account_sid = os.environ["account_sid"]
client = Client(api_key, api_secret, account_sid)

conversation = client.conversations.v1.conversations.create(
    friendly_name="Test Conversation"
)


conversations = client.conversations.v1.conversations(
    conversation.sid
).fetch()

print("conversation sid: ", conversations.links['messages'])

# participant = client.conversations.v1.conversations(
#     conversation.sid
# ).participants.create(identity="testPineapple")

# print("participant sid: ", participant.sid)

# message = client.messages.create(
#     to="+4917622933043",
#     from_="+493041736523",
#     body="Hello from Python!")

# print("message sid: ", message.sid)
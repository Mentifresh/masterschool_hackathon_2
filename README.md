# masterschool_hackathon_2

# NutriScan

A smart application that helps you discover recipes while keeping track of nutritional values.
NutriScan makes healthy cooking easier by providing nutritional insights for your meals.

## Features

- Recipe suggestions based on available ingredients
- Detailed nutritional information for each recipe
- Easy-to-follow cooking instructions
- Customizable dietary preferences

## Getting Started

### Prerequisites

- Python

### Installation

1. Clone the repository

2. Set up environment variables:

   - Make a copy of `.env.example` and rename it to `.env`
   - Keep the `.env.example` file for reference
   - Add your API keys and other required values to the `.env` file

3. Install dependencies:
   TO BE ADDED

4. Start the development server:
   TO BE ADDED

### Modules Planning

- OpenAI Module (input: image and/or text, output: text with links)

  - Connect to OpenAI
  - Define intructions
  - first return a list of possible recipes
  - after recipe confirmation, generate full recipe
  - return full recipe

- Twilio Module (input: text with links, ouput: image and/or text)

  - Connect to twilio
  - start polling (fetch messages)
  - save messages
  - if new messages, return them

- Flask app (server -- main.py) (Is there any rate limiting?)
  - Initiate Twilio
  - Check for messages
  - If there is a message:
    - Forward to openAI
    - Get Answer
    - Forward to back to user
  - Received recipes can be stored as json

### Optional tasks

- Add a website with saved (jinja templates)!
- third API service for recipes

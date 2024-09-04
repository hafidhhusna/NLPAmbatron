import discord
import os
import re

# Load environment variables from .env file

# Define patterns and responses
patterns_responses = {
    r'hi|hello|hey': 'Hello! How can I assist you today?',
    r'how are you': 'I am just a bot, but I am doing great! How about you?',
    r'what is your name': 'I am a chatbot created to assist you with your questions.',
    r'(.*) your (favorite|favourite) (.*)': 'I do not have preferences, but I enjoy helping you!',
    r'thank you|thanks': 'You are welcome! If you have more questions, feel free to ask.',
    r'bye|goodbye': 'Goodbye! Have a great day!'
}

# Default response for unmatched patterns
default_response = "I'm sorry, I don't understand that. Can you please rephrase?"

# Function to match user input to a pattern and return the corresponding response
def get_response(user_input):
    for pattern, response in patterns_responses.items():
        if re.search(pattern, user_input, re.IGNORECASE):
            return response
    return default_response

# Initialize the bot with intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Get the chatbot response
    user_input = message.content
    response = get_response(user_input)

    # Send the response back to the Discord channel
    await message.channel.send(response)

client.run()

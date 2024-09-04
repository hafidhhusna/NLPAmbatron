import discord
import os
import re
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

# YouTube Data API setup
youtube_api_key = os.getenv('youtube_api')
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# Function to search YouTube and return the first video link
def search_youtube(keyword):
    request = youtube.search().list(
        part="snippet",
        q=keyword,
        type="video",
        maxResults=1
    )
    response = request.execute()

    # If a video is found, return its link
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return "Sorry, I couldn't find a video for that."

# Define patterns and responses with support for callable functions
patterns_responses = {
    r'\$search youtube for (.+)': lambda keyword: f"Searching for '{keyword}' YouTube video...\n{search_youtube(keyword)}",
    r'hi|hello|hey|halo|hai': lambda _: 'Hello! How can I assist you today?',
    r'how are you': lambda _: 'I am just a bot, but I am doing great! How about you?',
    r'what is your name': lambda _: 'I am a chatbot created to assist you with your questions.',
    r'(.*) your (favorite|favourite) (.*)': lambda _: 'I do not have preferences, but I enjoy helping you!',
    r'thank you|thanks': lambda _: 'You are welcome! If you have more questions, feel free to ask.',
    r'bye|goodbye': lambda _: 'Goodbye! Have a great day!'
}

# Default response for unmatched patterns
default_response = "I'm sorry, I don't understand that. Can you please rephrase?"

# Function to match user input to a pattern and return the corresponding response
def get_response(user_input):
    for pattern, func in patterns_responses.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            # Call the function associated with the matched pattern
            return func(match.group(1) if match.groups() else None)
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

    user_input = message.content

    # Get the response based on user input
    response = get_response(user_input)

    # Send the response back to the Discord channel
    await message.channel.send(response)

# Run the bot with the token from the .env file
token = os.getenv('token')
client.run(token)

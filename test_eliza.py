import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('MTI4MDQ4MjM0OTEwODMwMTg5Ng.GkmBp0.9uvw3yhYrFkzz8tldV3JhNlaUZSqkdkFAWPnLc')

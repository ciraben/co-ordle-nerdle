#!/usr/bin/env python3
import discord as ds
import os
import sys


with open('token') as f:
    TOKEN = f.read().strip()
CHANNELS = ('bot-tester', 'wordlelikes')
WORD = 'QWERTY'

#sys.exit()

# add any "intents" (permissions we want) here
intents = ds.Intents.default()
intents.message_content = True

client = ds.Client(intents=intents)

# event listeners
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print(f'Accessing servers {[g.name for g in client.guilds]}')
    print(f'Reading messages in #{CHANNELS}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name not in CHANNELS:
        return
    
    content = message.content

    if content in ('$hello','!hello'):
        await message.channel.send(f'Hello {message.author.mention}!')
    elif content in ('$help','$info', '$rules', '!help', '!info', '!rules'):
        await message.channel.send('I am but a humble botto, pls don\'t expect too much of me.')
    elif content.startswith('!') and len(content) != 7:
        await message.channel.send('Try guessing a 6-letter word instead.')
    elif content.startswith('!') and len(content) == 7:
        guess = content[1:].upper()
        if guess == WORD:
            await message.channel.send(f'**{WORD}** – you got it, yay!✨')
            return
        response = ''
        for i in range(6):
            if guess[i] == WORD[i]:
                response += '**' + guess[i] + '**'
            elif guess[i] in WORD:
                response += guess[i]
            else:
                response += guess[i].lower()
        # await message.channel.send('You did it! You guessed a 6-letter word!!')
        await message.channel.send(response)


client.run(TOKEN)

#!/usr/bin/env python3
import discord as ds
import os
import sys

# 6-letter word db
# https://www.wordgamedictionary.com/word-lists/6-letter-words/6-letter-words.json

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
    # elif add other bot commands up here ^
    elif content.startswith('!') and len(content) != 7:
        # ignore other non-guesses
        return
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
        # remove instances of **** from response so bolding works
        response = ''.join(response.split('****'))

        await message.channel.send(response)


client.run(TOKEN)

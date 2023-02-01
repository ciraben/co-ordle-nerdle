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
        await message.channel.send(wordle_logic(message))

def wordle_logic(message):
    guess = message.content[1:].upper()
    if guess == WORD:
        # await message.channel.send(f'**{WORD}** – you got it, yay!✨')
        return '**' + WORD + '** – you got it, yay!✨'
    response = ''
    guess_status = [0]*6
    word_left = WORD
    # check for greens
    for i in range(6):
        if guess[i] == WORD[i]:
            # response += '**' + guess[i] + '**'
            guess_status[i] = 2
            word_left = word_left[:i] + '0' + word_left[i+1:]
    # check for yellows
    for i in range(6):
        if guess[i] in word_left and guess_status[i] == 0:
            # response += guess[i]
            guess_status[i] = 1
            j = word_left.find(guess[i])
            word_left = word_left[:j] + '0' + word_left[j+1:]
    # construct response
    for i in range(6):
        if guess_status[i] == 0:
            response += guess[i].lower()
        elif guess_status[i] == 1:
            response += guess[i]
        elif guess_status[i] == 2:
            response += '**' + guess[i] + '**'
    # remove instances of **** from response so bolding works
    response = ''.join(response.split('****'))
    return response



client.run(TOKEN)

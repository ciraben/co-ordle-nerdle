#!/usr/bin/env python3
import discord as ds
import os
import sys
import random

with open('token') as f:
    TOKEN = f.read().strip()
CHANNELS = ('bot-tester', 'wordlelikes')
with open('wordlist') as f:
    WORD_LIST = f.read().split(' ')

# WORD = 'qwerty'
def new_word():
    global WORD
    WORD = random.choice(WORD_LIST)
    print(f'new word is {WORD}')

# new_word()
# print(WORD)
# sys.exit()

# add any "intents" (discord permissions we want) here
intents = ds.Intents.default()
intents.message_content = True

client = ds.Client(intents=intents)

# event listeners
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print(f'Accessing servers {[g.name for g in client.guilds]}')
    print(f'Reading messages in #{CHANNELS}')
    new_word()

@client.event
async def on_message(message):
    # ignore these messages
    if message.author == client.user:
        return
    if message.channel.name not in CHANNELS:
        return
    
    # fun chatter
    if message.content == '!hello':
        await message.channel.send(f'Hello {message.author.mention}!')
        return
    if message.content in ('$help','$info', '$rules', '!help', '!info', '!rules'):
        await message.channel.send('I am but a humble botto, pls don\'t expect too much of me.')
        return
    
    # ignore these too
    if not message.content.startswith('!') or len(message.content) != 7:
        return
    
    # game content starts here
    if message.content.startswith('!') and message.content[1:] not in WORD_LIST:
        await message.channel.send('Not a valid word nope!')
        return
    if message.content[1:].lower() == WORD:
        await message.channel.send(f'**{WORD.upper()}** – you got it, yay!✨')
        # reset game here
        new_word()
        await message.channel.send('okay, new game!')
        return
    if message.content.startswith('!'):
        guess = wordle_logic(message)
        print(f'{message.author} guessed {guess}')
        await message.channel.send(guess)

def wordle_logic(message):
    guess = message.content[1:].lower()
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
    response = ''
    for i in range(6):
        if guess_status[i] == 0:
            response += guess[i].lower()
        elif guess_status[i] == 1:
            response += guess[i].upper()
        elif guess_status[i] == 2:
            response += '**' + guess[i].upper() + '**'
    # remove instances of **** from response so bolding works
    response = ''.join(response.split('****'))
    return response



client.run(TOKEN)

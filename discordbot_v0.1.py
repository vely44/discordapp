"""
This is a simple discord bot that can be used to schedule events and send reminders to users.
Used for private discord servers.
Functions:
    - ask users for their availability every week (reminder)
    - build a schedule based on user availability
    - schedule mandatory weekly events/meetings
    - schedule custom optional events/meetings
    - send reminders to users that have events/meetings scheduled
Extra features:
Save data in a database. Update the database with new events and user availability every day.
"""
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
import aiohttp
import os
from datetime import datetime, timedelta, timezone

# total time for delay between reminders
total_time = 3 # minutes
# reminder coordonates
# Get the time in hours and save it in x

x = 12
y = 55

# middle reminder
yone = y-5  # 5 minutes before the end of the total time
xone = x-1 # 1 hour before the end of the total time
# Get the token from a file
token = ""
with open("token.txt","r") as tokenFile:
    token = tokenFile.read().strip()
    tokenFile.close()

# Create a discord client
class MyClient(discord.Client):
    # Print a message when the bot is ready
    async def on_ready(self):
        print('Logged on as', self.user)
        # Schedule the weekly message
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.send_weekly_message, CronTrigger(day_of_week='fri', hour=x, minute=y))
        scheduler.start()

    # Respond to messages
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')
            print('Pong was used')
    
    # Send reminder message to users in one channel every week sunday at 23:59
    async def send_weekly_message(self):
        channel = self.get_channel(1277573107044974592)  # bot-meeting channel id
        await channel.send("Please do not forget to submit your JSON file with your availability for the next week.")
        # Schedule reminders
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.one_hour_left_message, CronTrigger(day_of_week='sat', hour=xone, minute=y)) # change the day of the week
        scheduler.add_job(self.five_min_left_message, CronTrigger(day_of_week='sat', hour=x, minute=yone))
        scheduler.add_job(self.time_elapsed_message, CronTrigger(day_of_week='sat', hour=x, minute=y))
        scheduler.start()

    async def one_hour_left_message(self):
        channel = self.get_channel(1277573107044974592)
        await channel.send("One hour left to submit your JSON file!") 

    async def five_min_left_message(self):
        channel = self.get_channel(1277573107044974592)
        await channel.send("Five minutes left to submit your JSON file!") 

    async def time_elapsed_message(self):
        channel = self.get_channel(1277573107044974592)
        await channel.send("Time is up!")
        await self.read_channel_for_json_files(channel)


    async def read_channel_for_json_files(self, channel):
        async for message in channel.history(oldest_first=True):
            for attachment in message.attachments:
                if attachment.filename.endswith('.json'):
                    await self.download_file(attachment)
                    await channel.send(f"Downloaded and deleted: {attachment.filename} send by {message.author.display_name}")
                    await message.delete()
        await channel.send("All JSON files have been downloaded.")

    async def download_file(self, attachment):
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as response:
                if response.status == 200:
                    file_path = os.path.join('downloads', attachment.filename)
                    with open(file_path, 'wb') as f:
                        f.write(await response.read())
                    print(f'Downloaded {attachment.filename}')


# Functions for file management
#def merge_files():
    

# Run the bot
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(token)


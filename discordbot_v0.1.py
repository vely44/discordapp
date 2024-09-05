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
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
import aiohttp
import os
from datetime import datetime, timedelta, timezone

#import a file for extra functions
import merge_files_script
#list of accepted user ids
admin_user_id_list = [452424972090998804, 416556479374426122]

#Time for the main reminders
x = 12
y = 55

# middle reminder
yone = y-5  # 5 minutes before the end of the total time
xone = x-1  # 1 hour before the end of the total time
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
        #print Turn on message in the channel bot-meeting
        channel = self.get_channel(1277573107044974592)
        await channel.send("Bot is turned on!")
        # print in the channel the time of the next due date
        await channel.send(f"Next due date: {scheduler.get_jobs()[0].next_run_time + timedelta(days=1)}")
    
    # Respond to messages
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        # Ping function
        # Description: Respond to the message "ping" with "pong"
        #
        # Output  : "pong"
        if message.content == 'ping':
            await message.channel.send('pong')
            print('Pong was used')
            merge_files_script.merge_files()
            print("All JSON files have been merged.")


        # Admin command for downloading the last file from the /downloads/combined folder
        # Command : dl
        # Description: Download the last file from the /downloads/combined folder
        #
        # Input   : None
        #
        # Output  : "Downloaded <filename>"
        if message.content == 'dl':
            # Check if the user is accepted to use the command
            if message.author.id not in admin_user_id_list:
                await message.channel.send("You are not allowed to use this command.")
                await message.author.send("Your ID is: " + str(message.author.id))
                return
            else:
                # Get the last file from the /downloads/combined folder
                file_list = os.listdir('downloads/combined')
                last_file = file_list[-1]
                # Send a message to the user that sent the command via a private message
                # Attach the file to the message
                await message.author.send(f"Downloaded {last_file}")
                await message.author.send(file=discord.File(f'downloads/combined/{last_file}'))
                # Tell the channel that the file has been downloaded by the admin
                await message.channel.send(f"Downloaded {last_file}")


        # Command : /meet 
        # Format  : /meet <number of users> <user1> <user2> ... <userN>
        # Description: Schedule a meeting with the specified users based on the availability of each user that is stored in a JSON file.
        # Description: The bot will suggest 3 possible dates for the meeting after overlapping the availability of the users.
        # Example : /meet 3 user1 user2  # Schedule a meeting with 3 users (yourself, user1, user2)
        # 
        # Input   : combined_data - list of JSON objects
        #
        #
        # Output  : "You can meet with user1, user2, user3 at: "
        # Output  : " <First Suggestion> "
        # Output  : " <Second Suggestion> "
        # Output  : " <Third Suggestion> "
        if message.content == "meet":
            #Print wip message
            await message.channel.send("Work in progress.")
    
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
                    #delete the message if the message contains no text, no embeds, no other attachments BUT the json file
                    if not message.content and not message.embeds and len(message.attachments) == 1:
                        await message.delete()
        await channel.send("All JSON files have been downloaded.")
        # Merge the JSON files and print a message in the terminal
        merge_files_script.merge_files()

    async def download_file(self, attachment):
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as response:
                if response.status == 200:
                    file_path = os.path.join('downloads', attachment.filename)
                    with open(file_path, 'wb') as f:
                        f.write(await response.read())
                    print(f'Downloaded {attachment.filename}')



    

# Run the bot
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(token)


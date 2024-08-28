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
from datetime import datetime, timedelta

# reminders timing
# total time for sending the json
total_time = 5 # minutes
# reminder coordonates
# Get the time in hours and save it in x
x = datetime.now().hour
y = datetime.now().minute + 1 # minute

# middle reminder
xone = x
yone = y + total_time - 2 # 2 minutes before the end of the total time
# done reminder
xtwo = x
ytwo = y + total_time # at the end of the total time




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
        scheduler.add_job(self.send_weekly_message, CronTrigger(day_of_week='wed', hour=x, minute=y))
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
        scheduler.add_job(self.one_hour_left_message, CronTrigger(day_of_week='wed', hour=xone, minute=yone))
        scheduler.add_job(self.time_elapsed_message, CronTrigger(day_of_week='wed', hour=xtwo, minute=ytwo))
        scheduler.start()

    async def one_hour_left_message(self):
        channel = self.get_channel(1277573107044974592)
        await channel.send("Two minutes left to submit your JSON file!") # change the text back to one hour left

    async def time_elapsed_message(self):
        channel = self.get_channel(1277573107044974592)
        await channel.send("Time is up!")
        await self.read_channel_for_json_files(channel)


    async def read_channel_for_json_files(self, channel):
        end_time = datetime.utcnow() + timedelta(minutes=total_time)
        async for message in channel.history(after=datetime.utcnow(), oldest_first=True):
            if datetime.utcnow() > end_time:
                break
            for attachment in message.attachments:
                if attachment.filename.endswith('.json'):
                    accepted_time = datetime.utcnow() - timedelta(minutes=total_time+1)
                    #await channel.send(f"Accepted time is {accepted_time.time()}")
                    if message.created_at.date() == datetime.utcnow().date():
                        #await channel.send("The message was sent today.")
                        if message.created_at.time() >= accepted_time.time():
                            #await channel.send("The message was sent at the right time.")
                            await self.download_file(attachment)
                            await channel.send(f"Downloaded {attachment.filename}")
                            #delete the message with the json file
                            await message.delete()
                        else:
                            await channel.send("The message was not sent at the right time.")
                            await channel.send(f"NOT Downloaded {attachment.filename}")
                    else:
                        await channel.send("The message was not sent today.")
                        await channel.send(f"NOT Downloaded {attachment.filename}")


        channel = self.get_channel(1277573107044974592)
        await channel.send("All JSON files have been downloaded.")

    async def download_file(self, attachment):
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as response:
                if response.status == 200:
                    file_path = os.path.join('downloads', attachment.filename)
                    with open(file_path, 'wb') as f:
                        f.write(await response.read())
                    print(f'Downloaded {attachment.filename}')


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(token)


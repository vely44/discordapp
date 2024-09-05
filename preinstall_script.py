#Script for preinstalling the required libraries for the project
#Author: Daniel V.
#Date: 31-08-2024
#Version: 1.0
#Info: This script will install the required libraries on the raspberry pi
#Info: This script will run only once, before the first use of the discord bot
#Info: This follwing libraries are used in the program:
#import discord
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from apscheduler.triggers.cron import CronTrigger
#import asyncio
#import aiohttp
#import os
#from datetime import datetime, timedelta, timezone
#Libraries that will be installed:
#- discord  # discord.py
#- apscheduler  # APScheduler
#- aiohttp  # aiohttp
# The script will install the libraries using the pip command and then check if the installation was successful and print a message for each library and if the installation was successful or not
# The script will also check if the libraries are already installed and if they are it will print a message that the library is already installed
# The script will also print a message if the installation was successful or not
# The script will also save the output  of the raspberry pi terminal in a file called "preinstall_log.txt"
# End of the information
# """
#

#imports
import os

#main function
def main():
    #list of libraries that need to be installed
    libraries = ["discord", "apscheduler", "aiohttp"]
    #loop through the libraries
    for lib in libraries:
        #install the library
        os.system(f"pip install {lib}")
        #get the answer from the terminal in the log file
        os.system(f"pip show {lib} > preinstall_log.txt")
        #check if the library is installed and log the result from the terminal
        if os.system(f"pip show {lib}") == 0:
            print(f"{lib} was installed successfully")
            os.system(f"pip show {lib} >> preinstall_log.txt")
        else:
            print(f"{lib} was not installed successfully")
            os.system(f"pip show {lib} >> preinstall_log.txt")
    #save the output of the terminal in a file
    os.system("pip list > preinstall_log.txt")


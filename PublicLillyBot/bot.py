import discord
from discord.ext import commands
import botCommands
import MemberPointTracker
import asyncio
import datetime
import json

#Global Variables for the bot
TOKEN = "CONFIDENTIAL"
prefix = "!"
bot = commands.Bot(command_prefix=prefix)

#class which keeps track of member points
MemberPointTracker = MemberPointTracker.MemberPointTracker()

#### The following test values are set in the on_ready function ###
#The admin channel ID
admin_channel = 0
##the person who will receive a message when someone achieves lotus
reporter_id = 0
#The server's ID
server_id = 0


@bot.event  
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('Bot ID: ' + str(bot.user.id))
    print('------------------')
    
    #Set the settings for the bot from the settings.JSON file
    #get the global variables
    global admin_channel, reporter_id, server_id
    #Open the file and get the data
    jsonFile = open('JSONFiles/settings.JSON', "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    
    admin_channel = data["admin_channel"]
    reporter_id = data["reporter_id"]
    server_id = data["server_id"]
    

""" This event is triggered when the bot starts up """
@bot.event
async def on_message(message): 
    global MemberPointTracker
    global reporter_id

    #check it's not the bot's own ID
    if (message.author.id != 000000000000000):
        #update their daily point. Check if they hit lotus
        lotus = MemberPointTracker.updateMemberPoint(message.author.id)
        if(lotus):
            await bot.get_user(reporter_id).send(str(message.author) + " has achieved LOTUS!")
    
    #If someone says they love LillyBot, they get a message
    if(("love you lilly" in message.content.lower()) or ("love lilly" in message.content.lower())):
        await message.channel.send("I love you too " + "<@!" + str(message.author.id) + "> !")
        
    # coroutine that triggers commands
    await bot.process_commands(message)
    
    
""" Give a member a daily point if they join a voice channel """
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        #update their daily point. Check if they hit lotus
        lotus = MemberPointTracker.updateMemberPoint(member.id)
        if(lotus):
            await bot.get_user(reporter_id).send(str(member) + " has achieved LOTUS!")

    
""" List of Lillybot commands """
@bot.command()
async def bot_commands(ctx):   
    commands = """
LillyBot Command List (!)
--------------------------------
mod_commands    --- List of Moderator Commands (mods only)
admin_commands  --- List of Administrator Commands (admins only)
    """
    await ctx.send(commands)


""" List of Moderator LillyBot commands """
@bot.command(pass_context=True)
@commands.has_any_role('Moderators')
async def mod_commands(ctx):
    global admin_channel
    commands = """
LillyBot Moderator Command List (!)
-------------------------------------
mod_commands     --- The list of commands available to mods.
report           --- Generates a report of the total member points.
daily_report     --- A list of users who have gotten their points today.
manual_reset     --- Manually resets the daily points earned today. Does not reset the time.
clear (number)   --- Clears the specified number of messages. Must be between 5 and 100 inclusive.
    """
    await bot.get_channel(admin_channel).send(commands)
    
    
""" List of Administrator LillyBot commands """
@bot.command(pass_context=True)
@commands.has_any_role('Moderators')
async def admin_commands(ctx):
    global admin_channel
    commands = """
LillyBot Administrator Command List (!)
-----------------------------------------
            Moderator 
mod_commands     --- The list of commands available to mods.
report           --- Generates a report of the total member points.
daily_report     --- A list of users who have gotten their points today.
manual_reset     --- manually resets the daily points earned today. Does not reset the time.
clear (number)   --- Clears the specified number of messages. Must be between 5 and 100 inclusive.

            Admin Specific
change_reporter(@member)            --- Changes the reporter to the member.
change_admin_channel (channel name) --- Changes the admin channel.
    """
    await bot.get_channel(admin_channel).send(commands)
    
    
    
"""  -----       Moderator Only Commands      -----       """

""" A list of users who have gotten their daily point for today """
@bot.command(pass_context=True)
@commands.has_any_role('Moderators')
async def daily_report(ctx):
    global MemberPointTracker
    global admin_chanel
    #Get the report as a string
    report = MemberPointTracker.getDailyMemberPointsNames(ctx.message.guild.members)
    await bot.get_channel(admin_channel).send(report)
            
    
""" Manually resets today's daily points """
@bot.command(pass_context=True)
@commands.has_any_role('Moderators')
async def manual_reset(ctx):
    MemberPointTracker.manualReset()
    await bot.get_channel(admin_channel).send("The daily points have been reset by: " + ctx.message.author.mention)
    print(ctx.author.name + " has reset the daily points.")
    
    
""" Generates a report of the member points in the server """
@bot.command(pass_context=True)
@commands.has_any_role('Moderators')
async def report(ctx):
    global MemberPointTracker
    global admin_channel
    #Get the report as a string
    report = MemberPointTracker.generateReport(ctx.message.guild.members)
    await bot.get_channel(admin_channel).send(report)
    
""" Deletes a given number of messages. The message deletion number must be between 5 and 100."""
@bot.command(pass_context = True)
@commands.has_any_role('Moderators')
async def clear(ctx, number):
    number = int(number) #Converting the amount of messages to delete to an integer
    if(number < 5 or number > 100):
        await ctx.send("Please provide a value in the range:  5 <= number <= 100")
    else:
        await ctx.channel.purge(limit=number)
        print(ctx.author.name + " has deleted " + str(number) + " messages from the channel:  \"" + ctx.channel.name + "\"")
    
    

"""  -----       Administrator Only Commands      -----       """

""" Changes the reporter: Person who will receive notifications that someone reached Lotus """
@bot.command(pass_context=True)
@commands.has_any_role('Admins')
async def change_reporter(ctx, member: discord.Member):
    #check that the user is a valid member
    validArgument = botCommands.checkValidMember(member.id, ctx.message.guild.members)
    if not(validArgument):
        await ctx.send("The user you provided does not exist in the server.")
        
    #If it's valid, change the reporter_id and the settings JSON
    global reporter_id
    reporter_id = member.id
    botCommands.changeReporterID(member.id)
    await bot.get_channel(admin_channel).send("The reporter was successfully changed. The new reporter is " + member.mention)
    
    
""" Changes the ID of the admin channel """
@bot.command(pass_context=True)
@commands.has_any_role('Admins')
async def change_admin_channel(ctx, arg):
    global admin_channel
    #strip the string of spaces
    arg = arg.strip()
    channel_id = -1
    
    #iterate through the channels and see if the channel name exists
    guild = bot.get_guild(server_id)
    for channel in guild.channels:
        if(channel.name == arg):
            channel_id = channel.id
    
    #If the channel doesn't exist
    if(channel_id == -1):
        await ctx.send("The channel \"" + arg + "\" does not exist.")
    #If the channel exists
    else:
        botCommands.changeAdminChannelID(channel_id)
        admin_channel = channel_id
        await bot.get_channel(admin_channel).send("The admin channel has been successfully changed to: " + arg)


"""  -----      Other      -----       """
    
""" Error Handling, just print the error and pass """
@bot.event
async def on_command_error(ctx, error):
    print("Error: " + str(error))
     
    
""" Coroutine task that will run each hour. Resets all user points at midnight. """
async def reset_daily():
    await bot.wait_until_ready()
    global MemberPointTracker
    global server_id
    while not bot.is_closed():
        try:
            #Update the JSON File 
            MemberPointTracker.updateJSONMemberPoints()
            guild = bot.get_guild(server_id) #get the members in the server
            MemberPointTracker.updateJSONActiveMembers(guild.members) #update the json by deleting inactive members
            MemberPointTracker.updateLotusLevelTotalPoints() 
            
            #check if it's time to reset the daily points
            MemberPointTracker.checkResetHour()
            print("   ---    Daily reset achieved: " + str(datetime.datetime.now()))
            # 3,600 seconds = 1 hour
            await asyncio.sleep(3600)
        except Exception as e: 
            print(e)
            await asyncio.sleep(3600) 


#run the reset coroutine
bot.loop.create_task(reset_daily())

#Run the client
bot.run(TOKEN)

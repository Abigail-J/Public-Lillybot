import discord
from discord.ext import commands
import json
import random


"""
 Helper functions to lower the clutter in bot.py
""" 

""" Checks if the id is a valid user ID. Returns True or False."""
def checkValidMember(id, member_list):
    #Check if the ID is in the user list provided by the discord server
    for member in member_list:
        if(member.id == id):
            return True
    return False


""" Changes the reporter ID in the settings.JSON """
def changeReporterID(id):
    #Open the file and get the data
    jsonFile = open('JSONFiles/settings.JSON', "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    
    #change the member_points to our member_total_points
    data["reporter_id"] = id
        
    #Save the changes to the JSON File
    json_object = json.dumps(data, indent = 4) 
    with open('JSONFiles/settings.JSON', "w") as outfile: 
        outfile.write(json_object) 
        

""" Changes the ID of the admin channel """
def changeAdminChannelID(id):
    #Open the file and get the data
    jsonFile = open('JSONFiles/settings.JSON', "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    
    #change the member_points to our member_total_points
    data["admin_channel"] = id
        
    #Save the changes to the JSON File
    json_object = json.dumps(data, indent = 4) 
    with open('JSONFiles/settings.JSON', "w") as outfile: 
        outfile.write(json_object) 
    


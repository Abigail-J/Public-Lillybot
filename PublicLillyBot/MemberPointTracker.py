import discord
from discord.ext import commands

import json
import datetime

"""  Keeps track of member daily points  """
class MemberPointTracker: 
    def __init__(self):
        #The number of points required to reach lotus. Determined from the JSON file. 
        self.lotus_level = 0
        #Each member and their total points. This is what is on the JSON file with each member's total points
        self.member_total_points = []  
        #Update the lotus_level and member_total_points from the JSON
        self.updateLotusLevelTotalPoints()
        
        #Each member who received a daily point today. List of str IDs
        self.members_daily_points = []
        #The reset hour will determine the current hour. Resets the members_updated at MIDNIGHT. 
        self.reset_hour = 0
        #The date on which the hour was last reset
        self.reset_date = datetime.datetime.now()
        
        
    """ Checks if the hour has to be reset. If the hour has to be reset, 
    the members_daily_points will be reset """
    def checkResetHour(self):
        current_hour = datetime.datetime.now().hour
        current_date = datetime.datetime.now()
        if(current_date > self.reset_date and current_hour == self.reset_hour and self.members_daily_points != []):
            #Update reset date
            self.reset_date = current_date  
            #reset daily points
            self.members_daily_points = []
        
        
    """ Cleanses the members whom are no longer in the discord server from the JSON file. Takes a list of member IDs from the discord """
    def updateJSONActiveMembers(self, server_members):
        #Open the file and get the data
        jsonFile = open('JSONFiles/memberPoints.JSON', "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file
        
        #get just the IDs from the members list. We are going to be comparing ids. 
        #Note that server_members_ids is a collection of member objects from all members in the server.
        # We just need the IDS of each member.
        server_members_ids = []
        for member in server_members:
            server_members_ids.append(str(member.id))

        #check if each member in the member points in the JSON is still a member
        for member in list(data["member_points"]):
            if(member not in server_members_ids):
                del data["member_points"][member]
                print("Member deleted: " + member)
        
        #Save the changes to the JSON File
        json_object = json.dumps(data, indent = 4) 
        with open('JSONFiles/memberPoints.JSON', "w") as outfile: 
            outfile.write(json_object) 
            
        
    """ Updates the JSON File and the member points based on the member_total_points""" 
    def updateJSONMemberPoints(self):
        #Open the file and get the data
        jsonFile = open('JSONFiles/memberPoints.JSON', "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file
        
        #change the member_points to our member_total_points
        data["member_points"] = self.member_total_points
        
        #change the lotus points if it was changed
        data["lotus_level"] = self.lotus_level
            
        #Save the changes to the JSON File
        json_object = json.dumps(data, indent = 4) 
        with open('JSONFiles/memberPoints.JSON', "w") as outfile: 
            outfile.write(json_object) 
    
    
    """ Opens the JSON file. Read only. Determines the member_total_points and the lotus_level """
    def updateLotusLevelTotalPoints(self):
        #Open the file and get the data
        jsonFile = open('JSONFiles/memberPoints.JSON', "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file
        
        self.member_total_points = data["member_points"]
        self.lotus_level = data["lotus_level"]
        
        
    """ Update's a member's total point to the dictionary. 
        Returns true/false whether they reached lotus. """
    def updateMemberPoint(self, member_id):
        #turn the key to a string
        member_id = str(member_id)
        
        #check if the member has received a daily point today
        if(member_id in self.members_daily_points):
            return False
        
        #Update their total points. Check that if are in the dict keys.
        if(member_id not in self.member_total_points):
            self.member_total_points[member_id] = 1
        else:
            self.member_total_points[member_id] += 1
            
        #Add them to the member_daily_points list since they got their point
        self.members_daily_points.append(member_id)
        
        #Check if they reached lotus level
        return (self.member_total_points[member_id] == self.lotus_level)
    
    
    """ Generates a string that is a report of all the current member points. """
    def generateReport(self, members_list):
        #today's date
        d = datetime.datetime.now()
        
        #the report string
        report_string = """    USER POINTS REPORT - {}   
---------------------------------------------\n""".format(d.date())
    
        #a dictionary that maps the user ids to the user names. 
        #Key = id number (string), value = username string utf-8
        user_id_dict = {}
    
        #populate dict
        for member in members_list:
            #get rid of encoding marks that happen in a string as: b' ... '
            member_name = str(str(member.name).encode('utf8'))[2:-1]
            user_id_dict[str(member.id)] = member_name

        #iterate through the data members, populate report string
        for member_id, points in self.member_total_points.items():
            #check if the user is a member of the server
            if(member_id in user_id_dict):
                user_rep = "{:20s} ------  {:6d}\n".format(user_id_dict[member_id], points)
                report_string += user_rep
        
        return report_string
    
    
    """ Manualy resets the members' daily points """
    def manualReset(self):
        self.members_daily_points = []
        
        
    """ Returns a string that is the name of all the users that have received a daily point today"""
    def getDailyMemberPointsNames(self, members_list): 
        #today's date
        d = datetime.datetime.now()
        
        #the report string
        report_string = """    User Daily Points - {}   
---------------------------------------------\n""".format(d.date())
    
        #a dictionary that maps the user ids to the user names.
        # Key = id number (string), value = username string utf-8
        user_id_dict = {}
    
        #populate dict
        for member in members_list:
            #get rid of encoding marks that happen in a string as: b' ... '
            member_name = str(str(member.name).encode('utf8'))[2:-1]
            user_id_dict[str(member.id)] = member_name

        #iterate through the data members, populate report string
        for member_id in  self.members_daily_points:
            #check that they're still a member of the server
            if(member_id in user_id_dict):
                report_string += user_id_dict[member_id]
                report_string += "\n"
        
        return report_string
    
    """ Number of users in the members daily points """
    def getMemberPointsList(self):
        return str(len(self.members_daily_points))
    
    
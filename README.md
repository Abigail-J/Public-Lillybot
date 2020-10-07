# Public LillyBot
**bot.py** in the PublicLillyBot folder runs the bot. It is where bot commands are declared. This is the main code.

**MemberPointTracker.py** is the class that helps keep track of member points. It accesses memberPoints.JSON in the JSON folder.

**botCommands.py** is the class that accesses/modifies settings.JSON in the JSON folder. This file keeps track of token/ID settings

# Summary
LillyBot's purpose is to measure user activity on a Discord server through an automated point system. Users are able to obtain a single daily point every 24 hours on the discord server. Messaging in a channel or joining voice communications can obtain the user a daily point. When users reach a certain threshold of activity through the point system, an administrator is notified. This is the public version of LillyBot that hides specific information.

# Commands
There are two types of commands: Moderator and Administrator. Administrators are able to access Moderator commands. 
The prefix for LillyBot commands is:  **!**

### Moderator Commands
|Command Name      | Summary     |
|------------------|-------------|
|mod_commands      |The list of commands available to moderators|
|report            |Generates a report of all the members in the server and their total associated points.|
|daily_report      |A list of names of all the users who have earned a daily point today.|
|manual_reset      |Resets the daily points earned today. Users will still be able to obtain a daily point after the reset because it does not reset the time, only the points.|
|clear(number)     |Clears the number of messages provided from the channel. The argument must be in the range: ( 5 <=  number <= 100)|

### Administrator Commands
|Command Name             | Summary     |
|-------------------------|-------------|
|change_reporter (@member)|Changes the ID of the reporter. The reporter is the person who receives notifications that someone has achieved lotus status.|
|change_admin_channel (channel name)|Changes the ID of the admin channel. The name of the channel is the argument. The results of admin and mod commands will now be sent to this channel.|
 
# Daily Points, Lotus, JSON
  Lotus is a status given to users who have been active on the server for a given time. Lillybot determines who has reached Lotus status through the use of daily points. The Lotus Level is the number of daily points required to reach the Lotus status. Lotus Level is currently 80 daily points or above. When a user in the server reaches the Lotus Level, an administrator called the "reporter" is given a private message notification. 
  
  User points and the lotus number are stored in the JSON file: memberPoints.JSON. The reporter ID and admin channel ID are stored in a separate JSON file: settings.JSON. LillyBot updates changes to memberPoints.JSON hourly. Setting updates done by Administrators instantly update to settings.JSON




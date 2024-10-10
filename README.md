# Discord Application Bot
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) ![Discord.py Version](https://img.shields.io/badge/discord.py-2.0%2B-orange)

## Statuses
To edit the status, edit line 49 in main.py `await bot.change_presence(activity=discord.Game(name="Your Status Here"), status=discord.Status.dnd)` change `status=discord.Status.dnd` with:<br>
`status=discord.Status.idle` for idle<br>
`status=discord.Status.offline` for offline<br>
`status=discord.Status.online` for online<br>
`status=discord.Status.dnd` for dnd.<br>
To use rotating status (change status every x minutes), remove all `#` from line 34-42 it should look something like:<br>

`statuses = cycle([`<br>
`    ("Status 1", discord.ActivityType.playing),`<br>
`    ("Status 2", discord.ActivityType.watching)`<br>
`])`<br>

`@tasks.loop(minutes=3)`<br>
`async def change_status():`<br>
`    status, activity_type = next(statuses)`<br>
`    await bot.change_presence(activity=discord.Activity(type=activity_type, name=status), status=discord.Status.dnd)`<br>
    
and remove line 49

## Commands
**`setup`**<br>

## Configuration
The bot will send the application message to the channel ID specified in `review_channel_id`<br>
To add application roles, add their IDs in `roles = []` (Seperated by a comma (,))<br>
To add questions, add them here:<br>
`application_questions = [`<br>
`    "Question 1",`<br>
`    "Question 2"`<br>
`]`<br>

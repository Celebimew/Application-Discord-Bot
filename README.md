# Discord Application Bot
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) ![Discord.py Version](https://img.shields.io/badge/discord.py-2.0%2B-orange)

## Statuses
To edit the status, edit line 49 in main.py `await bot.change_presence(activity=discord.Game(name="Your Status Here"), status=discord.Status.dnd)` change `status=discord.Status.dnd` with `status=discord.Status.idle` for idle, `status=discord.Status.offline` for offline, `status=discord.Status.online` for online and `status=discord.Status.dnd` for dnd.
To use rotating status (change status every x minutes), remove all `#` from:
`#statuses = cycle([
#    ("Status 1", discord.ActivityType.playing),
#    ("Status 2", discord.ActivityType.watching),
#])

#@tasks.loop(minutes=3)
#async def change_status():
#    status, activity_type = next(statuses)
#    await bot.change_presence(activity=discord.Activity(type=activity_type, name=status), status=discord.Status.dnd)`
and remove line 49

## Commands
**`setup`**

## Configuration
The bot will send the application message to the channel ID specified in `review_channel_id`
To add application roles, add their IDs in `roles = []` (Seperated by a comma (,))
To add questions, add them here:
`application_questions = [
    "Question 1",
    "Question 2"
]`

import os, discord, asyncio
from discord.ext import commands
from discord.ui import Button, View, Select
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.members = True
intents.dm_messages = True
intents.guild_reactions = True
intents.presences = True
intents.auto_moderation = True
intents.auto_moderation_configuration = True

# Change "c!" with your prefix or leave it to use the default prefix
bot = commands.Bot(command_prefix='c!', intents=intents)

# Applications will be sent in this channel
review_channel_id = 123456789123456789
# Roles for members to apply for (ID)
roles = [123456789123456789] 
# Your application questions
application_questions = [
    "Your Questions here"
]

# =================================== Status Switching ===================================
#statuses = cycle([
#    ("Status 1", discord.ActivityType.playing),
#    ("Status 2", discord.ActivityType.watching)
#])

#@tasks.loop(minutes=3)
#async def change_status():
#    status, activity_type = next(statuses)
#    await bot.change_presence(activity=discord.Activity(type=activity_type, name=status), status=discord.Status.dnd)
# ========================================================================================

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Change "Your Status Here" with your status or delete the line below if you want to use status switching
    await bot.change_presence(activity=discord.Game(name="Your Status Here"), status=discord.Status.online)

class RoleSelect(Select):
    def __init__(self, guild):
        options = [
            discord.SelectOption(label=role.name, value=str(role.id))
            for role_id in roles
            if (role := guild.get_role(role_id)) is not None
        ]
        super().__init__(placeholder='Select a staff role', options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You are now applying for: <@&{self.values[0]}>", ephemeral=True)

async def ask_questions(ctx, user):
    responses = []

    for question in application_questions:
        await user.send(question)
        try:
            msg = await bot.wait_for(
                'message',
                timeout=60.0,
                check=lambda m: m.author == user and m.channel == user.dm_channel
            )
            responses.append(msg.content)
        except asyncio.TimeoutError:
            await user.send("You took too long to respond. Please start the application again.")
            return

    application_details = "\n".join(f"{question}: {response}" for question, response in zip(application_questions, responses))

    application_channel = bot.get_channel(review_channel_id)
    if application_channel is None:
        await user.send("Review channel not found. Please contact an administrator.")
        return

    embed = discord.Embed(
        title="New Staff Application",
        description=application_details,
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Submitted by: {user.mention}")

    view = View()
    approve_button = Button(label='Approve', style=discord.ButtonStyle.success)
    deny_button = Button(label='Deny', style=discord.ButtonStyle.danger)

    async def approve_callback(interaction: discord.Interaction):
        role = interaction.guild.get_role(roles[0])
        if role:
            await user.add_roles(role)
            await user.send("Congratulations! Your application has been accepted.")
        else:
            await user.send("The role could not be found. Please contact an administrator.")
        
        await interaction.response.send_message("Application approved!", ephemeral=True)
        for item in view.children:
            item.disabled = True
        await interaction.message.edit(embed=embed, view=view)

    async def deny_callback(interaction: discord.Interaction):
        await user.send("We regret to inform you that your application has been denied.")
        await interaction.response.send_message("Application denied!", ephemeral=True)
        for item in view.children:
            item.disabled = True
        await interaction.message.edit(embed=embed, view=view)

    approve_button.callback = approve_callback
    deny_button.callback = deny_callback

    view.add_item(approve_button)
    view.add_item(deny_button)

    review_channel = bot.get_channel(review_channel_id)
    if review_channel is None:
        await user.send("Review channel not found. Please contact an administrator.")
        return

    await review_channel.send(f"New application from {user.mention}:", embed=embed, view=view)
    await user.send("Your application has been submitted!")

@bot.command()
@commands.has_permissions(administrator=True)
async def sendpanel(ctx):
    try:
        view = View()
        role_select = RoleSelect(ctx.guild)
        view.add_item(role_select)

        apply_button = Button(label='Apply for Staff', style=discord.ButtonStyle.primary)

        async def apply_callback(interaction: discord.Interaction):
            await interaction.response.send_message("Check your DMs for the application questions.", ephemeral=True)
            await ask_questions(ctx, interaction.user)

        apply_button.callback = apply_callback
        view.add_item(apply_button)

        embed = discord.Embed(
            title="Staff Application",
            description="Click below to apply for a staff role",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed, view=view)

    except Exception as e:
        print(f"Error in setup command: {e}")
        await ctx.send(f"Something went wrong while setting up the application system: {e}. Please try again later.")

bot.run(TOKEN)

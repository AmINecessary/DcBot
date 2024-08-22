import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

user_tasks = {}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Calculating Carbon Footprints"))
    print(f'Logged in as {bot.user.name} and set status to "Calculating Carbon Footprint"')
    channel = bot.get_channel(1166806610111369308)
    if channel:
        await channel.send("Hi! I am Carbon Footprint Calculator Bot. I calculate your carbon footprint with a series of questions. Here are some of the commands you can use:")
        await channel.send('"!introduce" for the bot to introduce itself.')
        await channel.send('"!info" to get some information about the calculation results and the world average data.')
        await channel.send('"!carbonfootprint" to calculate your carbon footprint')

@bot.command()
async def introduce(ctx):
    await ctx.send("Hi! I am Carbon Footprint Calculator Bot. I calculate your carbon footprint with a series of questions. Here are some of the commands you can use:")
    await ctx.send('"!introduce" for the bot to introduce itself.')
    await ctx.send('"!info" to get some information about the calculation results and the world average data.')
    await ctx.send('"!carbonfootprint" to calculate you carbon footprint')

@bot.command()
async def info(ctx):
    await ctx.send("Carbon footprint data is an estimate and may not reflect the real data.")
    await ctx.send("The calculation is just a simple way to calculate. May not reflect reality.")
    await ctx.send("If the bot stutters, re-write your answer.")

@bot.command()
async def carbonfootprint(ctx):
    user_id = ctx.author.id

    if user_id in user_tasks:
        user_tasks[user_id].cancel()
        await ctx.send("Your previous calculation has been canceled. Starting a new one.")
    
    task = bot.loop.create_task(run_carbonfootprint(ctx))
    user_tasks[user_id] = task

async def run_carbonfootprint(ctx):
    try:
        await ctx.send("Let's calculate your carbon footprint.")
        transport_choice = ""
        flight_choice = ""
        energy_choice1 = ""
        energy_choice2 = ""
        diet_choice = ""
        shopping_choice = ""

        first_try = True
        while transport_choice not in ["1", "2", "3", "4"]:
            if first_try:
                await ctx.send("How do you transport?")
                await ctx.send("4) Car (Solo)")
                await ctx.send("3) Carpool / Electric Car (Solo)")
                await ctx.send("2) Public Transport / Electric Carpool / Electric Scooter/Bike etc.")
                await ctx.send("1) Walking / Biking")
                first_try = False
            else:
                await ctx.send('Please answer with "1", "2", "3", or "4".')
            
            transport_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
            transport_choice = transport_msg.content
        
        first_try = True
        while flight_choice not in ["1", "2", "3", "4"]:
            if first_try:
                await ctx.send("How many times do you fly every year?")
                await ctx.send("4) Regularly (6+ times)")
                await ctx.send("3) Frequently (3+ times)")
                await ctx.send("2) Not often (1-2 times)")
                await ctx.send("1) Never / Rarely (Averaging below one)")
                first_try = False
            else:
                await ctx.send('Please answer with "1", "2", "3", or "4".')
            
            flight_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
            flight_choice = flight_msg.content

        first_try = True
        while energy_choice1 not in ["1", "2", "3", "4"]:
            if first_try:
                await ctx.send("How do you heat your home?")
                await ctx.send("4) Gas")
                await ctx.send("3) Wood / Pellet Stove")
                await ctx.send("2) Electric")
                await ctx.send("1) No heating")
                first_try = False
            else:
                await ctx.send('Please answer with "1", "2", "3", or "4".')
            
            energy_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
            energy_choice1 = energy_msg.content

        first_try = True
        while energy_choice2 not in ["1", "2", "3", "4"]:
            if first_try:
                await ctx.send("How energy efficient is your home?")
                await ctx.send("4) Not efficient")
                await ctx.send("3) Somewhat efficient")
                await ctx.send("2) Efficient")
                await ctx.send("1) Very efficient")
                first_try = False
            else:
                await ctx.send('Please answer with "1", "2", "3", or "4".')
            
            energy_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
            energy_choice2 = energy_msg.content

        first_try = True
        while diet_choice not in ["1", "2", "3", "4"]:
            if first_try:
                await ctx.send("How often do you eat meat?")
                await ctx.send("4) More than once every day")
                await ctx.send("3) Once a day")
                await ctx.send("2) Few times a week")
                await ctx.send("1) Never")
                first_try = False
            else:
                await ctx.send('Please answer with "1", "2", "3", or "4".')
            
            diet_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
            diet_choice = diet_msg.content

        first_try = True
        while shopping_choice not in ["1", "2", "3", "4"]:
            if first_try:
                await ctx.send("How often do you shop for clothes?")
                await ctx.send("4) Weekly or more")
                await ctx.send("3) Monthly")
                await ctx.send("2) 2-3 times a year")
                await ctx.send("1) Yearly or less")
                first_try = False
            else:
                await ctx.send('Please answer with "1", "2", "3", or "4".')
            
            shopping_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
            shopping_choice = shopping_msg.content

        transport_choice = int(transport_choice)
        flight_choice = int(flight_choice)
        energy_choice1 = int(energy_choice1)
        energy_choice2 = int(energy_choice2)
        diet_choice = int(diet_choice)
        shopping_choice = int(shopping_choice)

        
        cftotal = (transport_choice + flight_choice + energy_choice1 + energy_choice2 + diet_choice + shopping_choice)
        cfavg = cftotal / 6
        cftotal = str(cftotal)
        cfavg = str(cfavg)
        
        await ctx.send("Keep in mind that More Score = More Carbon Footprint. Less carbon footprint equals to less negative impact on nature.")
        await ctx.send("Your average score: " + cfavg)
        await ctx.send("World average score: 2.3")
        await ctx.send("Your total score: " + cftotal)
        await ctx.send("World average total score: 13.8")
        if int(cftotal) > 13.8:
            await ctx.send("Your carbon footprint is above average. But you could:")
            if int(transport_choice) == 4:
                await ctx.send("If possible, try carpooling, walking, biking or using public transport to your destination.")
            if int(flight_choice) == 3 or int(flight_choice) == 4:
                await ctx.send("Get on less flights.")
            if int(energy_choice1) == 3 or int(energy_choice1) == 4:
                await ctx.send("Try using electric heating.")
            if int(energy_choice2) == 3 or int(energy_choice2) == 4:
                await ctx.send("Insulate walls, switch to LEDs, seal your walls and doors, improve heating and cooling systems for more efficiency etc.")
            if int(diet_choice) == 3 or int(diet_choice) == 4:
                await ctx.send("If not already, eat suggested amount of meat.")
            if int(shopping_choice) == 3 or int(shopping_choice) == 4:
                await ctx.send("Try shhopping for clothes less.")

        else:
            await ctx.send("Your carbon footprint is below average. Hope it will always be that way!")

    except asyncio.CancelledError:
        pass
    finally:
        user_tasks.pop(ctx.author.id, None)

bot.run('TOKEN')

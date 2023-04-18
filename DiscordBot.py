import discord
from discord.ext import commands
import giphy_client
import random
from giphy_client.rest import ApiException

bot = commands.Bot(command_prefix='$')
giphy_token = "token"

api_instance = giphy_client.DefaultApi()


# to generate random number
def rand():
    global r
    r = random.randint(1, 100)
    print(f"Ans: {r}")


rand()


# funtion to search gif's
async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(giphy_token, query, limit=3, rating='g')
        lst = list(response.data)
        gif = random.choices(lst)
        return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


# [BOT COMMANDS]:

# for reacting to user
async def on_message(self, message):
    l = ["hi", "Hi", "Hello", "hello", "Bye", "bye"]
    if message.author != self.user:
        if message.content in l:
            gif = await search_gifs(message)
            await message.channel.send(message + gif)


# to check the guessed number
@bot.command()
async def g(ctx, a):
    userID = ctx.author.mention
    # ID=userID.split("#")
    # print(userID)

    if int(a) == r:
        rand()
        gif = await search_gifs("Clap")
        await ctx.send(userID + " Sugoi!  " + gif)

    else:
        await ctx.send(userID + " Better luck next time!😢")


# to kill bot
@bot.command()
async def kill(ctx):
    await ctx.send("Ahhhhhhh!")
    await ctx.bot.logout()


# print gif according to keyword
@bot.command()
async def gif(ctx, e):
    gif = await search_gifs(e)
    await ctx.send('Gif URL : ' + gif)


bot.run('token')

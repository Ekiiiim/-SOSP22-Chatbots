import os
import random
import requests
import json
import pyjokes
from discord.ext import commands
from urllib.request import urlopen
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix='!')
bot.videos = ['https://www.youtube.com/watch?v=XmoKM4RunZQ', 'https://www.youtube.com/watch?v=qTmjKpl2Jk0', 'https://www.youtube.com/watch?v=hY7m5jjJ9mM']
bot.happylist = []
bot.notelist = []

@bot.event
async def on_ready():
  print(f'{bot.user.name} has connected to Discord!')

# Interacting w/ messages: to be developed
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.content.startswith('!'):
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
  if ctx.invoked_with == "img":
    await ctx.send("Please add description (e.g. !img park)")
  elif ctx.invoked_with == "happy":
    await ctx.send("Please add description (e.g. !happy picnic)")
  elif ctx.invoked_with == "notedown":
    await ctx.send("Please add description (e.g. !notedown Picnic on Sunday)")
  elif ctx.invoked_with == "deletenote":
    await ctx.send("Please choose the number of note (e.g. !deletenote 1)")
  else:
    response = "```"
    for command in bot.commands:
      response += f"{command}\n"
    response += "```"
    await ctx.send(f"Sorry, I don't understand. Please try these commands:\n{response}")

# Running speed to be improved
@bot.command()
async def img(ctx, *, title):
  htmldata = urlopen(f"https://unsplash.com/s/photos/{title.replace(' ', '-')}")
  soup = BeautifulSoup(htmldata, 'html.parser')
  images = soup.find_all('img', limit=3)
  await ctx.send(random.choice(images)['src'])

@bot.command()
async def joke(ctx):
  await ctx.send(pyjokes.get_joke('en', 'all'))

@bot.command()
async def quote(ctx):
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = f"{json_data[0]['q']} — {json_data[0]['a']}"
  await ctx.send(quote)

@bot.command()
async def hello(ctx):
  await ctx.send("hello " + ctx.author.display_name)

@bot.command()
async def cat(ctx):
  await ctx.send(random.choice(bot.videos))

@bot.command()
async def happy(ctx, *, item):
  await ctx.send("Awesome!")
  bot.happylist.append(item)
  print(bot.happylist)

@bot.command()
async def sad(ctx):
  await ctx.send("Hope this makes you feel better!")
  await ctx.send(random.choice(bot.happylist))

@bot.command()
async def calc(ctx, x: float, fn: str, y: float):
  if fn == '+':
    await ctx.send(x + y)
  elif fn == '-':
    await ctx.send(x - y)
  elif fn == '*':
    await ctx.send(x * y)
  elif fn == '/':
    await ctx.send(x / y)
  elif fn == '^':
    await ctx.send(x ** y)
  elif fn == '%':
    await ctx.send(x % y)
  else:
    await ctx.send("We only support 6 operations: + - * / ^ %")

@bot.command()
async def notedown(ctx, *, item):
  bot.notelist.append(item)
  await ctx.send("Got it!")

@bot.command()
async def notes(ctx):
  n = len(bot.notelist)
  await ctx.send(f"You have taken {n} note(s):")
  for i in range(n):
    await ctx.send(f'{i + 1}. {bot.notelist[i]}')

@bot.command()
async def deletenote(ctx, idx: int):
  if len(bot.notelist) == 0:
    await ctx.send("You have no note to be deleted.")
  elif not 1 <= idx <= len(bot.notelist):
    await ctx.send(f"Please choose a number from 1 to {len(bot.notelist)}.")
  else:
    bot.notelist.pop(idx - 1)
    await ctx.send("Deleted!")
    await ctx.send(f"Now you have {len(bot.notelist)} note(s):")
    for i in range(len(bot.notelist)):
      await ctx.send(f'{i + 1}. {bot.notelist[i]}')

password = os.environ['token']
bot.run(password)


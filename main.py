import discord
import sys
import smtplib
import json
from datetime import datetime
from discord.ext import commands
from random_line import RandomLine


TOKEN = "" # Bot Token
PREFIX  = "" # Intended Prefix for the Bot
email = "" # Email Address
pwd = "" # Email Password
sender_name = "" # Email Sender Name
client = commands.Bot(command_prefix=PREFIX)


async def send_mail(ctx, server, target_email, count):
  progress = 0
  command_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Preserve the timestamp of the command
  author = ctx.author # Preserve the original author
  message_id = await progress_update(ctx, author, progress, target_email, count, command_timestamp)
  for i in range(count):
    rand_essay = json.loads(RandomLine().get_random_line('essays.txt'))
    title = ", ".join(rand_essay.keys())
    paragraph = rand_essay[title]
    message = ('From: {0} <{1}>\r\n'.format(sender_name, email) + "To: %s\r\n" % target_email + "Subject: %s\r\n" % title + "\r\n" + paragraph)
    server.sendmail(email, target_email, message)
    progress += 1
    await progress_update(message_id, author, progress, target_email, count, command_timestamp)


# Progress Bar for Progress Update
def get_progress_bar(progress, count):
  progress_bar = "["
  progress_percentage = progress / count
  complete_count = round_school(progress_percentage * 30)
  for i in range(complete_count):
      progress_bar += "#"
  for i in range(30-complete_count):
      progress_bar += "="
  progress_bar += "]"
  return progress_bar, progress_percentage * 100


def round_school(x):
    i, f = divmod(x, 1)
    return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))


@client.event
async def progress_update(ctx, author, progress, target_email, count, command_timestamp):
  embed = discord.Embed(title="Progress Tracker", description="Track your email spam progress", color=0x569ff0)
  embed.set_author(name=author.display_name, icon_url=author.avatar_url)
  progress_bar, progress_percentage = get_progress_bar(progress, count)
  embed.add_field(name="Progress", value="'{}' {:.2f}% Done".format(progress_bar, progress_percentage), inline=False)
  embed.add_field(name="Target", value=target_email, inline=False)
  embed.add_field(name="Count", value=count, inline=True)
  embed.add_field(name="Timestamp", value=command_timestamp)
  embed.set_footer(text="Spam Requested By: {}#{}".format(author.name, author.discriminator))

  # Checks if there was already an embed sent previously by checking the type of ctx object
  if (type(ctx) is discord.ext.commands.context.Context):
    message = await ctx.send(embed=embed)
    return message
  else:
    await ctx.edit(embed=embed)


@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


@client.command(name="spam")
async def spam_mail(ctx, target_mail:str, count:int):
  smtp_server = 'smtp.gmail.com'
  port = 587
  # Initialise SMTP server connection
  server = smtplib.SMTP(smtp_server, port)
  server.ehlo()
  if (smtp_server == "smtp.gmail.com"):
      server.starttls()
  server.login(email, pwd)
  await send_mail(ctx, server, target_mail, count)
  server.quit()
  sys.stdout.flush()

  
@spam_mail.error
async def on_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Missing required argument')
  elif isinstance(error, commands.MissingAnyRole):
    await ctx.send("Missing role permission!")
  elif isinstance(error, commands.CommandOnCooldown):
    await ctx.send("Command on cooldown")

  
client.run(TOKEN)

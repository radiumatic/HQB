import discord
import os
from discord.ext import commands
from live import alive
import asyncio
import requests
players={}
questions={}
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="hqb.")
bot.remove_command("help")
help_embed = discord.Embed(title="راهنمای سوالات جهنمی:",description="""
***تمامی دستورات با ***`.hqb`*** آغاز می شوند***

:fire::question:`help` : نمایش راهنما \n========
:fire::question:`question` : پیشنهاد سوال  \n========
:fire::question:`bug` : گزارش باگ \n========
:fire::question:`ping` : دریافت میزان تاخیر ربات \n========
:fire::question:`start` : آغاز گیم \n========
:fire::question:`pack` : پیشنهاد پک سوال  \n========
:fire::question:`join` : اضافه شدن به بازی \n========
:fire::question:`leave` : ترک بازی \n========
:fire::question:`setup` : ستاپ(تنظیم) بازی(باید قبل شروع بازی این کار را انجام دهید) \n========
:fire::question:`party` : لیست افرادی که بازی می کنند \n========

""", color=0xffffff)
#template: :fire::question:`command` : توضیحات \n========


#insert your admins here
admins=["SMM#9107","Nima Ghasemi#9847"]



@bot.command()
async def bot_is_online(ctx):
  if str(ctx.message.author) in admins:
    channel = bot.get_channel(870624299877277716)
    embed=discord.Embed(title=f"ربات روشن شد!", description="هم اکنون میتوانید از ربات استفاده کنید", color=0x00ff00)
    await channel.send(embed=embed)
    embed=discord.Embed(title="انجام شد", description="همگان دانند وضعیت مرا :)", color=0x00ff00)
    await ctx.reply(embed=embed)
  else:
    embed=discord.Embed(title="خطا", description="شما ادمین نیستید :)", color=0xFF0000)
    await ctx.reply(embed=embed)
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="hqb.help"))
    print(f"Logged in as {bot.user.name}({bot.user.id}")



@bot.command(name="help",help="نمایش راهنما",aliases=["h","راهنما"])
async def help(ctx):
    await ctx.reply(embed=help_embed)


@bot.command(help='پینگ ربات')
async def ping(ctx):
    await ctx.reply(f"پونگ! `{str(round(bot.latency * 1000))}` میلی ثانیه")



@bot.command(name="bug", help="گزارش باگ به ادمین ها")
async def bug(ctx, *, message):
    channel = bot.get_channel(870551794273644565)
    embed=discord.Embed(title=f"باگ جدید از {ctx.message.author.name}", description=message, color=0x00ff00)
    await channel.send(embed=embed)
    await ctx.reply("باگ گزارش شد")

@bot.command(help="پیشنهاد سوال")
async def question(ctx, *, question):
    channel = bot.get_channel(870559120476999690)
    embed = discord.Embed(title=f"سوال جدید از {ctx.message.author.name}", description=question, color=0x00ff00)
    await channel.send(embed=embed)
    await ctx.reply("سوال پیشنهادی شما برای بررسی ارسال شد")

@bot.command(name="pack",help='پیشنهاد پک سوال')
async def pack(ctx):
    def check(msg):
        return msg.channel == ctx.channel and msg.author == ctx.author
        

    packmsg = await ctx.send("سوالات:")
    for i in range(5):
      try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        await packmsg.edit(content=packmsg.content+f"\n{msg.content}")
        await msg.delete()
      except asyncio.TimeoutError:
          embed=discord.Embed(title="خطا", description="داااااداش جواب بده تو می خواستی پک پیشنهاد بدی :(", color=0xFF0000)
          await ctx.send(embed=embed)
          return 0
    channel=bot.get_channel(870559120476999690)    
    embed = discord.Embed(title=f"پک سوال جدید از {ctx.message.author.name}", description=packmsg.content, color=0x00ff00)
    await channel.send(embed=embed)
    await ctx.reply("پک سوال پیشنهادی شما ارسال شد")


@bot.command()
async def join(ctx):
  #define server party if there not is
  if not ctx.guild.id in players :
    players[ctx.guild.id]=[]
  #check if player in party
  if ctx.message.author.mention in players[ctx.guild.id]:
    embed=discord.Embed(title="خطا", description="الان تو بازی هستی :neutral_face: میخوای دوباره جوین بدی؟", color=0xFF0000)
    embed.set_image(url="https://pbs.twimg.com/media/EEzQfuTXkAALUWZ.jpg")
    await ctx.send(embed=embed)
    return
  #add player to party
  players[ctx.guild.id].append(ctx.message.author.mention) 
  #send successful
  embed=discord.Embed(title="خوش اومدی", description="با امید عدم به هم خوردن رفاقت شما :upside_down_face:", color=0x00ff00)
  embed.set_image(url="https://i.ytimg.com/vi/pNNN31IB1wE/maxresdefault.jpg")
  await ctx.send(embed=embed)

@bot.command()
async def leave(ctx):
  try:
    players[ctx.guild.id].remove(ctx.message.author.mention)
    embed=discord.Embed(title="خداحافظ", description="بر میگردی دیگه نه؟ به قیافه مظلوم من نگاه کن بگو دلت میاد برنگردی؟ :pleading_face:", color=0x00ff00) 
    embed.set_image(url="https://excitedcats.com/wp-content/uploads/2021/01/cat-cute.png")
    await ctx.send(embed=embed)
  except:
    embed=discord.Embed(title="خطا!", description="تو توی بازی نیستی چجوری می خوای لیو بدی؟ :neutral_face:", color=0xFF0000)
    embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyGjuwn4loVQsviIQw8tmRe8KrgflJxqKtsDmdGqEdSxIQQDh98F_I3C21BTAxSs7STFM&usqp=CAU")
    await ctx.send(embed=embed)
@bot.command()
async def party(ctx):
  if not ctx.guild.id in players:
    players[ctx.guild.id]=[]
    embed=discord.Embed(title="هیچکس نیست", description="مانده ایم تنهای تنها:", color=0xFF0000)
    embed.set_image(url="https://memegenerator.net/img/instances/72390221/were-all-alone-theres-no-one-here.jpg")
    await ctx.send(embed=embed)
    return
  if not players[ctx.guild.id]:
    embed=discord.Embed(title="هیچکس نیست", description="مانده ایم تنهای تنها:", color=0xFF0000)
    embed.set_image(url="https://memegenerator.net/img/instances/72390221/were-all-alone-theres-no-one-here.jpg")
    await ctx.send(embed=embed)
    return
  else:
    message=""
    for p in players[ctx.guild.id]:
      message = message + f"{p}\n"
    embed=discord.Embed(title="افراد حاضر", description=f"این عزیزان الان تو گیمن :smiley:\n{message}", color=0x00ff00)
    embed.set_image(url="https://www.memecreator.org/static/images/memes/5054822.jpg")
    await ctx.send(embed=embed)

@bot.command()
async def setup(ctx):
  if not ctx.guild.id in questions:
    questions[ctx.guild.id]=[]
  if not ctx.guild.id in players or not ctx.message.author.mention in players[ctx.guild.id]:
    embed=discord.Embed(title="خطا!", description="تو توی بازی نیستی چجوری می خوای ستاپ کنی؟ :neutral_face:", color=0xFF0000)
    embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyGjuwn4loVQsviIQw8tmRe8KrgflJxqKtsDmdGqEdSxIQQDh98F_I3C21BTAxSs7STFM&usqp=CAU")
    await ctx.send(embed=embed)
    return
  try:
    questions[ctx.guild.id][5]
    embed=discord.Embed(title="خطا", description=":neutral_face: بازی قبلا ستاپ شده", color=0xFF0000)
    embed.set_image(url="https://i.redd.it/ovmgcxcmu5u61.jpg")
    await ctx.send(embed=embed)
    return
  except:
    pass
  question_pack=requests.post(url="https://nimgp.pythonanywhere.com/api/v1/get_pack_by_server/",data={"server":ctx.guild.id})
  if question_pack.status_code == 404:
    requests.post(url="https://nimgp.pythonanywhere.com/api/v1/register_server/",data={"server":ctx.guild.id,"server_name":ctx.guild.name})
    question_pack=requests.post(url="https://nimgp.pythonanywhere.com/api/v1/get_pack_by_server/",data={"server":ctx.guild.id})
  elif question_pack.status_code == 456:
    embed=discord.Embed(title="خطا", description="عزیزان آروممممم آروم :sweat_smile:\nفعلا پکی واسه شما نداریم وایسید پک جدید بیاد :relaxed:", color=0xFF0000)
    embed.set_image(url="https://devforum.roblox.com/uploads/default/original/4X/d/8/8/d88050147f95355b41b1b842b36d7559606385db.png")
    await ctx.send(embed=embed)
    return 0
  questions[ctx.guild.id].append(question_pack.json()["Pack"])
  for question in question_pack.json()["Questions"]:
    questions[ctx.guild.id].append(question)
  embed=discord.Embed(title="ستاپ تموم وشد :smiley:", color=0x00ff00)
  embed.set_image(url="https://i.stack.imgur.com/nDAux.png")
  await ctx.send(embed=embed)

  

@bot.command()
async def start(ctx):
  def check(msg):
        return msg.channel == ctx.channel and msg.author == ctx.author
  def check_answer(msg):
    return msg.channel == ctx.channel and msg.author.mention == p.replace("!","")

  if not ctx.guild.id in questions or not questions[ctx.guild.id]:
    embed=discord.Embed(title="خطا!", description="ستاپ کنید اول :sweat_smile:", color=0xFF0000)
    embed.set_image(url="https://c.tenor.com/4RtWwdT6hnQAAAAC/homer-simpson-poker-face.gif")
    await ctx.send(embed=embed)
    return
  try:
    questions[ctx.guild.id][6]
    embed=discord.Embed(title="خطا", description="بازی در حال انجامه نمی تونی الان استارت کنی وایسا دست بعد :smile:", color=0xFF0000)
    embed.set_image(url="https://i.pinimg.com/originals/9b/48/f3/9b48f3aaf5e6c52e2a10d4f7ae3d38f6.gif")
    await ctx.send(embed=embed)
    return
  except:
    pass
  questions[ctx.guild.id].append("game started")
  embed=discord.Embed(title="بنگرید ای فرزندان آراگورن! بازی از اینجا شروع می شود...", description=f'نام پک:\n{questions[ctx.guild.id][0]}', color=0x00ff00)
  embed.set_image(url="https://thumbs.dreamstime.com/b/game-starting-screen-saying-get-ready-game-starting-screen-saying-get-ready-motion-dynamic-animated-background-techno-style-169494139.jpg")
  await ctx.send(embed=embed)
  await asyncio.sleep(5)
  question_number=1


  for q in questions:
    if question_number == 6:
      break
      
    for i in range(5):
      embed=discord.Embed(title=f"سوال {question_number}:", description=questions[ctx.guild.id][question_number], color=0x00ff00)
      await ctx.send(embed=embed)
      question_number+=1
      for p in players[ctx.guild.id]:
        question_msg = await ctx.send(f"{p} پاسخگو باش :hugging:")
        try:
          msg = await bot.wait_for("message", check=check_answer, timeout=60)
          embed = discord.Embed(title=f"پاسخ!", description=f"جواب {p} :relaxed::\n{msg.content}", color=0x00ff00)
          await msg.delete()
          await ctx.send(embed=embed)
          await question_msg.delete()
        except asyncio.TimeoutError:
          embed=discord.Embed(title="معرفت گوهر گرانی است به هرکس ندهند...", description="یک عدد بیشعور جواب نداد بریم بعدی :neutral_face:", color=0xFF0000)
          await ctx.send(embed=embed)


  questions[ctx.guild.id].clear()
  embed=discord.Embed(title="واینک بنگرید! پایان بازی!", description="همانا دکتر استرنج فقید گفت: از 14،000،605 احتمال تنها در یک احتمال ما این بازی را ترک خواهیم کرد... :upside_down_face:", color=0x00ff00)
  embed.set_image(url="https://i.imgflip.com/5jw7uz.jpg")
  await asyncio.sleep(5)
  await ctx.send(embed=embed)



alive()
bot.run(TOKEN)

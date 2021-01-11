import dlive
import random

bot = dlive.Bot(command_prefix="!", channels=["Your Channel Name"])

@bot.listener
async def ready():
    print("Ready for commands")

@bot.command()
async def choose(message: dlive.models.Message, a, b):
    await message.chat.send(random.choice(a, b))

bot.run("token")
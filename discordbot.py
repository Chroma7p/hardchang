# discord.pyの大事な部分をimport
from discord.ext import commands
import discord
import os
import asyncio
from dotenv import load_dotenv
from chatgpt import Chat,Role


load_dotenv(".env")

# デプロイ先の環境変数にトークンをおいてね
APITOKEN = os.environ["DISCORD_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

chat=Chat(OPENAI_API_KEY)

# botのオブジェクトを作成(コマンドのトリガーを!に)
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

with open("hard_takanawa.txt","r") as f:
    prompt=f.read()


chat.add(prompt,Role.system)
@bot.tree.command(name="test", description="スラッシュコマンドが機能しているかのテスト用コマンド")
async def test(interaction: discord.Interaction):
    print("test")
    await interaction.response.send_message("test")


# イベントを検知
@bot.event
# botの起動が完了したとき
async def on_ready():
    print("Hello!")  # コマンドラインにHello!と出力


# メッセージ編集時に発動(編集前(before)と後(after)のメッセージを送信)
@bot.event
async def on_message(message:discord.Message):
    if message.author.bot:
        return
    await message.channel.send(chat.send(message.content).content)
    
@bot.command()
async def reset(ctx):
    chat.reset()
    chat.add(prompt,Role.system)
    await ctx.send("リセットしたよー")

async def main():
    # コグのフォルダ
    cogfolder = "cogs."
    # そして使用するコグの列挙(拡張子無しのファイル名)
    cogs = ["sample_cog"]

    for c in cogs:
        await bot.load_extension(cogfolder + c)

    # start the client
    async with bot:
        await bot.start(APITOKEN)

asyncio.run(main())

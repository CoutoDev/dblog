import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import timezone
import pdb;

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

tags = []

@client.event
async def on_ready():
    print(f'Bot está pronto: {client.user.name}')

@client.event
async def on_thread_create(thread):
    if isinstance(thread.parent, discord.ForumChannel):
        # Aqui você pode processar o novo post do fórum
        print(f'Novo post criado: {thread.name}')
        await process_post(thread)

# @client.command()
# async def create_post(ctx, *, content):
#     if isinstance(ctx.channel, discord.ForumChannel):
#         thread = await ctx.channel.create_thread(name="Novo Blog Post", content=content)
#         await ctx.send(f'Post criado: {thread.jump_url}')
#     else:
#         await ctx.send('Este comando só pode ser usado em canais de fórum.')

        
async def process_post(thread):
    user = await client.fetch_user(thread.owner_id)

    if thread.last_message_id is not None:
        message_content = await thread.fetch_message(thread.last_message_id)
    else:
        messages =  [message async for message in thread.history(limit=1)]
        if messages:
            message_content = messages[0]
        else:
            print("Thread is empty")
            return

    title = thread.name
    author = user.display_name
    author_id = user.id
    author_avatar = f'![{user.display_name}]({user.display_avatar.with_size(32).url})'

    pub_date = thread.created_at.replace(tzinfo=timezone.utc).astimezone()
    formatted_date = pub_date.strftime("%Y-%m-%d")

    tags = list(map(format_tags, thread.applied_tags))

    image_urls = [attachment.url for attachment in message_content.attachments if attachment.content_type.startswith("image")]

    image_links = "\n".join(f"![Imagem]({url})" for url in image_urls) if image_urls else ""

    blog_content = f"""
---
title: '{title}'
author: [{author}](https://discordapp.com/users/{author_id})
author_avatar: {author_avatar}
pubDate: {formatted_date}
tags: {tags}
---
{image_links}
{message_content.content}
"""
    
    with open(f"{thread.parent.id}_{thread.id}.md", "w") as file:
        file.write(blog_content)

def format_tags(tag):
    return f'{tag}'

def get_attachment_url(attachment):
    return f'{attachment.url}'

client.run(TOKEN)
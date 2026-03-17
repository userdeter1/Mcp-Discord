import os
import asyncio
import discord
from mcp.server.fastmcp import FastMCP
from pydantic import Field
mcp = FastMCP("Discord MCP")



# discord configuration
Intents = discord.Intents.default()
Intents.message_content = True
Intents.members = True
bot = discord.Client(intents=Intents)

# mcp tools
@mcp.tool(
    name="send_message",
    description="Allow user to send message on discord"
)
async def send_messaage(
    channel_id: str = Field(description="the channel which will send a message"),
    content: str = Field(description="the message we will send")
):
    channel = bot.get_channel(int(channel_id))
    if not channel:
        return "channel introuvable"
    await channel.send(content)
    return "Message envoyé"

@mcp.tool(
    name="read_message",
    description="Allow to read discussion from a channel. Return the messages exactly as received without summarizing"
)
async def read_message(
    channel_id: str = Field(description="the channel which will read a message"),
    limit: int = Field(default=10,description="limit of messages to read")
):
    channel = bot.get_channel(int(channel_id))
    if not channel:
        return "channel introuvable"
    limit = min(limit, 100)
    messages = [f"[{m.author.display_name}] : {m.content}"
    async for m in channel.history(limit=limit)]
    return "\n".join(reversed(messages))


@mcp.tool(
    name="get_channel",
    description="Allow to see all channels in the server"
)
async def get_channel(
    server_id: str = Field(description="The id of the server")
):  
    server = bot.get_guild(int(server_id))
    if not server:
        return "The Id of the server doesn't exist"
    
    channels = [f"#{c.name} (id : {c.id})" for c in server.text_channels]
    return "\n".join(channels)

async def main():
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise ValueError("The token discord is not set")
    
    async with bot:
        asyncio.create_task(bot.start(token))
        await bot.wait_until_ready()
        await mcp.run_stdio_async()

asyncio.run(main())
    


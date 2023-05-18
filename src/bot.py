import logging
import os
import traceback
from pathlib import Path
from typing import Any, Optional

import discord
from discord import TextChannel
from discord.ext import commands

from src.container import Container

logger = logging.getLogger(__name__)


SYNC_COMMANDS = True  # Set to false for faster startup, but commands will not be synced with discord
cogs_dir = Path("./src/cogs")
cogs_base_path = ".".join(cogs_dir.parts)


class WeatherBot(commands.Bot):
    # NB: Commands available in self.tree
    def __init__(self, container: Container) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix="", intents=intents)
        self.dev_channel: Optional[TextChannel] = None
        self.target_channel: Optional[TextChannel] = None
        # Set dependencies, that is, the bot will act as a service container for cogs as they (only) take the bot as dependency
        # XXX: Create own solution for automatic dependency injection when loading cogs?
        self.container = container
        self.config = container.config

    async def setup_hook(self):
        await self._load_cogs()

    async def on_ready(self):
        await self._sync_commands()
        # Get channels of interest
        self.dev_channel = self._get_text_channel_or_raise(self.config.dev_channel_id)
        self.target_channel = self._get_text_channel_or_raise(
            self.config.target_channel_id
        )
        ready_msg = f"Bot is online ({self.user})"
        logger.info(ready_msg)
        await self.dev_channel.send(ready_msg)

    # Send any errors to dev channel
    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any):
        trace = traceback.format_exc()
        if self.dev_channel:
            await self.dev_channel.send(f"Exception occured: ```" + trace + "```")
        return await super().on_error(event_method, *args, **kwargs)

    async def _sync_commands(self):
        if SYNC_COMMANDS:
            logger.info("Syncing commands with discord...")
            # await tree.sync() # This takes a while, as it syncs with all guilds
            # Sync with specified target guild to update slash commands instantly
            await self.tree.sync(guild=discord.Object(id=self.config.target_guild_id))
            logger.info("Commands synced")

    def _get_text_channel_or_raise(self, channel_id: int) -> TextChannel:
        channel = self.get_channel(channel_id)
        if not channel:
            raise Exception(f"Channel not found (id: {channel_id})")
        if not isinstance(channel, TextChannel):
            raise Exception(f"Channel is not a text channel (id: {channel_id})")
        return channel

    async def _load_cogs(self):
        logger.info(f"Loading cogs from: {cogs_dir.resolve()}")
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py"):
                await self.load_extension(f"{cogs_base_path}.{filename[:-3]}")
                logger.info(f"Cog loaded: {filename[:-3]}")

    def _print_commands(self):
        for command in self.tree.get_commands():
            logger.info(command.name)

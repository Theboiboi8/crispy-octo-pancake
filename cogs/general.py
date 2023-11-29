""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import platform
import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
	def __init__(self, bot) -> None:
		self.bot = bot
		self.context_menu_user = app_commands.ContextMenu(
			name="Grab ID", callback=self.grab_id
		)
		self.bot.tree.add_command(self.context_menu_user)
		self.context_menu_message = app_commands.ContextMenu(
			name="Remove spoilers", callback=self.remove_spoilers
		)
		self.bot.tree.add_command(self.context_menu_message)

	# Message context menu command
	async def remove_spoilers(
			self, interaction: discord.Interaction, message: discord.Message
	) -> None:
		"""
		Removes the spoilers from the message. This command requires the MESSAGE_CONTENT intent to work properly.

		:param interaction: The application command interaction.
		:param message: The message that is being interacted with.
		"""
		spoiler_attachment = None
		for attachment in message.attachments:
			if attachment.is_spoiler():
				spoiler_attachment = attachment
				break
		embed = discord.Embed(
			title="Message without spoilers",
			description=message.content.replace("||", ""),
			color=0xBEBEFE,
		)
		if spoiler_attachment is not None:
			embed.set_image(url=attachment.url)
		await interaction.response.send_message(embed=embed, ephemeral=True)

	# User context menu command
	async def grab_id(
			self, interaction: discord.Interaction, user: discord.User
	) -> None:
		"""
		Grabs the ID of the user.

		:param interaction: The application command interaction.
		:param user: The user that is being interacted with.
		"""
		embed = discord.Embed(
			description=f"The ID of {user.mention} is `{user.id}`.",
			color=0xBEBEFE,
		)
		await interaction.response.send_message(embed=embed, ephemeral=True)

	@commands.hybrid_command(
		name="help", description="List all commands the bot has loaded."
	)
	async def help(self, context: Context) -> None:
		prefix = self.bot.config["prefix"]
		embed = discord.Embed(
			title="Help", description="List of available commands:", color=0xBEBEFE
		)
		for i in self.bot.cogs:
			if i == "owner" and not (await self.bot.is_owner(context.author)):
				continue
			cog = self.bot.get_cog(i.lower())
			commands = cog.get_commands()
			data = []
			for command in commands:
				description = command.description.partition("\n")[0]
				data.append(f"{prefix}{command.name} - {description}")
			help_text = "\n".join(data)
			embed.add_field(
				name=i.capitalize(), value=f"```{help_text}```", inline=False
			)
		await context.send(embed=embed)

	@commands.hybrid_command(
		name="botinfo",
		description="Get some useful (or not) information about the bot.",
	)
	async def botinfo(self, context: Context) -> None:
		"""
		Get some useful (or not) information about the bot.

		:param context: The hybrid command context.
		"""
		embed = discord.Embed(
			description="The crispiest octo pancake to ever pancake",
			color=0xBEBEFE,
		)
		embed.set_author(name="Bot Information")
		embed.add_field(name="Created by:", value="ktanchev", inline=True)
		embed.add_field(name="Using:", value="Python-Discord-Bot-Template by kkrypt0nn on GitHub", inline=True)
		embed.add_field(
			name="Python Version:", value=f"{platform.python_version()}", inline=True
		)
		embed.add_field(
			name="Prefix:",
			value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
			inline=False,
		)
		embed.set_footer(text=f"Requested by {context.author}")
		await context.send(embed=embed)

	@commands.hybrid_command(
		name="serverinfo",
		description="Get some useful (or not) information about the server.",
	)
	async def serverinfo(self, context: Context) -> None:
		"""
		Get some useful (or not) information about the server.

		:param context: The hybrid command context.
		"""
		roles = [role.name for role in context.guild.roles]
		if len(roles) > 50:
			roles = roles[:50]
			roles.append(f">>>> Displaying [50/{len(roles)}] Roles")
		roles = ", ".join(roles)

		embed = discord.Embed(
			title="**Server Name:**", description=f"{context.guild}", color=0xBEBEFE
		)
		if context.guild.icon is not None:
			embed.set_thumbnail(url=context.guild.icon.url)
		embed.add_field(name="Server ID", value=context.guild.id)
		embed.add_field(name="Member Count", value=context.guild.member_count)
		embed.add_field(
			name="Text/Voice Channels", value=f"{len(context.guild.channels)}"
		)
		embed.add_field(name=f"Roles ({len(context.guild.roles)})", value=roles)
		embed.set_footer(text=f"Created on: {context.guild.created_at}")
		await context.send(embed=embed)

	@commands.hybrid_command(
		name="ping",
		description="Check if the bot is alive.",
	)
	async def ping(self, context: Context) -> None:
		"""
		Check if the bot is alive.

		:param context: The hybrid command context.
		"""
		embed = discord.Embed(
			title="🏓 Pong!",
			description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
			color=0xBEBEFE,
		)
		await context.send(embed=embed)

	@commands.hybrid_command(
		name="invite",
		description="Get a link to invite the bot to your server.",
	)
	async def invite(self, context: Context) -> None:
		"""
		Get a link to invite the bot to your server.

		:param context: The hybrid command context.
		"""
		embed = discord.Embed(
			description=f"Invite me by clicking [here]({self.bot.config['invite_link']}).",
			color=0xD75BF4,
		)
		try:
			await context.author.send(embed=embed)
			await context.send("I sent you a private message!")
		except discord.Forbidden:
			await context.send(embed=embed)

	@commands.hybrid_command(
		name="support",
		description="Join the support server.",
	)
	async def server(self, context: Context) -> None:
		"""
		Join the support server.

		:param context: The hybrid command context.
		"""
		embed = discord.Embed(
			description=f"Join the support server for the bot by clicking [here](https://discord.gg/f74GGrvHHZ).",
			color=0xD75BF4,
		)
		try:
			await context.author.send(embed=embed)
			await context.send("I sent you a private message!")
		except discord.Forbidden:
			await context.send(embed=embed)

	@commands.hybrid_command(
		name="8ball",
		description="Ask the bot a question and receive a \"yes\" or \"no\" answer, or somewhere inbetween.",
	)
	@app_commands.describe(question="The question you want to ask.")
	async def eight_ball(self, context: Context, *, question: str) -> None:
		"""
		Ask the bot a question and receive a \"yes\" or \"no\" answer, or somewhere inbetween.

		:param context: The hybrid command context.
		:param question: The question that should be asked by the user.
		"""
		answers = [
			"It is certain.",
			"It is decidedly so.",
			"You may rely on it.",
			"Without a doubt.",
			"Yes - definitely.",
			"As I see, yes.",
			"Most likely.",
			"Outlook good.",
			"Yes.",
			"Signs point to yes.",
			"Reply hazy, try again.",
			"Ask again later.",
			"Better not tell you now.",
			"Cannot predict now.",
			"Concentrate and ask again later.",
			"Don't count on it.",
			"My reply is no.",
			"My sources say no.",
			"Outlook not so good.",
			"Very doubtful.",
		]
		embed = discord.Embed(
			title="**My Answer:**",
			description=f"{random.choice(answers)}",
			color=0xBEBEFE,
		)
		embed.set_footer(text=f"The question was: {question}")
		await context.send(embed=embed)

	@commands.hybrid_command(
		name="random",
		description="Choose a random number from a given range."
	)
	@app_commands.describe(number1="Lower bound (Floor)", number2="Upper bound (Ceiling)")
	async def random_number(self, context: Context, *, number1: int, number2: int) -> None:
		"""
		Choose a random number from a given range.

		:param context: The hybrid command context.
		:param number1: The lower bound for the random operation.
		:param number2: The upper bound for the random operation.
		"""
		embed = discord.Embed(
			title="**Random Number:**",
			description=f"{random.randint(number1, number2)}",
			color=0xBEBEFE,
		)
		embed.set_footer(text=f"The number range was from {number1} to {number2}")
		await context.send(embed=embed)


async def setup(bot) -> None:
	await bot.add_cog(General(bot))

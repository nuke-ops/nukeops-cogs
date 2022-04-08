from redbot.core import commands, checks, Config
import random
import mysql.connector
import discord
from discord.utils import get
from discord.ext.commands import Bot

"""
Reminder: Add JSON support instead of using sql
"""
from .conf import credentials
mydb = credentials()
cursor = mydb.cursor()

class NukeOpsCog(commands.Cog):
	"""My custom cog
	Feel free to ping/pm me(maksxpl#8503) if you found a bug
	or if you got an idea for a new feture."""

	def __init__(self, bot):
		self.bot = bot

	# @commands.command()
	# @checks.admin_or_permissions(administrator=True)
	# async def dice(self, ctx):
		# await ctx.send("Exiting..")
		# exit()

	@commands.command()
	# @checks.admin_or_permissions(administrator=True)
	async def dice(self, ctx, *, throw: str):
		"""Syntax: ``!red dice [dices]d[sides]``"""
		throw_array = throw.split("d")
		if "d" in throw and (len(throw_array)) == 2:
			dices = throw_array[0]
			sides = throw_array[-1]
			summary = 0
			pre_all_rolls = str()
			for rolls in range(int(dices)):
				roll = random.randint(1, int(sides))
				pre_all_rolls += str(roll) + ", "
				summary += roll
			all_rolls = pre_all_rolls[:-2]
			if "," in all_rolls:
				all_rolls+=" | Summary: "+str(summary)
				await ctx.send(all_rolls)
			else:
				await ctx.send(all_rolls)
		elif not "d" in throw or (len(throw_array)) != 2:
			embed=discord.Embed(color=0xff0000)
			embed.add_field(name="Wrong syntax.", 	value="``!red dice [dices]d[sides]``", inline=False)
			embed.add_field(name="example:", 		value="``!red dice 1d20``", inline=False)
			await ctx.send(embed=embed)


	@commands.group()
	async def warframe(self, ctx):
		pass

	@warframe.group()
	async def check(self, ctx):	
		pass

	@check.command()
	async def ign(self, ctx, In_Game_Name: str):
		""" |``!red warframe check ign [someone's in-game name]``|"""
		cursor.execute("SELECT * FROM ign WHERE ign_name = '%s'" % In_Game_Name)
		myresult = cursor.fetchall()
		if not myresult:
			await ctx.send("user_doesnt_exist")
		else:
			for user in myresult:
				id, discord_name, ign_name, affiliation = user
			embed=discord.Embed(color=0xff0000)
			embed.add_field(name="Discord name", 	value="``"+discord_name+"``", inline=False)
			embed.add_field(name="In-game name", 	value="``"+ign_name+"``", inline=False)
			embed.add_field(name="Affiliation", 	value="``"+affiliation+"``", inline=False)
			await ctx.send(embed=embed)

	@check.command()
	async def dn(self, ctx, Discord_Name: str):
		""" |``!red warframe check dn [someone's discord name]``|"""
		cursor.execute("SELECT * FROM ign WHERE discord_name = '%s'" % Discord_Name)
		myresult = cursor.fetchall()
		if not myresult:
			await ctx.send("user_doesnt_exist")
		else:
			for user in myresult:
				id, discord_name, ign_name, affiliation = user
			embed=discord.Embed(color=0xff0000)
			embed.add_field(name="Discord name", 	value="``"+discord_name+"``", inline=False)
			embed.add_field(name="In-game name", 	value="``"+ign_name+"``", inline=False)
			embed.add_field(name="Affiliation", 	value="``"+affiliation+"``", inline=False)
			await ctx.send(embed=embed)


	@warframe.command()
	async def register(self, ctx, In_Game_Name: str, Affiliation: int):
		# """ |``!red warframe wfhelpRegister``|"""
		user_name = (f"{ctx.author}")
		id = int()
		discord_name = str()
		affiliation = str()
		ign_name = str()
		user = str()

		cursor.execute("SELECT * FROM ign WHERE discord_name = '%s'" % user_name)
		myresult = cursor.fetchall()
		for user in myresult:
			id, discord_name, ign_name, affiliation = user

		user_doesnt_exist = 0
		if user_name in user:
			await ctx.send("You're already registrated.")
		else:
			user_doesnt_exist == 1

			cursor.execute("SELECT * FROM ign WHERE ign_name = '%s'" % In_Game_Name)
			myresult = cursor.fetchall()

			check1 = 1
			check2 = 1
			check3 = 1
			if Affiliation < 0: 		check1 = 1
			if Affiliation > 2:			check2 = 1
			if user_doesnt_exist == 1: 	check3 = 1
			if check1 == 1 and check2 == 1 and check3 == 1:
				if Affiliation == 0: Affiliation = "none"
				elif Affiliation == 1: Affiliation = "Clan"
				elif Affiliation == 2: Affiliation = "Alliance"

				sql = "INSERT INTO ign (discord_name, ign_name, affiliation) VALUES (%s, %s, %s)"
				ign_name = In_Game_Name
				discord_name = user_name
				# user_name = str()
				val = (discord_name, ign_name, Affiliation)
				# cursor = mydb.cursor()
				cursor.execute(sql, val)
				mydb.commit()
	
				id = int()
				discord_name = str()
				affiliation = str()
				ign_name = str()

				cursor.execute("SELECT * FROM ign WHERE discord_name = '%s'" % user_name)
				myresult = cursor.fetchall()
				for user in myresult:
					id, discord_name, ign_name, affiliation = user
			if user_name == discord_name:
				await ctx.send(f"User {ctx.author} registrated successfully.")
			else:
				await ctx.send("Something borked")

		cursor.execute("SELECT * FROM ign WHERE discord_name = '%s'" % user_name)
		myresult = cursor.fetchall()
		for user in myresult:
			id, discord_name, ign_name, affiliation = user
		if user_name in user:
			if affiliation == "Clan":
				member = ctx.message.author
				role = ctx.guild.get_role(812407726767472720)
				await member.add_roles(role)
				member = ctx.message.author
				role = ctx.guild.get_role(812416188448768031)
				await member.add_roles(role)
			elif affiliation == "Alliance":
				member = ctx.message.author
				role = ctx.guild.get_role(812416188448768031)
				await member.add_roles(role)

	@warframe.group()
	async def wfhelp(self, ctx):	
		pass

	@wfhelp.command(name="register")
	async def hregister(self, ctx):
		embed=discord.Embed(color=0xff0000)
		embed.add_field(name="Syntax", 	value="``| !red warframe register [Your in-game name] [Affiliation]   |``", inline=False)
		embed.add_field(name="Example", value="``| 0 = None | 1 = Clan | 2 = Alliance |``", inline=False)
		embed.add_field(name="^", 		value="|By Clan I mean our clan named Nuke Ops.                         |", inline=False)
		embed.add_field(name="^", 		value="|By joining the clan, you're automatically a member of alliance. |", inline=False)
		embed.add_field(name="^", 		value="|By Alliance I mean our Alliance named S.E.L.F.                  |", inline=False)
		embed.add_field(name="Example", value="``!red warframe register test 1`` Will register user with the name 'test' as a member of our clan.", inline=False)
		await ctx.send(embed=embed)

	@wfhelp.command(name="check")
	async def hcheck(self, ctx):
		embed=discord.Embed(color=0xff0000)
		embed.add_field(name="Syntax", 	value="``!red warframe check dn/ing [someone's discord/ign]``", inline=False)
		embed.add_field(name="Example", value="``!red warframe check dn maksxpl#8503``", inline=False)
		embed.add_field(name="Example", value="``!red warframe check ign Maksxpl``", inline=False)
		await ctx.send(embed=embed)

	

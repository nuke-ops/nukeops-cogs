from redbot.core import commands, checks, Config, data_manager
import random
import sqlite3

from discord import Embed
from discord.utils import get
from discord.ext.commands import Bot

from .nukeops import check


class NukeOpsCog(commands.Cog):
    """My custom cog
    Feel free to ping/pm me(maksxpl#8503) if you found a bug
    or if you got an idea for a new feature."""

    def __init__(self, bot):
        self.bot = bot


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
                all_rolls += " | Summary: " + str(summary)
                await ctx.send(all_rolls)
            else:
                await ctx.send(all_rolls)
        elif "d" not in throw or (len(throw_array)) != 2:
            embed = Embed(color=0xff0000)
            embed.add_field(name="Wrong syntax.", value="``!red dice [dices]d[sides]``", inline=False)
            embed.add_field(name="example:", value="``!red dice 1d20``", inline=False)
            await ctx.send(embed=embed)

    @commands.group()
    async def warframe(self, ctx):
        pass

    @warframe.group()
    async def check(self, ctx):
        pass

    @check.command()
    async def user(self, ctx, username: str):
        """ |``!red warframe user [username]``|"""
        results = check.user(username)
        if results:
            for x in results:
                await ctx.send(x)
        else: await ctx.send("User doesn't exist")

    @warframe.command()
    async def register(self, ctx, ingame_username: str, affiliation: str):
        if check.database_exist(str(data_manager.cog_data_path(self))+"/warframe.db"):
            pass
        else:
            await ctx.send("Database doesn't exist")
            return

        discord_username = ctx.author

        # check if user already exist in db
        if check.user_exist(discord_username):
            await ctx.send("You're already registered.")
            return
        # Check if user used correct 'affiliation'
        elif affiliation.capitalize() not in ["None", "Clan", "Alliance"]:
            await ctx.send("Wrong affiliation, choose one from list:\
                           ```None, Clan, Alliance```")
            return

        # save user data in db
        try:
            with sqlite3.connect("warframe.db") as conn:
                conn.executescript(f"""
                               insert into nicknames (discord_name, warframe_name, affiliation)
                               values('{discord_username}', '{ingame_username}', '{affiliation}');
                               """)
                await ctx.send("Registration complete\n\
                               ```Discord: {DiscordUsername}\nWarframe: {In_Game_Name}\nAffiliation: {Affiliation}```")

        # Assign ranks based on affiliation
        except Exception as Error:
            await ctx.send("Error 1")
            print(Error)
        try:
            if affiliation == "Clan":
                role = ctx.guild.get_role(812407726767472720)  # clan
                await ctx.message.author.add_roles(role)

                role = ctx.guild.get_role(812416188448768031)  # alliance
                await ctx.message.author.add_roles(role)

            if affiliation == "Alliance":
                role = ctx.guild.get_role(812416188448768031)  # alliance
                await ctx.message.author.add_roles(role)

        except Exception as Error:
            await ctx.send("Error 2")
            print(Error)

    @warframe.group()
    async def wfhelp(self, ctx):
        pass

    @wfhelp.command(name="register")
    async def hregister(self, ctx):
        embed = Embed(color=0xff0000)
        embed.add_field(name="Syntax", value="``| !red warframe register [Your in-game name] [Affiliation]   |``",
                        inline=False)
        embed.add_field(name="Example", value="``| 0 = None | 1 = Clan | 2 = Alliance |``", inline=False)
        embed.add_field(name="^", value="|By Clan I mean our clan named Nuke Ops.                         |",
                        inline=False)
        embed.add_field(name="^", value="|By joining the clan, you're automatically a member of alliance. |",
                        inline=False)
        embed.add_field(name="^", value="|By Alliance I mean our Alliance named S.E.L.F.                  |",
                        inline=False)
        embed.add_field(name="Example",
                        value="``!red warframe register test 1``\
                        Will register user with the name 'test' as a member of our clan.",
                        inline=False)
        await ctx.send(embed=embed)

    @wfhelp.command(name="check")
    async def check_help(self, ctx):
        embed = Embed(color=0xff0000)
        embed.add_field(name="Syntax", value="``!red warframe check [Discord/in-game username]``", inline=False)
        embed.add_field(name="Example", value="``!red warframe check dn maksxpl#8503``", inline=False)
        embed.add_field(name="Example", value="``!red warframe check ign Maksxpl``", inline=False)
        await ctx.send(embed=embed)

import asyncio
from datetime import datetime, timedelta
import discord
from discord import member
from discord.ext import commands
import json
from discord import NotFound, Object
from typing import Optional
import datetime
from discord.utils import find
from discord.ext.commands import BadArgument, MemberNotFound
from discord.ext.commands import Greedy, Converter


warning_color = 0xff0400
role_ids = {}



class BannedUser(Converter):
    async def convert(self, ctx, arg):
        if ctx.guild.me.guild_permissions.ban_members:
            if arg.isdigit():
                try:
                    return (await ctx.guild.fetch_ban(Object(id=int(arg)))).user
                except NotFound:
                    await ctx.send("Mentioned user is not banned from the server or is not a valid user.")

        banned = [e.user for e in await ctx.guild.bans()]
        if banned:
            if (user := find(lambda u: str(u) == arg, banned)) is not None:
                return user
            else:
                raise BadArgument


class Automod(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def kick_member(self, ctx, member, reason):
        if ctx.guild.me.top_role.position < member.top_role.position or member == ctx.guild.owner:
            await ctx.send("I can't ban Owner/Modeartors/Staff.")
            return
        # with open("./json/config.json", "r") as json_file:
        #     config = json.load(json_file)
        # try:
        #     logchanel_id = config[("Guild_ID_" + str(ctx.guild.id))
        #                           ]["Configuration"]["Logchannel"]
        #     log_channel = self.client.get_channel(id=logchanel_id)
        # except KeyError:
        #     log_channel = ctx.channel
        # await member.send(f"You got banned from server **{ctx.guild.name}** by **{ctx.author.name}** for reason: `{reason}`")
        await member.kick(reason=reason)
        await ctx.send(f" Member ID : ||{member.id}||")
        ban_embed = discord.Embed(title="Member Kicked!", colour=warning_color)
        ban_embed.add_field(name="User", value=member.name)
        ban_embed.add_field(name="Kicked by", value=ctx.author.name)
        ban_embed.add_field(name="Reason", value=reason)
        ban_embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=ban_embed)

    async def ban_member(self, ctx, member, reason):
        if ctx.guild.me.top_role.position < member.top_role.position or member == ctx.guild.owner:
            await ctx.send("I can't ban Owner/Modeartors/Staff.")
            return
        # with open("./json/config.json", "r") as json_file:
        #     config = json.load(json_file)
        # try:
        #     logchanel_id = config[("Guild_ID_" + str(ctx.guild.id))
        #                           ]["Configuration"]["Logchannel"]
        #     log_channel = self.client.get_channel(id=logchanel_id)
        # except KeyError:
        #     log_channel = ctx.channel
        await member.send(f"You got banned from server **{ctx.guild.name}** by **{ctx.author.name}** for reason: `{reason}`")
        await member.ban(reason=reason)
        await ctx.send(f" Member ID : ||{member.id}||")
        ban_embed = discord.Embed(title="Member banned", colour=warning_color)
        ban_embed.add_field(name="User", value=member.name)
        ban_embed.add_field(name="Banned by", value=ctx.author.name)
        ban_embed.add_field(name="Reason", value=reason)
        ban_embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=ban_embed)

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        await self.ban_member(ctx, member, reason)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing `ban_member` permission for above action.", colour=warning_color)
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, MemberNotFound):
            embed = discord.Embed(
                description="Can't ban user who is not in server.", colour=warning_color)
            await ctx.send(embed=embed, delete_after=10)

    async def unban_member(self, ctx, members, reason):
        for member in members:
            # with open("./json/config.json", "r") as json_file:
            #     config = json.load(json_file)
            # try:
            #     logchanel_id = config[(
            #         "Guild_ID_" + str(ctx.guild.id))]["Configuration"]["Logchannel"]
            #     log_channel = self.client.get_channel(id=logchanel_id)
            # except KeyError:
            #     log_channel = ctx.channel

            await ctx.guild.unban(user=member, reason=reason)
            await ctx.send(f" Member ID : ||{member.id}||")
            ban_embed = discord.Embed(
                title="Member Unbanned", colour=warning_color)
            ban_embed.add_field(name="User", value=member.name)
            ban_embed.add_field(name="Reason", value=reason)
            ban_embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=ban_embed)

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member: Greedy[BannedUser], *, reason: Optional[str] = "No reason provided"):
        await self.unban_member(ctx, member, reason)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing `ban_member` permission for above action.", colour=warning_color)
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, MemberNotFound):
            embed = discord.Embed(
                description="Mentioned user is not banned from the server.", colour=warning_color)
            await ctx.send(embed=embed, delete_after=10)

    async def member_role(self, member):
        role_id = ",".join(str(r.id) for r in member.roles)
        role_ids.append(role_id)

    async def mute_members(self, ctx, member, time, reason):
        # with open("./json/config.json", "r") as json_file:
        #     config = json.load(json_file)
        # try:
        #     logchanel_id = config[("Guild_ID_" + str(ctx.guild.id))
        #                           ]["Configuration"]["Logchannel"]
        #     log_channel = self.client.get_channel(id=logchanel_id)
        # except KeyError:
        #     log_channel = ctx.channel  # sourcery no-metrics
        # json_file = open("./json/mute.json", "r")
        # mute_members = json.load(json_file)
        try:
            # Gets the numbers from the time argument, start to -1
            seconds = time[:-1]
            duration = time[-1]  # Gets the timed maniulation, s, m, h, d
            if duration == "s":
                seconds = seconds * 1
            elif duration == "m":
                seconds = seconds * 60
            elif duration == "h":
                seconds = seconds * 60 * 60
            elif duration == "d":
                seconds = seconds * 86400
            else:
                await ctx.send("Invalid duration input")
                return
        except Exception as e:
            print(e)
            await ctx.send("Invalid time input")
            return

        unmutes = []
        admin_id = self.client.id if ctx.author.id == member.id else ctx.author.id
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role not in ctx.guild.roles:
            await ctx.guild.create_role(name="Muted", permissions=0)
        if (mute_role not in member.roles):
            # end_time = datetime.utcnow() + timedelta(seconds=seconds) if time else None
            # if str(ctx.guild.id) not in mute_members:
            #     mute_members[str(ctx.guild.id)] = {}
            #     mute_members[str(ctx.guild.id)][str(member.id)] = {'role_ids': role_ids,
            #                                                        "time": getattr(end_time, "isoformat", lambda: None)(),
            #                                                        "Reason": reason}
            # elif str(member.id) not in mute_members[str(ctx.guild.id)]:
            #     mute_members[str(ctx.guild.id)][str(member.id)] = {'role_ids': role_ids,
            #                                                        "time": getattr(end_time, "isoformat", lambda: None)(), "Reason": reason}
            await member.add_roles(mute_role)

            embed = discord.Embed(title="Member muted",
                                  colour=0xDD2222,
                                  timestamp=datetime.datetime.utcnow())

            embed.set_thumbnail(url=member.avatar_url)
            admin = await ctx.guild.fetch_member(admin_id)
            fields = [("Member", member.mention, False),
                      ("Duration",
                       f"{time}" if time else "Indefinite", True),
                      ("Reason", reason, True),
                      ("Actioned by", admin.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)
            if time:
                unmutes.append(member)

            # with open("./JSON/mute_members.json", "w") as f:
            #     json.dump(mute_members, f, indent=4)
        elif ctx.guild.me.top_role.position < member.top_role.position:
            await ctx.send("I can't mute Owner/Staff/Moderators.")
        else:
            await ctx.channel.send("Member is already muted.")
        return unmutes

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True, manage_guild=True)
    async def mute_command(self, ctx, member: discord.Member, time, *, reason: Optional[str] = "No reason provided."):
        try:
            # Gets the numbers from the time argument, start to -1
            seconds = time[:-1]
            seconds = int(seconds)
            duration = time[-1]  # Gets the timed maniulation, s, m, h, d
            if duration == "s":
                seconds *= 1
            elif duration == "m":
                seconds *= 60
            elif duration == "h":
                seconds = seconds * 60 * 60
            elif duration == "d":
                seconds *= 86400
            else:
                await ctx.send("Invalid duration input")
                return
        except Exception as e:
            print(e)
            await ctx.send("Invalid time input")
            return
        if not member:
            await ctx.send("One or more required arguments are missing.")

        else:

            unmutes = await self.mute_members(ctx, member, time, reason)
            await ctx.send("Action complete.")

            if len(unmutes):
                await asyncio.sleep(seconds)
                await self.unmute_members(ctx.guild, member)

    async def unmute_members(self, ctx, member, *, reason="Mute time expired."):
        # with open("./json/config.json", "r") as json_file:
        #     config = json.load(json_file)
        # # try:
        # #     logchanel_id = config[("Guild_ID_" + str(ctx.guild.id))
        # #                           ]["Configuration"]["Logchannel"]
        # #     log_channel = self.client.get_channel(id=logchanel_id)
        # # except KeyError:
        #     log_channel = ctx.channel  # sou
        # with open("./json/mute.json") as f:
        #     mute_member = json.load(f)
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:

            # role_ids = mute_member[str(ctx.guild.id)][str(member.id)]['role_ids']
            # roles = [ctx.guild.get_role(int(id_))
            #          for id_ in role_ids.split(",") if len(id_)]
            await member.remove_roles(mute_role)

            # del mute_member[str(ctx.guild.id)][str(member.id)]

            

            embed = discord.Embed(title="Member unmuted",
                                  colour=warning_color,
                                  timestamp=datetime.datetime.utcnow())

            embed.set_thumbnail(url=member.avatar_url)

            fields = [("Member", member.mention, False),
                      ("Reason", reason, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Member is not muted.')
        # with open("./json/mute.json", "w") as f:
        #     json.dump(mute_member, f, indent=4)

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True, manage_guild=True)
    async def unmute_command(self, ctx, members: discord.Member, *, reason: Optional[str] = "No reason provided."):
        if not members:
            await ctx.send("One or more required arguments is missing.")

        else:
            await self.unmute_members(ctx, members, reason=reason)


def setup(client):
    client.add_cog(Automod(client))
    print(" <Mod cog is loaded>")

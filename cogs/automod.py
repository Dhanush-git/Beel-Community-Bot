import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from discord import NotFound, Object
from typing import Optional
import datetime
from discord.ext.commands.errors import MissingRequiredArgument
from discord.utils import find
from discord.ext.commands import BadArgument, MemberNotFound
from discord.ext.commands import Greedy, Converter


warning_color = 0xff0400


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


async def kick_member(ctx, member, reason):
    if ctx.guild.me.top_role < member.top_role or ctx.message.author.top_role < member.top_role:
        await ctx.send("I can't Kick Owner/Moderators/Staff.")
        return
    # with open("./json/config.json", "r") as json_file:
    #     config = json.load(json_file)
    # try:
    #     logchanel_id = config[("Guild_ID_" + str(ctx.guild.id))
    #                           ]["Configuration"]["Logchannel"]
    #     log_channel = self.client.get_channel(id=logchanel_id)
    # except KeyError:
    #     log_channel = ctx.channel
    await member.send(f"You got Kicked from server **{ctx.guild.name}** by **{ctx.author.name}** for reason: `{reason}`")
    await member.kick(reason=reason)
    await ctx.send(f" Member ID : ||{member.id}||")
    ban_embed = discord.Embed(title="Member Kicked!", colour=warning_color)
    ban_embed.add_field(name="User", value=member.name, inline = False)
    ban_embed.add_field(name="Kicked by", value=ctx.author.name, inline = True)
    ban_embed.add_field(name="Reason", value=reason, inline = True)
    ban_embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=ban_embed)


async def ban_member(ctx, member, reason):
    if ctx.guild.me.top_role.position < member.top_role.position or member == ctx.guild.owner:
        await ctx.send("I can't ban Owner/Moderators/Staff.")
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
    ban_embed.add_field(name="User", value=member.name, inline = False)
    ban_embed.add_field(name="Banned by", value=ctx.author.name, inline = True)
    ban_embed.add_field(name="Reason", value=reason, inline = True)
    ban_embed.set_thumbnail(url = member.avatar_url)
    ban_embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=ban_embed)


async def unban_member(ctx, members, reason):
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
        ban_embed.add_field(name="User", value=member.name, inline = False)
        ban_embed.add_field(name="Reason", value=reason, inline = False)
        ban_embed.set_thumbnail(url = member.avatar_url)
        ban_embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=ban_embed)


async def unmute_members(ctx, member, *, reason="Mute time expired."):
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
        embed = discord.Embed(title="Member unmuted",
                              colour=warning_color,
                              timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=member.avatar_url)

        fields = [("Member", member.mention, False),
                  ("Reason", reason, False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)
        # del mute_member[str(ctx.guild.id)][str(member.id)]
    else:
        await ctx.send("Member is not muted")
    # with open("./json/mute.json", "w") as f:
    #     json.dump(mute_member, f, indent=4)


class Automod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "kick")
    @commands.has_guild_permissions(kick_members=True)
    async def _kick(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        await kick_member(ctx, member, reason)

    @_kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing `Kick_member` permission for above action.", colour=warning_color)
            await ctx.send(embed=embed)
        elif isinstance(error, MemberNotFound):
            embed = discord.Embed(
                description="Can't kick user who is not in server.", colour=warning_color)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        await ban_member(ctx, member, reason=reason)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing `ban_member` permission for above action.", colour=warning_color)
            await ctx.send(embed=embed)
        elif isinstance(error, MemberNotFound):
            embed = discord.Embed(
                description="Can't ban user who is not in server.", colour=warning_color)
            await ctx.send(embed=embed)

    @commands.command(aliases=['clearuser'], description="Clear messages of particular user in a channel")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purgeuser(self, ctx, user: discord.Member = None, num_messages: Optional[int] = 100):
        user = user or ctx.author
        channel = ctx.message.channel
        if ctx.guild.me.top_role < user.top_role or ctx.message.author.top_role < user.top_role:
            return await ctx.send("Sorry!, I can't clear messages of Owner/staff/moderators.")

        def check(msg):
            return msg.author.id == user.id

        await ctx.message.delete()
        await channel.purge(limit=num_messages, check=check, before=None)
        await ctx.send(f"Cleared {num_messages} messages of **{user.name}** in channel {ctx.channel.mention}")

    @commands.command(name='clear', help='Using this command you can clear messages in any channel.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount1: int = None):
        if amount1 is None:
            amount1 = 10
        channel = ctx.message.channel
        if 0 < amount1 <= 100:
            await channel.purge(limit=amount1)
            await ctx.send(f"Cleared {amount1} messages")

        else:
            await ctx.send("Limit provided is not in range.")

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member: Greedy[BannedUser], *, reason: Optional[str] = "No reason provided"):
        await unban_member(ctx, member, reason)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing `ban_member` permission for above action.", colour=warning_color)
            await ctx.send(embed=embed)
        elif isinstance(error, MemberNotFound):
            embed = discord.Embed(
                description="Mentioned user is not banned from the server.", colour=warning_color)
            await ctx.send(embed=embed)

    async def mute_members(self, ctx, member, time, reason):
        if ctx.guild.me.top_role.position < member.top_role.position or member == ctx.guild.owner:
            return await ctx.send("I can't ban Owner/Moderators/Staff.")
        
        # with open("./json/config.json", "r") as json_file:
        #     config = json.load(json_file)
        # try:
        #     logchanel_id = config[("Guild_ID_" + str(ctx.guild.id))
        #                           ]["Configuration"]["Logchannel"]
        #     log_channel = self.client.get_channel(id=logchanel_id)
        # except KeyError:
        #     log_channel = ctx.channel  # sorcery no-metrics
        # json_file = open("./json/mute.json", "r")
        # mute_members = json.load(json_file)
        unmutes = []
        admin_id = self.client.user.id if ctx.author.id == member.id else ctx.author.id
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role not in ctx.guild.roles:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        if mute_role not in member.roles:
            # end_time = datetime.uptown() + timedelta(seconds=seconds) if time else None
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
                       f"{time} hour(s)" if time else "Indefinite", True),
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
    async def mute_command(self, ctx, member: discord.Member, time: Optional[int], *, reason: Optional[str] = "No reason provided.", ):
        # if time:

        #     try:
        #     # Gets the numbers from the time argument, start to -1

        #         seconds = time[:-1]
        #         seconds = int(seconds)
        #         duration = time[-1]  # Gets the timed manipulation, s, m, h, d
        #         if duration == "s":
        #             seconds *= 1
        #         elif duration == "m":
        #             seconds *= 60
        #         elif duration == "h":
        #             seconds = seconds * 60 * 60
        #         elif duration == "d":
        #             seconds *= 86400
        #         else:
        #             await ctx.send("Invalid duration input")
        #             return
        #     except Exception as e:
        #         print(e)
        #         await ctx.send('Invalid time input')
        #         return
        unmutes = await self.mute_members(ctx, member, time, reason)
        await ctx.send("Action complete.")
        if len(unmutes):
            time = time * 60 * 60
            await asyncio.sleep(time)
            await unmute_members(ctx, member)

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True, manage_guild=True)
    async def unmute_command(self, ctx, members: discord.Member, *, reason: Optional[str] = "No reason provided."):
        await unmute_members(ctx, members, reason=reason)

    @mute_command.error
    async def _error(self, ctx, member):
        if isinstance(member, MissingRequiredArgument):
            await ctx.send("Oh no! You forget to mention user.")

        elif isinstance(member, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing `manage_guild` permission for above action.", colour=warning_color)
            await ctx.send(embed=embed)

    @unmute_command.error
    async def _error(self, ctx, member):
        if isinstance(member, MissingRequiredArgument):
            await ctx.send("Oh no! You forget to mention user.")

        elif isinstance(member, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing `manage_guild` permission for above action.", colour=warning_color)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(" <Mod cog is loaded>")


def setup(client):
    client.add_cog(Automod(client))

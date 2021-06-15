from os import name
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import datetime
from discord import Spotify
import requests
import random
import asyncio

warning_color = 0xff0400


class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="ban", description="Bans mention user from server.")
    async def slash_ban(self, ctx: SlashContext, member: discord.Member, *, reason=None):
        if ctx.guild.me.top_role < member.top_role or ctx.author.top_role < member.top_role:
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
        if reason is None:
            reason = "No reason provided"
        await member.send(
            f"You got banned from server **{ctx.guild.name}** by **{ctx.author.name}** for reason: `{reason}`")
        await member.ban(reason=reason)
        ban_embed = discord.Embed(title="Member banned", colour=warning_color)
        ban_embed.add_field(name="Member ID", value=member.id, inline=False)
        ban_embed.add_field(name="User", value=member.name, inline=False)
        ban_embed.add_field(
            name="Banned by", value=ctx.author.name, inline=False)
        ban_embed.add_field(name="Reason", value=reason, inline=False)
        ban_embed.set_thumbnail(url=member.avatar_url)
        ban_embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=ban_embed)

    @cog_ext.cog_slash(name="kick", description="Kick member from server.")
    async def slash_kick(self, ctx: SlashContext, member: discord.Member, *, reason=None):
        if ctx.guild.me.top_role < member.top_role or ctx.author.top_role < member.top_role:
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
        if reason is None:
            reason = "No reason provided"
        await member.send(
            f"You got Kicked from server **{ctx.guild.name}** by **{ctx.author.name}** for reason: `{reason}`")
        await member.kick(reason=reason)
        kick_embed = discord.Embed(
            title="Member Kicked!", colour=warning_color)
        kick_embed.add_field(name="Member ID ", value=member.id, inline=False)
        kick_embed.add_field(name="User", value=member.name, inline=False)
        kick_embed.add_field(
            name="Kicked by", value=ctx.author.name, inline=True)
        kick_embed.add_field(name="Reason", value=reason, inline=True)
        kick_embed.set_thumbnail(url=member.avatar_url)
        kick_embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=kick_embed)

    @cog_ext.cog_slash(name='clear', description='clears messages in any channel.')
    async def slash_clear(self, ctx: SlashContext, amount1: int = None):
        if amount1 is None:
            amount1 = 10
        if 0 < amount1 <= 100:
            await ctx.channel.purge(limit=amount1)
            await ctx.send(f"Cleared {amount1} messages")

        else:
            await ctx.send("Limit provided is not in range.")

    @cog_ext.cog_slash(name='clearuser', description="Clear messages of particular user in a channel")
    async def slash_purgeuser(self, ctx: SlashContext, user: discord.Member = None, num_messages: int = None):
        if num_messages is None:
            num_messages = 100
        user = user or ctx.author
        if ctx.guild.me.top_role < user.top_role or ctx.author.top_role < user.top_role:
            return await ctx.send("Sorry!, I can't clear messages of Owner/staff/moderators.")

        def check(msg):
            return msg.author.id == user.id

        await ctx.channel.purge(limit=num_messages, check=check, before=None)
        await ctx.send(f"Cleared {num_messages} messages of **{user.name}** in channel {ctx.channel.mention}")

    @cog_ext.cog_slash(name="spotify", description="Sends song title and Author of song user is listening on Spotify")
    async def slash_spotify(self, ctx: SlashContext, user: discord.Member):
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = discord.Embed(
                        title=f"{user.name}'s Spotify",
                        description="Listening to {}".format(activity.title),
                        color=activity.colour)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.set_footer(text="Song started at {}".format(
                        activity.created_at.strftime("%H:%M")))
                    await ctx.send(embed=embed)
        else:
            await ctx.send("user is not listening to any song ")

    @cog_ext.cog_slash(name="joke", description="Sends joke")
    async def slash_joke(self, ctx: SlashContext):
        req = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = req.json()
        embed = discord.Embed(
            title="{}".format(joke['setup']),
            description="{}".format(joke['punchline']),
            color=0xFF5733)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="createavatar", description="Creates avatar from random characters")
    async def slash_createavatar(self, ctx: SlashContext, a=None):
        if a is None:
            await ctx.send("please enter a random text to generate your avatar")
        else:
            req = requests.get(
                f'https://robohash.org/{a}.png?set=set{random.randint(1, 3)}')
            img = req.url
            embed = discord.Embed(title="your avatar",
                                  description=f"Here is your random avatar generated by your text {a}",
                                  color=0xFF5733)
            embed.set_image(url=img)
            embed.set_footer(text="created by https://robohash.org/")
            await ctx.send(embed=embed)

    # to send avatar of the user

    @cog_ext.cog_slash(name="avatar", description="sends user avatar")
    async def slash_av(self, ctx: SlashContext, user: discord.User = None):
        if isinstance(user, commands.UserNotFound):
            await ctx.send(
                "Hmm 🤔, I had a hard time finding the user, you sure that user exits❓ it got a bit chilly right now 👻")
            return

        emb = discord.Embed(title="Avatar")

        if user is None:
            emb.set_image(url=ctx.author.avatar_url)

        else:
            emb.set_image(url=user.avatar_url)

        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

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

    async def mute_members(self, ctx, member, time, reason):
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

    @cog_ext.cog_slash(name="mute", description="Mutes member of server.")
    async def mute_command(self, ctx, member: discord.Member, time: int = None, *, reason: str = None, ):
        if reason is None:
            reason = "No reason provided."
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
            await self.unmute_members(ctx, member)

    @cog_ext.cog_slash(name="unumute", description="Helps to unmute muted members")
    async def unmute_command(self, ctx, members: discord.Member, *, reason=None):
        if reason is None:
            reason = "No reason provided."
        await self.unmute_members(ctx, members, reason=reason)

    @cog_ext.cog_slash(name="meme", description="Sends memee")
    async def slash_meme(self, ctx: SlashContext):
        req = requests.get(
            "https://meme-api.herokuapp.com/gimme/dankmemes")
        r = req.json()
        image_url = r["url"]
        title = r["title"]
        embed = discord.Embed(title=title, colour=0x009aff)
        embed.set_image(url=image_url)
        embed.set_footer(text=f"👍 :  {r['ups']}  |  NSFW: {r['nsfw']}")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(" <Slash commands loaded>")


def setup(client):
    client.add_cog(Slash(client))

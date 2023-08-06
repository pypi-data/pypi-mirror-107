# -*- coding: utf-8 -*-
"""
This module holds different command checks to add as decorator for custom commands.
Use this checks on your code like this:
    ```
    @bot.command()
    @admin_or_roles('Moderator')
    async def mute(ctx, member: discord.Member):
        ...
    ```
Or inside Cogs:
    ```
    @commands.command()
    @only_this_guild(123456789...)
    async def magic(self, ctx):
        ...
    ```
"""
from datetime import datetime, time, timezone

from discord import Member, Permissions
from discord.ext import commands
from discord.ext.commands import PrivateMessageOnly, Context
from typing import Union
from discord import utils

from dpytools.errors import Unauthorized, IncorrectGuild, NotMemberOfCorrectGuild, OutsidePermittedDatetime


def admin_or_roles(*roles: Union[int, str]) -> commands.check:
    """
    This check returns true under these conditions:
        The command is run in a guild AND:
            ctx.author has admin permissions OR has any role in :roles:

    Raises:
        TypeError if roles are not strings or ints
        ValueError if no roles are found with given parameters
        commands.NoPrivateMessage if ran from DM
        Unauthorized if user doesn't have correct roles or admin permissions
        ValueError if value passed on role_ids is not int or str
    """

    async def predicate(ctx):

        if not all(type(r) in [int, str] for r in roles):
            raise TypeError('Roles must be type int or str')

        if ctx.guild is None:
            raise commands.NoPrivateMessage()

        if ctx.author.guild_permissions.administrator is True:
            return True

        discord_roles = []
        for role in roles:
            if isinstance(role, str):
                discord_roles.append(utils.get(ctx.guild.roles, name=role))
            elif isinstance(role, int):
                discord_roles.append(ctx.guild.get_role(role))
            else:
                raise TypeError(f"int or str was expected but received {type(role)}")

        if not discord_roles:
            raise ValueError('No role in the server matched parameters')

        if any([role for role in discord_roles if role and role in ctx.author.roles]):
            return True
        else:
            raise Unauthorized("User doesn't have admin permissions or specified roles")

    return commands.check(predicate)


def only_this_guild(guild_id: int) -> commands.check:
    """This check returns true if ctx.guild has same id as param :guild_id:

    Raises:
        commands.NoPrivateMessage if ran from DM
        Custom IncorrectGuild commands.CommandError if id doesn't check

    """

    async def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage("Command was called from a direct message.")
        elif guild_id != ctx.guild.id:
            raise IncorrectGuild(f"Command was called from a guild with id different than specified in check")
        return True

    return commands.check(predicate)


def dm_from_this_guild(guild_id: int, delete: bool = False) -> commands.check:
    """
    The check returns true only if the specified :guild_id: is found within the bot's guilds.
    For this check to work the guilds and members intents must be enabled.

    Args:
        guild_id: id of the guild the author of the context must be a part of for check to return True
        delete: if True, it will try to delete ctx.message. This will only happen if the message is called
                from the specificed guild_id, if the command is called from another guild the check will
                just return False.

            Possible exceptions by discord.py library:
                commands.Forbidden – You do not have proper permissions to delete the message.
                commands.NotFound – The message was deleted already
                commands.HTTPException – Deleting the message failed.

    Returns:
        commands.check

    Raises:
        commands.PrivateMessageOnly: if called from a guild
        dpytools.errors.NotMemberOfCorrectGuild: if not a member of the specified guild
    """
    async def predicate(ctx):
        if ctx.guild and ctx.guild.id == guild_id:
            if delete is True:
                await ctx.message.delete()
            raise PrivateMessageOnly("Command was called from the guild instead of a direct message.")
        elif ctx.guild:
            return False

        guild = ctx.bot.get_guild(guild_id)

        if ctx.author in guild.members:
            return True
        else:
            raise NotMemberOfCorrectGuild("This command is unavailable to you.")

    return commands.check(predicate)


def any_of_permissions(**perms) -> commands.check:
    """
    This check returns true if ctx.author matches any permission passed in the decorator
    Use Example:
        ```
        @bot.command()
        @any_of_permissions(administrator=True, manage_guild=True, manage_messages=True)
        async def test(ctx):
            await ctx.send('success')
        ```
        The above command will send 'success' only if ctx.author has any or more
        of administrator, manage_guild or manage_messages permissions

    Args:
        perms: kwargs with the name of the permission and its expected value
    Raises:
        commands.NoPrivateMessage if ran from DM
        TypeError if passed an invalid set of permissions
    """

    async def predicate(ctx):
        if invalid := (set(perms) - set(Permissions.VALID_FLAGS)):
            raise TypeError('Invalid permission(s): %s' % (', '.join(invalid)))
        elif ctx.guild is None:
            raise commands.NoPrivateMessage("Command was called from a direct message.")

        author: Member = ctx.author
        author_perms: Permissions = author.guild_permissions
        matched = [k for k, v in perms.items() if getattr(author_perms, k) == v]
        return any(matched)

    return commands.check(predicate)


def this_or_higher_role(role: Union[str, int]) -> commands.check:
    """
    This check will return True only if ctx.author has the specified role or another hierarchically higher
    Args:
        role: The role as its name (case sensitive) or id (int).
    """
    def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage('This command can only be used in a server.')
        author: Member = ctx.author

        if type(role) not in [int, str]:
            raise TypeError('Roles must be type int or str')

        drole = utils.get(ctx.guild.roles, name=role) if isinstance(role, str) else ctx.guild.get_role(role)

        if not drole:
            raise ValueError(f'No role found within guild {ctx.guild.name} with name or id "{role}"')

        return author.top_role >= drole
    return commands.check(predicate)


def between_times(from_time: time, to_time: time) -> commands.check:
    """
    Check decorator that returns True only when the command is run in the given time interval
    Note that arguments must be datetime.time objects.
    This will be checked against the ctx.message creation time (UTC)
    Args:
        from_time: minimum time
        to_time: maximum time
    """
    def predicate(ctx: Context):
        cmd_time = ctx.message.created_at.time()
        return from_time <= cmd_time <= to_time

    return commands.check(predicate)


def between_datetimes(from_dt: datetime,
                      to_dt: datetime,
                      ) -> commands.check:
    """
    Check decorator that returns True only when the command is run in the given time interval
    Note that arguments must be datetime.time objects.
        This will be checked against the ctx.message creation datetime (UTC)

    Args:
        from_dt:
        to_dt:
    Note:
        from_dt and to_dt must be both either aware or naive. If they're aware they must share the same tz
        If params are aware then ctx.message.created_at will be converted to their timezone.
    Raises:
        Value error if the :tz: name cannot be found
    """
    def predicate(ctx: Context):
        tzs = (from_dt.tzinfo, to_dt.tzinfo)
        if any(tzs) and not all(tzs):
            raise TypeError("Either from_dt and to_dt are both aware or both naive")

        dt: datetime = ctx.message.created_at

        if all(tzs):
            if tzs[0] != tzs[1]:
                raise ValueError("When both params are aware their timezones must match.")
            else:
                tzconvert = tzs[0]
                dt = dt.replace(tzinfo=timezone.utc).astimezone(tzconvert)
        check = from_dt <= dt <= to_dt
        if check:
            return True
        else:
            raise OutsidePermittedDatetime(f"This command can only run from {from_dt.strftime('%x %X')} "
                                           f"to {to_dt.strftime('%x %X')} timezone={dt.tzname()}")

    return commands.check(predicate)


def only_these_users(*users: int) -> commands.check:
    """
    This check returns True only when ctx.author is authorized by this check
    Args:
        *users: one or more user id's
    Returns:
        commands.check
    """
    def predicate(ctx):
        return ctx.author.id in users

    return commands.check(predicate)


def in_these_channels(*channels: int) -> commands.check:
    """
    This check returns True only when ctx.channel is authorized by this check
    Args:
        *channels: one or more channel id's
    Returns:
        commands.check
    """
    def predicate(ctx):
        return ctx.channel.id in channels
    
    return commands.check(predicate)


def is_guild_owner() -> commands.check:
    """
    Returns True if ctx.author is the guild's owner

    Raises:
        commands.NoPrivateMessage if called outside a guild
        commands.Not

    Returns:
        commands.check
    """
    def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage('This command can only be used in a server.')
        author: Member = ctx.author
        if author != ctx.guild.owner.id:
            commands.MissingPermissions('This command can only be run by the owner of this guild.')
    return commands.check(predicate)











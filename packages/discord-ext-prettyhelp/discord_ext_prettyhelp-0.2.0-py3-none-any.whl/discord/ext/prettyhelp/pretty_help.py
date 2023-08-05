__all__ = ["PrettyHelp"]

from random import randint
from typing import List, Union

import discord
from discord.ext import commands
from discord.ext.commands.help import HelpCommand

from .menu import DefaultMenu


class Paginator:
    """A class that creates pages for Discord messages.

    Attributes
    -----------
    prefix: Optional[:class:`str`]
        The prefix inserted to every page. e.g. three backticks.
    suffix: Optional[:class:`str`]
        The suffix appended at the end of every page. e.g. three backticks.
    max_size: :class:`int`
        The maximum amount of codepoints allowed in a page.
    color: Optional[:class:`discord.Color`, :class: `int`]
        The color of the disord embed. Default is a random color for
        every invoke
    ending_note: Optional[:class:`str`]
        The footer in of the help embed
    """

    def __init__(self, color, pretty_help: "PrettyHelp"):
        self.pretty_help = pretty_help
        self.ending_note = None
        self.color = color
        self.char_limit = 6000
        self.field_limit = 25
        self.prefix = ""
        self.suffix = ""
        self.usage_prefix = "```"
        self.usage_suffix = "```"
        self.clear()

    def clear(self):
        """Clears the paginator to have no pages."""
        self._pages = []

    def _check_embed(self, embed: discord.Embed, *chars: str):
        """
        Check if the emebed is too big to be sent on discord

        Args:
            embed (discord.Embed): The embed to check

        Returns:
            bool: Will return True if the emebed isn't too large
        """
        check = (
            len(embed) + sum(len(char) for char in chars if char)
            < self.char_limit
            and len(embed.fields) < self.field_limit
        )
        return check

    def _new_page(self, title: str, description: str):
        """
        Create a new page

        Args:
            title (str): The title of the new page

        Returns:
            discord.Emebed: Returns an embed with the title and color set
        """
        embed = discord.Embed(
            title=title, description=description, color=self.color
        )
        self._add_page(embed)
        return embed

    def _add_page(self, page: discord.Embed):
        """
        Add a page to the paginator

        Args:
            page (discord.Embed): The page to add
        """
        page.set_footer(text=self.ending_note)
        self._pages.append(page)

    def add_cog(
        self,
        title: Union[str, commands.Cog],
        commands_list: List[commands.Command],
    ):
        """
        Add a cog page to the help menu

        Args:
            title (Union[str, commands.Cog]): The title of the embed
            commands_list (List[commands.Command]): List of commands
        """
        cog = isinstance(title, commands.Cog)
        if not commands_list:
            return

        page_title = title.qualified_name if cog else title
        embed = self._new_page(
            page_title, (title.description or "") if cog else ""
        )

        self._add_command_fields(embed, page_title, commands_list)

    def _add_command_fields(
        self,
        embed: discord.Embed,
        page_title: str,
        commands: List[commands.Command],
    ):
        """
        Adds command fields to Category/Cog and Command Group pages

        Args:
            embed (discord.Embed): The page to add command descriptions
            page_title (str): The title of the page
            commands (List[commands.Command]): The list of commands for
                the fields
        """
        for command in commands:
            if not self._check_embed(
                embed,
                self.ending_note,
                command.name,
                command.short_doc,
                self.prefix,
                self.suffix,
            ):
                embed = self._new_page(page_title, embed.description)

            embed.add_field(
                name=command.name,
                value=(
                    f'{self.prefix}{command.short_doc or "No Description"}'
                    f'{self.suffix}'
                ),
            )

    @staticmethod
    def __command_info(
        command: Union[commands.Command, commands.Group]
    ) -> str:
        info = ""
        if command.description:
            info += command.description + "\n\n"
        if command.help:
            info += command.help
        if not info:
            info = "None"
        return info

    def add_command(
        self, command: commands.Command, signature: str
    ) -> discord.Embed:
        """
        Add a command help page

        Args:
            command (commands.Command): The command to get help for
            signature (str): The command signature/usage string
        """
        page = self._new_page(
            command.qualified_name,
            f"{self.prefix}{self.__command_info(command)}{self.suffix}" or "",
        )
        if command.aliases:
            aliases = ", ".join(command.aliases)
            page.add_field(
                name=self.pretty_help.aliases_string,
                value=f"{self.prefix}{aliases}{self.suffix}",
                inline=False,
            )
        page.add_field(
            name=self.pretty_help.usage_string,
            value=f"{self.usage_prefix}{signature}{self.usage_suffix}",
            inline=False,
        )
        if self.pretty_help.show_bot_perms:
            try:
                perms = command.bot_perms
            except AttributeError:
                pass
            else:
                if perms:
                    page.add_field(
                        name=self.pretty_help.bot_perms_title,
                        value=", ".join(perms),
                        inline=False,
                    )
        if self.pretty_help.show_user_perms:
            try:
                chan_perms = command.channel_perms
                guild_perms = command.guild_perms
            except AttributeError:
                pass
            else:
                if chan_perms:
                    page.add_field(
                        name=self.pretty_help.user_channel_perms_title,
                        value=", ".join(chan_perms),
                        inline=False,
                    )
                if guild_perms:
                    page.add_field(
                        name=self.pretty_help.user_guild_perms_title,
                        value=", ".join(guild_perms),
                        inline=False,
                    )
        return page

    def add_group(
        self, group: commands.Group, commands_list: List[commands.Command]
    ):
        """
        Add a group help page

        Args:
            group (commands.Group): The command group to get help for
            commands_list (List[commands.Command]): The list of commands in
                the group
        """

        page = self.add_command(
            group, self.pretty_help.get_command_signature(group)
        )

        self._add_command_fields(page, group.name, commands_list)

    def add_index(self, include: bool, title: str, bot: commands.Bot):
        """
        Add an index page to the response of the bot_help command

        Args:
            include (bool): Include the index page or not
            title (str): The title of the index page
            bot (commands.Bot): The bot instance
        """
        if include:
            index = self._new_page(title, bot.description or "")
            self._pages.pop(-1)

            for page_no, page in enumerate(self._pages, start=1):
                index.add_field(
                    name=f"{page_no}) {page.title}",
                    value=(
                        f'{self.prefix}{page.description or "No Description"}'
                        f'{self.suffix}'
                    ),
                )
            index.set_footer(text=self.ending_note)
            self._pages.insert(0, index)
        else:
            self._pages[0].description = bot.description

    @property
    def pages(self):
        """Returns the rendered list of pages."""
        return self._pages


class PrettyHelp(HelpCommand):
    """The implementation of the prettier help command.
    A more refined help command format
    This inherits from :class:`HelpCommand`.
    It extends it with the following attributes.

    Attributes
    ------------

    color: :class: `discord.Color`
        The color to use for the help embeds. Default is a random color.
    dm_help: Optional[:class:`bool`]
        A tribool that indicates if the help command should DM the user
        instead of sending it to the channel it received it from. If the
        boolean is set to ``True``, then all help output is DM'd. If
        ``False``, none of the help output is DM'd. If ``None``, then
        the bot will only DM when the help message becomes too long
        (dictated by more than :attr:`dm_help_threshold` characters).
        Defaults to ``False``.
    menu: Optional[:class:`pretty_help.PrettyMenu`]
        The menu to use for navigating pages. Defautl is :class:`DefaultMenu`
        Custom menus should inherit from :class:`pretty_help.PrettyMenu`
    sort_commands: :class:`bool`
        Whether to sort the commands in the output alphabetically. Defaults to
        ``True``.
    show_index: class: `bool`
        A bool that indicates if the index page should be shown listing the
        available cogs. Defaults to ``True``.
    show_bot_perms: class: `bool`
        Whether or not running help <command> should show the permissions that
        the bot needs. Defaults to ``False``.
    show_user_perms: class: `bool`
        Whether or not running help <command> should show the permissions that
        the user needs. Defaults to ``False``.
    bot_perms_title: class `str`
        The string to use for the bot required permissions field. Only applies
        if show_bot_perms is set to True. Defaults to
        ``"Required Bot Permissions"``.
    user_guild_perms_title: class `str`
        The string to use for the guild-wide user required permissions field.
        Only applies if show_user_perms is set to True. Defaults to
        ``"Required User Permissions"``.
    user_channel_perms_title: class `str`
        The string to use for channel-specific user required permissions field.
        Only applies if show_user_perms is set to True. Defaults to
        ``"Required User Permissions (channel specific)"``.
    ending_note: Optional[:class:`str`]
        The footer in of the help embed
    index_title: :class: `str`
        The string used when the index page is shown. Defaults to
        ``"Categories"``
    no_category: :class:`str`
        The string used when there is a command which does not belong to
        any category(cog).
        Useful for i18n. Defaults to ``"No Category"``
    aliases_string: :class: `str`
        The string to use for the aliases field of a command. Defaults to
        ``"Aliases"``.
    usage_string: :class: `str`
        The string to use for the usage field of a command. Defaults to
        ``"Usage"``.
    """

    def __init__(self, **options):

        self.color = options.pop(
            "color",
            discord.Color.from_rgb(
                randint(0, 255), randint(0, 255), randint(0, 255)
            ),
        )
        self.dm_help = options.pop("dm_help", False)
        self.sort_commands = options.pop("sort_commands", True)
        self.show_index = options.pop("show_index", True)
        self.menu = options.pop("menu", DefaultMenu())
        self.paginator = Paginator(self.color, self)
        self.show_user_perms = options.pop("show_user_perms", False)
        self.show_bot_perms = options.pop("show_bot_perms", False)
        self.bot_perms_title = options.pop(
            "bot_perms_title", "Required Bot Permissions"
        )
        self.user_guild_perms_title = options.pop(
            "user_guild_perms_title", "Required User Permissions"
        )
        self.user_channel_perms_title = options.pop(
            "user_channel_perms_title",
            "Required User Permissions (channel specific)",
        )
        self.index_title = options.pop("index_title", "Categories")
        self.no_category = options.pop("no_category", "No Category")
        self.ending_note = options.pop("ending_note", "")
        self.usage_string = options.pop("usage_string", "Usage")
        self.aliases_string = options.pop("aliases_string", "Aliases")

        super().__init__(**options)

    async def prepare_help_command(
        self, ctx: commands.Context, command: commands.Command
    ):
        if ctx.guild is not None:
            perms = ctx.channel.permissions_for(ctx.guild.me)
            missing: List[str] = []
            if not perms.embed_links:
                missing.append("Embed Links")
            if not perms.read_message_history:
                missing.append("Read Message History")
            if not perms.add_reactions:
                missing.append("Add Reactions")
            if missing:
                raise commands.BotMissingPermissions(missing)

        self.paginator.clear()
        self.paginator.ending_note = self.get_ending_note()
        await super().prepare_help_command(ctx, command)

    def get_ending_note(self):
        """Returns help command's ending note.

        This is mainly useful to override for i18n purposes."""
        note = self.ending_note or (
            "Type {help.clean_prefix}{help.invoked_with} command for more "
            "info on a command.\nYou can also type {help.clean_prefix}"
            "{help.invoked_with} category for more info on a category."
        )
        return note.format(ctx=self.context, help=self)

    async def send_pages(self):
        pages = self.paginator.pages
        destination = self.get_destination()
        await self.menu.send_pages(self.context, destination, pages)

    def get_destination(self):
        ctx = self.context
        if self.dm_help is True:
            return ctx.author
        else:
            return ctx.channel

    async def send_bot_help(self, mapping: dict):
        bot = self.context.bot
        channel = self.get_destination()
        async with channel.typing():
            mapping = dict((name, []) for name in mapping)
            for cmd in await self.filter_commands(
                bot.commands,
                sort=self.sort_commands,
            ):
                mapping[cmd.cog].append(cmd)
            self.paginator.add_cog(self.no_category, mapping.pop(None))
            sorted_map = sorted(
                mapping.items(),
                key=lambda cg: cg[0].qualified_name
                if isinstance(cg[0], commands.Cog)
                else str(cg[0]),
            )
            for cog, command_list in sorted_map:
                self.paginator.add_cog(cog, command_list)
            self.paginator.add_index(self.show_index, self.index_title, bot)
        await self.send_pages()

    async def send_command_help(self, command: commands.Command):
        filtered = await self.filter_commands([command])
        if filtered:
            self.paginator.add_command(
                command, self.get_command_signature(command)
            )
            await self.send_pages()

    async def send_group_help(self, group: commands.Group):
        async with self.get_destination().typing():
            filtered = await self.filter_commands(
                group.commands, sort=self.sort_commands
            )
            self.paginator.add_group(group, filtered)
        await self.send_pages()

    async def send_cog_help(self, cog: commands.Cog):
        async with self.get_destination().typing():
            filtered = await self.filter_commands(
                cog.get_commands(), sort=self.sort_commands
            )
            self.paginator.add_cog(cog, filtered)
        await self.send_pages()

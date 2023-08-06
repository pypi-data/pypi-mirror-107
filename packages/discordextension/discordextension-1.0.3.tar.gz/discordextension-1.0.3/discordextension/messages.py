from discord.ext.commands import Bot, Context
from discord import Embed


async def command_list(ctx: Context, client: Bot, *, cog_or_command=None, event_cogs: list = None):
    cogs = [f'{cog}' for cog in client.cogs.keys()]
    for removable in event_cogs:
        cogs.remove(removable)
    help_embed = Embed(
        title='Help',
        color=0x018786
    )
    if cog_or_command is None:
        for cog in cogs:
            commands = ""
            for command in client.get_cog(cog).get_commands():
                help_command = f'{command.name} - {command.description}\n'
                if len(help_command) >= 60:
                    commands += f'{help_command[:57]}...\n'
                else:
                    commands += help_command
            # this version does not display the subcommands
            # if you want to display them, do this:
            # for command in client.get_cog(cog).walk_commands():
            #   ...
            help_embed.add_field(name=cog, value=str(commands), inline=False)
        help_embed.add_field(name='No Category', value='help - Shows this help\nreload - Reloads the bot\n\n'
                                                       'Type `help <cog | command>` for specificated help')
    else:
        if cog_or_command in client.cogs:
            commands = ''
            for command in client.get_cog(cog_or_command).get_commands():
                commands += f'`{command.name}` - {command.description}\n'
            help_embed.add_field(name=cog_or_command, value=commands)
        elif command := client.get_command(cog_or_command):
            command = f'`{command.name}` - {command.description}'
            help_embed.add_field(name=cog_or_command.capitalize(), value=command)
        else:
            help_embed.add_field(name='Error', value='This is not a category or a command')
    help_embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=help_embed)

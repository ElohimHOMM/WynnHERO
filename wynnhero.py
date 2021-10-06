from discord_components import ComponentsBot
import discord
import requests

import profilebuilder
import management

intents = discord.Intents.default()
intents.members = True

# bot = commands.Bot(command_prefix='w>')
bot = ComponentsBot(command_prefix='w>')

@bot.event
async def on_ready():
    management.readyDataSetup()
    print(f'Logged in as {bot.user}!')

@bot.command(brief = 'Shuts the bot down', description = 'Shuts the bot down')
async def bye(ctx):
    if ctx.message.author.id != 146325558584803328:
        return
    await ctx.send('Shutting down.')
    print('Bot shutting down')
    await bot.close()

class Wynncraft:
    """Category for Wynncraft Profile Management"""

@bot.command(brief = 'Links Discord and Minecraft', description = 'Links the two accounts.\nname: Name of the Minecraft Account you want to link')
async def connect(ctx, name = ''):
    if name == '':
        await ctx.send('Syntax: connect [name]')
        return
    sdata = management.load_dict()
    uid = str(ctx.message.author.id)
    if uid in sdata:
        await ctx.send(f'You\'re already connected to Minecraft Account {sdata[uid]}.')
    else:
        sdata[uid] = name
        management.save_dict(sdata)
        print(f'Associated \"{name}\" to \"{name}\".')
        await ctx.send('Associated you to Minecraft Account ' + name + '.')

@bot.command(brief = 'Unlink Discord and Minecraft', description = 'Unlinks the linked accounts.')
async def disconnect(ctx):
    uid = str(ctx.message.author.id)
    sdata = management.load_dict()
    if uid in sdata == False:
        await ctx.send('Your Discord Account is not linked to a Minecraft Account.')
        return
    else:
        name = sdata[uid]
        del sdata[uid]
        management.save_dict(sdata)
        print(f'Disassociated \"{name}\" from \"{uid}\".')
        await ctx.send('Disassociated you with Minecraft Account ' + name + '.')

@bot.command(brief = 'Shows selected Wynncraft Profile', description = 'Shows an embed with information about the user and his played classes.\nname: Optional! Name of the profile you want to view. Will show your linked account if empty.')
async def profile(ctx, name = ''):
    uid = str(ctx.message.author.id)
    if name == '':
        sdata = management.load_dict()
        if uid in sdata:
            name = sdata[uid]
        else:
            await ctx.send('Syntax: profile [name]')
            return
    response = requests.get(f'https://api.wynncraft.com/v2/player/{name}/stats').json()
    await ctx.send(embed = profilebuilder.buildProfile(response), components = profilebuilder.buildComponents(response), delete_after=60.0)

@bot.event
async def on_select_option(interaction):
#interaction: client, user, component, custom_id, values (id der selection), component_type, message, guild, channel, interaction_id, interaction_token, responded?, deferred?
    name = interaction.message.components[0].components[0].options[0].value
    classCounter = int(interaction.values[0])
    response = requests.get(f'https://api.wynncraft.com/v2/player/{name}/stats').json()
    await interaction.message.edit(embed = profilebuilder.buildClass(response, classCounter), components = profilebuilder.buildComponents(response))
    

bot.run('ODQ0NTEyNzM3NjEwNTYzNTk1.YKTfxg.oiIMgMItG44ZYmrtqc1W2ZW_AKY')
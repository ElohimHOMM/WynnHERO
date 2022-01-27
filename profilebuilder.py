from discord_components import Select, SelectOption
import discord
import datetime


def build_profile(res):
    current = res['data'][0]
    ret = discord.Embed(title='Stats for ' + current['username'])
    ret.color = discord.Color.dark_green()
    ret.timestamp = datetime.datetime.now()
    name = current['username']
    ret.url = f'https://wynncraft.com/stats/player/{name}'
    ret.set_thumbnail(url='https://cdn.wynncraft.com/img/wynn.png')
    
    # set content
    ret.add_field(name='Status', value=get_status(current['meta']['location']), inline=True)
    ret.add_field(name='Playtime', value=str(current['meta']['playtime']) + 'min?', inline=True)  # playtime kommt von der API falsch zurück
    rank = current['meta']['tag']['value']
    ret.add_field(name='Rank', value='No Rank' if rank is None else rank, inline=True)
    # new line
    ret.add_field(name='Classes', value=len(current['classes']), inline=True)
    ret.add_field(name='test', value='Something', inline=True)
    ret.add_field(name='test', value='Something', inline=True)

    return ret


def build_class(res, c_id):
    current = res['data'][0]['classes'][c_id]
    level = current['level']
    name = current['name']
    ret = discord.Embed(title=f'Level {level} {name}')
    username = res['data'][0]['username']
    ret.url = f'https://wynncraft.com/stats/player/{username}'
    ret.color = discord.Color.dark_green()
    ret.timestamp = datetime.datetime.now()
    ret.set_thumbnail(url=get_thumbnail(name))

    professions = current['professions']

    # set content
    ret.add_field(name='Class', value=name, inline=True)
    ret.add_field(name='Level', value=level, inline=True)
    ret.add_field(name='Combat Level', value=professions['combat']['level'], inline=True)

    ret = post_professions(ret, professions)

    return ret


def get_status(current):
    ret = 'offline' if current['online'] is False else 'online - ' + current['server']
    return ret


def build_components(res):
    option_list = list
    option_list.append(SelectOption(label='Profile', value=res['data'][0]['username']))
    counter = 0
    for i in res['data'][0]['classes']:
        option_list.append(get_option(i, counter))
        counter = counter + 1
    return [Select(id='class-select', options=option_list, )]


def get_option(class_object, counter):
    identifier = counter
    text = 'Lv. ' + str(class_object['level']) + ' ' + str(class_object['name'])
    return SelectOption(label=text, value=identifier)


def post_professions(ret, professions):
    ret.add_field(name='Crafting Professions', value='\u200b', inline=False)

    ret.add_field(name='Alchemism', value=professions['alchemism']['level'], inline=True)
    ret.add_field(name='Armouring', value=professions['armouring']['level'], inline=True)
    ret.add_field(name='Cooking', value=professions['cooking']['level'], inline=True)
    ret.add_field(name='Jeweling', value=professions['jeweling']['level'], inline=True)
    ret.add_field(name='Scribing', value=professions['scribing']['level'], inline=True)
    ret.add_field(name='Tailoring', value=professions['tailoring']['level'], inline=True)
    ret.add_field(name='Weaponsmithing', value=professions['weaponsmithing']['level'], inline=True)
    ret.add_field(name='Woodworking', value=professions['woodworking']['level'], inline=True)

    ret.add_field(name='Gathering Professions', value='\u200b', inline=False)

    ret.add_field(name='Farming', value=professions['farming']['level'], inline=True)
    ret.add_field(name='Fishing', value=professions['fishing']['level'], inline=True)
    ret.add_field(name='Mining', value=professions['mining']['level'], inline=True)
    ret.add_field(name='Woodcutting', value=professions['woodcutting']['level'], inline=True)
    return ret


def get_thumbnail(class_name):
    if class_name == 'mage' or class_name == 'darkwizard':
        return 'https://cdn.wynncraft.com/img/stats/classes/mage.png'
    elif class_name == 'archer' or class_name == 'hunter':
        return 'https://cdn.wynncraft.com/img/stats/classes/archer.png'
    elif class_name == 'warrior' or class_name == 'knight':
        return 'https://cdn.wynncraft.com/img/stats/classes/warrior.png'
    elif class_name == 'assassin' or class_name == 'ninja':
        return 'https://cdn.wynncraft.com/img/stats/classes/assassin.png'
    elif class_name == 'shaman' or class_name == 'skyseer':
        return 'https://cdn.wynncraft.com/img/stats/classes/shaman.png'
    else:
        return ''

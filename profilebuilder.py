from discord_components import Select, SelectOption
import discord
import datetime

def buildProfile(res):
    current = res['data'][0]
    ret = discord.Embed(title = 'Stats for ' + current['username'])
    ret.color = discord.Color.dark_green()
    ret.timestamp = datetime.datetime.now()
    name = current['username']
    ret.url = f'https://wynncraft.com/stats/player/{name}'
    ret.set_thumbnail(url = 'https://cdn.wynncraft.com/img/wynn.png')
    
    # set content
    ret.add_field(name = 'Status', value = getStatus(current['meta']['location']), inline = True)
    ret.add_field(name = 'Playtime', value = str(current['meta']['playtime']) + 'min?', inline = True) # playtime kommt von der API falsch zurück
    rank = current['meta']['tag']['value']
    ret.add_field(name = 'Rank', value = 'No Rank' if rank is None else rank, inline = True) 
    # new line
    ret.add_field(name = 'Classes', value = len(current['classes']), inline = True)
    ret.add_field(name = 'test', value = 'Something', inline = True)
    ret.add_field(name = 'test', value = 'Something', inline = True)

    return ret

def buildClass(res, id):
    current = res['data'][0]['classes'][id]
    level = current['level']
    name = current['name']
    ret = discord.Embed(title = f'Level {level} {name}')
    username = res['data'][0]['username']
    ret.url = f'https://wynncraft.com/stats/player/{username}'
    ret.color = discord.Color.dark_green()
    ret.timestamp = datetime.datetime.now()
    ret.set_thumbnail(url = getThumbnail(name))

    professions = current['professions']

    # set content
    ret.add_field(name = 'Class', value = name, inline = True)
    ret.add_field(name = 'Level', value = level, inline = True)
    ret.add_field(name = 'Combat Level', value = professions['combat']['level'], inline = True) 

    ret = postProfessions(ret, professions)

    return ret

def getStatus(current):
    ret = 'offline' if current['online'] == False else 'online - ' + current['server']
    return ret

def buildComponents(res):
    optionList = []
    optionList.append(SelectOption(label = 'Profile', value = res['data'][0]['username']))
    counter = 0
    for i in res['data'][0]['classes']:
        optionList.append(getOption(i, counter))
        counter = counter + 1
    return [Select(id = 'class-select', options = optionList, )]

def getOption(classObject, counter):
    identifier = counter
    text = 'Lv. ' + str(classObject['level']) + ' ' + str(classObject['name'])
    return SelectOption(label = text, value = identifier)

def postProfessions(ret, professions):
    ret.add_field(name = 'Crafting Professions', value = '\u200b', inline = False) 

    ret.add_field(name = 'Alchemism', value = professions['alchemism']['level'], inline = True)
    ret.add_field(name = 'Armouring', value = professions['armouring']['level'], inline = True)
    ret.add_field(name = 'Cooking', value = professions['cooking']['level'], inline = True) 
    ret.add_field(name = 'Jeweling', value = professions['jeweling']['level'], inline = True)
    ret.add_field(name = 'Scribing', value = professions['scribing']['level'], inline = True)
    ret.add_field(name = 'Tailoring', value = professions['tailoring']['level'], inline = True) 
    ret.add_field(name = 'Weaponsmithing', value = professions['weaponsmithing']['level'], inline = True)
    ret.add_field(name = 'Woodworking', value = professions['woodworking']['level'], inline = True)

    ret.add_field(name = 'Gathering Professions', value = '\u200b', inline = False) 

    ret.add_field(name = 'Farming', value = professions['farming']['level'], inline = True) 
    ret.add_field(name = 'Fishing', value = professions['fishing']['level'], inline = True)
    ret.add_field(name = 'Mining', value = professions['mining']['level'], inline = True)
    ret.add_field(name = 'Woodcutting', value = professions['woodcutting']['level'], inline = True) 
    return ret

def getThumbnail(className):
    if className == 'mage' or className == 'darkwizard':
        return 'https://cdn.wynncraft.com/img/stats/classes/mage.png'
    elif className == 'archer' or className == 'hunter':
        return 'https://cdn.wynncraft.com/img/stats/classes/archer.png'
    elif className == 'warrior' or className == 'knight':
        return 'https://cdn.wynncraft.com/img/stats/classes/warrior.png'
    elif className == 'assassin' or className == 'ninja':
        return 'https://cdn.wynncraft.com/img/stats/classes/assassin.png'
    elif className == 'shaman' or className == 'skyseer':
        return 'https://cdn.wynncraft.com/img/stats/classes/shaman.png'
    else:
        return ''

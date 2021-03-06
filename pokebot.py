# -*- coding: utf-8 -*-
import random
import asyncio
import discord
import logging
import math
import json
import sqlite3
import os

from discord.ext import commands
from pokemans import pokemans, legendaries, base_stats, cp_multipliers, pokejson
from shutil import copyfile

client = discord.Client()

# If .db file not there
if not os.path.isfile('./pokemon.db'):
        print('DB file not detected, copying empty.')
        copyfile('./pokemon.emptydb', './pokemon.db')

# Init DB
db = sqlite3.connect('pokemon.db')
cursor = db.cursor()

# Method to calculate CP.
def calculate_cp(pokemon, level, iv_attack, iv_defense, iv_stamina):
    stats = base_stats[str(pokemon)]
    cpm = cp_multipliers[str(level)]

    return math.floor(
        (cpm * cpm *
         (stats['attack'] + iv_attack)
         * math.sqrt((stats['defense'] + iv_defense))
         * math.sqrt((stats['stamina'] + iv_stamina))) / 10)

def find_pokemon_id(name):
    if name == 'Nidoran-F':
        return 29
    elif name == 'Nidoran-M':
        return 32
    elif name == 'Mr-Mime':
        return 122
    elif name == 'Ho-Oh':
        return 250
    elif name == 'Mime-Jr':
        return 439
    else:
        name = name.split('-')[0]
        for k in pokejson.keys():
            v = pokejson[k]
            if v == name:
                return int(k)

        return 0


def store_pokemon(params):
    pokemon, type, level, cp, iv, attack, defense, hp, owner = params
    query = 'INSERT INTO pokemon(`pokemon`, `type`, `level`, `cp`, `iv`, `attack`, `defense`, `hp`, `owner`) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cursor.execute(query, (pokemon, type, level, cp, iv, attack, defense, hp, owner))
    db.commit()

@client.event
async def on_ready():
    print("Connected!")
    print("Logged in as: " + client.user.name)
    print("User ID:" + client.user.id)
    print("_________________")
    await client.change_presence(game=discord.Game(name="spawning pokemon!"))


logging.basicConfig(level=logging.ERROR)

#set prefix
bot = commands.Bot(command_prefix='$')

async def on_message(message):
    if message.author == client.user:
        return

@client.event
async def on_message(message):
    if message.content.startswith('$100'):
        if random.randint(1,300) <= 299:
            hundochoice = (random.choice(pokemans))
        else:
            hundochoice = random.choice(legendaries)
        if message.author == client.user:
            return
        hp = random.randint(0, 15)
        attack = random.randint(0, 15)
        defense = random.randint(0, 15)
        IV = ((attack + defense + hp) / 45) * 100
        roll_count = 0
        end_goal = 100.0
        while IV != end_goal:
            if random.randint(1, 300) <= 299:
                hundochoice = (random.choice(pokemans))
            else:
                hundochoice = random.choice(legendaries)
            end_goal = 100.0
            attack = random.randint(0, 15)
            defense = random.randint(0, 15)
            hp = random.randint(0, 15)
            IV = ((attack + defense + hp) / 45) * 100
            roll_count += 1
        async def hundo_poke():
            hundo_poke = discord.Embed(
                title="You rolled a hundo!",
                description="User: " + str(message.author.name) + "\n\nEncounters before 100% encounter:\n```" + str(roll_count) + '```Pokemon rolled: ```' + str(hundochoice) +
                            '``` IV: 100% (15/15/15)', color=3447003)
            hundo_poke.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(hundochoice).lower() + ".gif")
            await client.send_message(message.channel, embed=hundo_poke)
        async def shiny_hundo():
            shiny_hundo = discord.Embed(
                title="You rolled a SHINY hundo!",
                description="User: " + str(message.author.name) + "\n\nEncounters before 100% encounter:\n```" + str(roll_count) + '```Shiny pokemon rolled: ```' + str(hundochoice) +
                            '``` IV: 100% (15/15/15)', color=3447003)
            shiny_hundo.set_image(url="http://www.pokestadium.com/sprites/xy/shiny/" + str(hundochoice).lower() + ".gif")
            await client.send_message(message.channel, embed=shiny_hundo)
        if random.randint(1,300) <= 290:
            await hundo_poke()
        else:
            await shiny_hundo()
    if random.randint(0,200) <= 3 or message.content.startswith('$search'):
        async def on_message(message):
            if message.author == client.user:
                return
        pokechoice = (random.choice(pokemans))
        pokeid = find_pokemon_id(pokechoice)
        level = random.randint(1, 30)
        if message.author == client.user:
            return
        attack = random.randint(0, 15)
        defense = random.randint(0, 15)
        hp = random.randint(0, 15)
        IV = (((attack + defense + hp) / 45) * 100)
        throw_rate = random.randint(1, 100)
        highiv = "Wow, your pokemon has great IV's! It's a keeper!"
        cp = calculate_cp(pokeid, level, attack, defense, hp)
        type = 'Normal'
        if random.randint(1,200) < 197:
            def log_fled():
                print(str(message.author) + ' had a ' + str(round(IV,1)) + '% ' + str(pokechoice) + ' run away from them!')
            def log_caught():
                print(str(message.author) + ' caught a ' + str(round(IV,1)) + '% ' + str(pokechoice) + '!')
            async def spawn_pokes():
                embed_spawn = discord.Embed(
                    title="A wild " + str(pokechoice) + " has appeared!",
                    description="CP: " + str(cp) + "\nTo catch the wild pokemon, type $throw", color = 3447003)
                embed_spawn.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(pokechoice).lower() + ".gif")
                await client.send_message(message.channel, embed=embed_spawn)
            await spawn_pokes()
            if client.wait_for_message(author=None, content="$throw"):
                def throw_check(msg):
                    return msg.content.startswith("$throw")
                message = await client.wait_for_message(author=None, check=throw_check)
                async def normal_caught():
                    embed_normal_caught = discord.Embed(
                        title= message.author.name + " caught the wild " + str(pokechoice) + "!",
                        description="Name: " + str(pokechoice) + ".\nLevel: "+ str(level) + "\nCP: " + str(cp) + "\nIV: " + str(round(IV, 1)) + "% (" + str(attack) + "/" + str(defense) + "/" + str(hp) + ")", color=0x20ef25)
                    embed_normal_caught.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(pokechoice).lower() + ".gif")
                    await client.send_message(message.channel, embed=embed_normal_caught)
                async def normal_fled():
                    embed_normal_fled = discord.Embed(
                        title= "The wild " + str(pokechoice) + " has fled!",
                        description=message.author.name + " tried to catch the wild " + str(pokechoice) + ", but it has ran away!", color=0xef101e)
                    embed_normal_fled.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(pokechoice).lower() + ".gif")
                    await client.send_message(message.channel, embed=embed_normal_fled)
                if throw_rate <= 30:
                    print('excellent throw triggered for ' + str(message.author))
                    throwing_pokeball = await client.send_message(message.channel, "throwing pokéball...")
                    await asyncio.sleep(1)
                    await client.delete_message(throwing_pokeball)
                    excellent_throw = await client.send_message(message.channel, "excellent throw!")
                    await asyncio.sleep(1)
                    await client.delete_message(excellent_throw)
                    shake1 = await client.send_file(message.channel, "images/shake.png")
                    await asyncio.sleep(1)
                    if random.randint(1, 100) < 2:
                        await client.delete_message(shake1)
                        await normal_fled()
                        log_fled()
                    else:
                        await client.delete_message(shake1)
                        shake2 = await client.send_file(message.channel, "images/shake2.png")
                        await asyncio.sleep(1)
                        if random.randint(1, 100) < 2:
                            await client.delete_message(shake2)
                            await normal_fled()
                            log_fled()
                        else:
                            await client.delete_message(shake2)
                            shake3 = await client.send_file(message.channel, "images/shake.png")
                            await asyncio.sleep(1)
                            await client.delete_message(shake3)
                            await normal_caught()
                            log_caught()
                            owner = message.author.id
                            params = (pokechoice, type, level, cp, IV, attack, defense, hp, owner)
                            store_pokemon(params)
                            if IV > 90:
                                await client.send_message(message.channel, highiv)
                elif 31 <= throw_rate <= 75:
                    print('great throw triggered for ' + str(message.author))
                    throwing_pokeball = await client.send_message(message.channel, "throwing pokéball...")
                    await asyncio.sleep(1)
                    await client.delete_message(throwing_pokeball)
                    great_throw = await client.send_message(message.channel, "great throw!")
                    await asyncio.sleep(1)
                    await client.delete_message(great_throw)
                    shake1 = await client.send_file(message.channel, "images/shake.png")
                    await asyncio.sleep(1)
                    if random.randint(1, 100) < 5:
                        await client.delete_message(shake1)
                        await normal_fled()
                        log_fled()
                    else:
                        await client.delete_message(shake1)
                        shake2 = await client.send_file(message.channel, "images/shake2.png")
                        await asyncio.sleep(1)
                        if random.randint(1, 100) < 3:
                            await client.delete_message(shake2)
                            await normal_fled()
                            log_fled()
                        else:
                            await client.delete_message(shake2)
                            shake3 = await client.send_file(message.channel, "images/shake.png")
                            await asyncio.sleep(1)
                            await client.delete_message(shake3)
                            await normal_caught()
                            log_caught()
                            owner = message.author.id
                            params = (pokechoice, type, level, cp, IV, attack, defense, hp, owner)
                            store_pokemon(params)
                            if IV > 90:
                                await client.send_message(message.channel, highiv)
                elif throw_rate >= 76:
                    print('nice throw triggered for ' + str(message.author))
                    throwing_pokeball = await client.send_message(message.channel, "throwing pokéball...")
                    await asyncio.sleep(1)
                    await client.delete_message(throwing_pokeball)
                    nice_throw = await client.send_message(message.channel, "nice throw!")
                    await asyncio.sleep(1)
                    await client.delete_message(nice_throw)
                    shake1 = await client.send_file(message.channel, "images/shake.png")
                    await asyncio.sleep(1)
                    if random.randint(1, 100) < 6:
                        await client.delete_message(shake1)
                        await normal_fled()
                        log_fled()
                    else:
                        await client.delete_message(shake1)
                        shake2 = await client.send_file(message.channel, "images/shake2.png")
                        await asyncio.sleep(1)
                        if random.randint(1, 100) < 4:
                            await client.delete_message(shake2)
                            await normal_fled()
                            log_fled()
                        else:
                            await client.delete_message(shake2)
                            shake3 = await client.send_file(message.channel, "images/shake.png")
                            await asyncio.sleep(1)
                            await client.delete_message(shake3)
                            await normal_caught()
                            log_caught()
                            owner = message.author.id
                            params = (pokechoice, type, level, cp, IV, attack, defense, hp, owner)
                            store_pokemon(params)
                            if IV > 90:
                                await client.send_message(message.channel, highiv)
        else:
            async def spawn_shiny_pokes():
                embed_shiny_spawn = discord.Embed(
                    title="A shiny " + str(pokechoice) + " has appeared!",
                    description="CP: " + str(cp) + "\nTo catch the wild pokemon, type $throw", color = 3447003)
                embed_shiny_spawn.set_image(url="http://www.pokestadium.com/sprites/xy/shiny/" + str(pokechoice).lower() + ".gif")
                await client.send_message(message.channel, embed=embed_shiny_spawn)
            await spawn_shiny_pokes()
            if client.wait_for_message(author=None, content="$throw"):
                def throw_check(msg):
                    return msg.content.startswith("$throw")
                message = await client.wait_for_message(author=None, check=throw_check)
                attack = random.randint(0, 15)
                defense = random.randint(0, 15)
                hp = random.randint(0, 15)
                IV = (((attack + defense + hp) / 45) * 100)
                throw_rate = random.randint(1, 100)
                highiv = "Wow, your shiny pokemon has great IV's! It's a keeper!"
                cp = calculate_cp(pokeid, level, attack, defense, hp)
                async def shiny_caught():
                    embed_shiny_caught = discord.Embed(
                        title= message.author.name + " caught the shiny " + str(pokechoice) + "!",
                        description="Name: Shiny " + str(pokechoice) + ".\nLevel: " + str(level) + "\nCP: " + str(cp) + "\nIV: " + str(round(IV, 1)) + "% (" + str(attack) + "/" + str(defense) + "/" + str(hp) + ")", color=0x20ef25)
                    embed_shiny_caught.set_image(url="http://www.pokestadium.com/sprites/xy/shiny/" + str(pokechoice).lower() + ".gif")
                    await client.send_message(message.channel, embed=embed_shiny_caught)
                async def shiny_fled():
                    embed_shiny_fled = discord.Embed(
                        title= "The shiny " + str(pokechoice) + " has fled!",
                        description=message.author.name + " tried to catch the shiny " + str(pokechoice) + ", but it has ran away!", color=0xef101e)
                    embed_shiny_fled.set_image(url="http://www.pokestadium.com/sprites/xy/shiny/" + str(pokechoice).lower() + ".gif")
                    await client.send_message(message.channel, embed=embed_shiny_fled)
                if throw_rate <= 30:
                    print('excellent throw triggered for ' + str(message.author))
                    throwing_pokeball = await client.send_message(message.channel, "throwing pokéball...")
                    await asyncio.sleep(1)
                    await client.delete_message(throwing_pokeball)
                    excellent_throw = await client.send_message(message.channel, "excellent throw!")
                    await asyncio.sleep(1)
                    await client.delete_message(excellent_throw)
                    shake1 = await client.send_file(message.channel, "images/shake.png")
                    await asyncio.sleep(1)
                    if random.randint(1, 100) < 2:
                        await client.delete_message(shake1)
                        await shiny_fled()
                        log_fled()
                    else:
                        await client.delete_message(shake1)
                        shake2 = await client.send_file(message.channel, "images/shake2.png")
                        await asyncio.sleep(1)
                        if random.randint(1, 100) < 2:
                            await client.delete_message(shake2)
                            await shiny_fled()
                            log_fled()
                        else:
                            await client.delete_message(shake2)
                            shake3 = await client.send_file(message.channel, "images/shake.png")
                            await asyncio.sleep(1)
                            await client.delete_message(shake3)
                            await shiny_caught()
                            log_caught()
                            owner = message.author.id
                            params = (pokechoice, type, level, cp, IV, attack, defense, hp, owner)
                            store_pokemon(params)
                            if IV > 90:
                                await client.send_message(message.channel, highiv)
                elif 31 <= throw_rate <= 75:
                    print('great throw triggered for ' + str(message.author))
                    throwing_pokeball = await client.send_message(message.channel, "throwing pokéball...")
                    await asyncio.sleep(1)
                    await client.delete_message(throwing_pokeball)
                    great_throw = await client.send_message(message.channel, "great throw!")
                    await asyncio.sleep(1)
                    await client.delete_message(great_throw)
                    shake1 = await client.send_file(message.channel, "images/shake.png")
                    await asyncio.sleep(1)
                    if random.randint(1, 100) < 5:
                        await client.delete_message(shake1)
                        await shiny_fled()
                        log_fled()
                    else:
                        await client.delete_message(shake1)
                        shake2 = await client.send_file(message.channel, "images/shake2.png")
                        await asyncio.sleep(1)
                        if random.randint(1, 100) < 3:
                            await client.delete_message(shake2)
                            await shiny_fled()
                            log_fled()
                        else:
                            await client.delete_message(shake2)
                            shake3 = await client.send_file(message.channel, "images/shake.png")
                            await asyncio.sleep(1)
                            await client.delete_message(shake3)
                            await shiny_caught()
                            log_caught()
                            owner = message.author.id
                            params = (pokechoice, type, level, cp, IV, attack, defense, hp, owner)
                            store_pokemon(params)
                            if IV > 90:
                                await client.send_message(message.channel, highiv)
                elif throw_rate >= 76:
                    print('nice throw triggered for ' + str(message.author))
                    throwing_pokeball = await client.send_message(message.channel, "throwing pokéball...")
                    await asyncio.sleep(1)
                    await client.delete_message(throwing_pokeball)
                    nice_throw = await client.send_message(message.channel, "nice throw!")
                    await asyncio.sleep(1)
                    await client.delete_message(nice_throw)
                    shake1 = await client.send_file(message.channel, "images/shake.png")
                    await asyncio.sleep(1)
                    if random.randint(1, 100) < 6:
                        await client.delete_message(shake1)
                        await shiny_fled()
                        log_fled()
                    else:
                        await client.delete_message(shake1)
                        shake2 = await client.send_file(message.channel, "images/shake2.png")
                        await asyncio.sleep(1)
                        if random.randint(1, 100) < 4:
                            await client.delete_message(shake2)
                            await shiny_fled()
                            log_fled()
                        else:
                            await client.delete_message(shake2)
                            shake3 = await client.send_file(message.channel, "images/shake.png")
                            await asyncio.sleep(1)
                            await client.delete_message(shake3)
                            await shiny_caught()
                            log_caught()
                            owner = message.author.id
                            params = (pokechoice, type, level, cp, IV, attack, defense, hp, owner)
                            store_pokemon(params)
                            if IV > 90:
                                await client.send_message(message.channel, highiv)
    if message.content.startswith("$hatch"):
        print(str(message.author.name) + ' began to hatch a Pokemon')
        pokehatch = (random.choice(pokemans))
        # print(pokehatch) Debug
        pokeid = find_pokemon_id(pokehatch)
        # print(pokeid) Debug
        hatch_attack = random.randint(10, 15)
        hatch_defense = random.randint(10, 15)
        hatch_hp = random.randint(10, 15)
        hatch_IV = (((hatch_attack + hatch_defense + hatch_hp) / 45) * 100)
        hatch_level = 20
        hatch_cp = calculate_cp(pokeid, hatch_level, hatch_attack, hatch_defense, hatch_hp)
        async def hatch_pokes():
            embed_hatch = discord.Embed(
                title= message.author.name + " has hatched a " + str(pokehatch) + "!",
                description="Name: " + str(pokehatch) + ".\nLevel: " + str(hatch_level) + "\nCP: " + str(hatch_cp) + "\nIV: " + str(round(hatch_IV, 1)) + "% (" + str(hatch_attack) + "/" + str(hatch_defense) + "/" + str(hatch_hp) + ")",color=0x20ef25)
            embed_hatch.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(pokehatch).lower() + ".gif")
            await client.send_message(message.channel, embed=embed_hatch)
        async def hatch_shiny():
            embed_shiny_hatch = discord.Embed(
                title= message.author.name + " has hatched a shiny " + str(pokehatch) + "!",
                description="Name: Shiny " + str(pokehatch) + ".\nLevel: " + str(hatch_level) + "\nCP: " + str(hatch_cp) + "\nIV: " + str(round(hatch_IV, 1)) + "% (" + str(hatch_attack) + "/" + str(hatch_defense) + "/" + str(hatch_hp) + ")", color=0x20ef25)
            embed_shiny_hatch.set_image(url="http://www.pokestadium.com/sprites/xy/shiny/" + str(pokehatch).lower() + ".gif")
            await client.send_message(message.channel, embed=embed_shiny_hatch)
        hatch = message.author.mention + " has hatched a " + str(pokehatch) + "!\nYour " + str(pokehatch) + " has an IV of " + str(round(hatch_IV, 2)) + "% and is level " + str(hatch_level) + "!\nCP: " + str(hatch_cp) + "\nIndividual Values:\nAttack: " + str(hatch_attack) + "\nDefense: " + str(hatch_defense) + "\nHP: " + str(hatch_hp)
        await client.send_message(message.channel, message.author.name + " incubated an egg....")
        await asyncio.sleep(0.75)
        await client.send_message(message.channel, "oh?")
        await asyncio.sleep(0.75)
        if message.content.startswith("$hatch"):
            await client.send_file(message.channel, "images/egg.png")
            await asyncio.sleep(0.75)
            if random.randint(1,100) < 1:
                await client.send_message(message.channel, message.author.mention + " has a bad egg\nStats: ???")
                await asyncio.sleep(0.5)
                await client.send_message(message.channel, "To hatch another pokemon, type `$hatch`")
                await asyncio.sleep(0.5)
            else:
                await client.send_message(message.channel, "*....*")
                await asyncio.sleep(0.75)
                if random.randint(1,100) < 1:
                    await client.send_message(message.channel, message.author.mention + " has a bad egg\nStats: ???")
                    await asyncio.sleep(0.5)
                    await client.send_message(message.channel, "To hatch another pokemon, type `$hatch`")
                    await asyncio.sleep(0.5)
                else:
                    await client.send_message(message.channel, "*....*")
                    await asyncio.sleep(0.75)
                    if random.randint(1,100) <= 97:
                        await hatch_pokes()
                        print(str(message.author.name) + ' hatched a ' + str(pokehatch))
                        await asyncio.sleep(0.5)
                        await client.send_message(message.channel, "To hatch another pokemon, type `$hatch`")
                        await asyncio.sleep(0.5)
                    else:
                        await hatch_shiny()
                        print(str(message.author.name) + ' hatched a shiny ' + str(pokehatch))
                        await asyncio.sleep(0.5)
                        await client.send_message(message.channel, "To hatch another pokemon, type `$hatch`")
                        await asyncio.sleep(0.5)
    if message.content.startswith("$raid"):
        def raid_boss_cp(id, level=5):
            hp = 12500
            if level == 1:
                hp = 600
            elif level == 2:
                hp = 1800
            elif level == 3:
                hp = 3000
            elif level == 4:
                hp = 7500
            stats = base_stats[str(id)]
            # =FLOOR(((B9 + 15) * sqrt(C9 + 15) * sqrt(600)) / 10)
            return math.floor(((stats['attack'] + 15) * math.sqrt(stats['defense'] + 15) * math.sqrt(hp)) / 10)
        leg_choice = random.choice(legendaries)
        leg_id = find_pokemon_id(leg_choice)
        health = 500
        shiny_or_not = random.randint(1,100)
        damage = health - random.randint(125, 145)
        damage2 = damage - random.randint(125, 200)
        damage3 = damage2 - random.randint(125, 130)
        damage4 = damage3 - random.randint(125, 170)
        damage5 = damage4 - random.randint(100, 180)
        damage6 = damage5 - random.randint(90, 150)
        damage7 = damage6 - random.randint(70, 100)
        leg_attack = random.randint(10, 15)
        leg_defense = random.randint(10, 15)
        leg_hp = random.randint(10, 15)
        leg_iv = (((leg_attack + leg_defense + leg_hp) / 45) * 100)
        leg_level = 20
        leg_cp = calculate_cp(leg_id, leg_level, leg_attack, leg_defense, leg_hp)
        leg_highiv = "Wow, your legendary has great IV's! It's a keeper!"
        async def legendary_caught():
            embed_legendary_caught = discord.Embed(
                title= message.author.name + " has caught the legendary " + str(leg_choice) + "!",
                description="Your " + str(leg_choice) + " has an IV of " + str(round(leg_iv, 2)) + "% and is level " + str(leg_level) + "!\nCP: " + str(leg_cp) + "\nIndividual Values:\nAttack: " + str(leg_attack) + "\nDefense: " + str(leg_defense) + "\nHP: " + str(leg_hp), color=0x20ef25)
            embed_legendary_caught.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(leg_choice).lower() + ".gif")
            await client.send_message(message.channel, embed=embed_legendary_caught)
        async def legendary_fled():
            embed_legendary_fled = discord.Embed(
                title= "The " + str(leg_choice) + " escaped!",
                description=message.author.name + " battled hard, but could not catch the legendary pokemon!", color=0xef101e)
            embed_legendary_fled.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(leg_choice).lower() + ".gif")
            await client.send_message(message.channel, embed=embed_legendary_fled)
        async def legendary_shiny_caught():
            embed_legendary_shiny_caught = discord.Embed(
                title= message.author.name + " has caught the shiny " + str(leg_choice) + "!",
                description="Your " + str(leg_choice) + " has an IV of " + str(round(leg_iv, 2)) + "% and is level " + str(leg_level) + "!\nCP: " + str(leg_cp) + "\nIndividual Values:\nAttack: " + str(leg_attack) + "\nDefense: " + str(leg_defense) + "\nHP: " + str(leg_hp), color=0x20ef25)
            embed_legendary_shiny_caught.set_image(url="http://www.pokestadium.com/sprites/xy/shiny/" + str(leg_choice).lower() + ".gif")
            await client.send_message(message.channel, embed=embed_legendary_shiny_caught)
        async def legendary_shiny_fled():
            embed_legendary_shiny_fled = discord.Embed(
                title= "The shiny " + str(leg_choice) + " escaped!",
                description=message.author.name + " battled hard, but could not catch the legendary pokemon!", color=0xef101e)
            embed_legendary_shiny_fled.set_image(url="http://www.pokestadium.com/sprites/xy/shiny/" + str(leg_choice).lower() + ".gif")
            await client.send_message(message.channel, embed=embed_legendary_shiny_fled)
        async def leg_capture():
            if shiny_or_not <= 96:
                await client.send_message(message.channel, "throwing pokéball...")
                await asyncio.sleep(1)
                await client.send_message(message.channel, "excellent throw!")
                await asyncio.sleep(1.5)
                await client.send_file(message.channel, "images/shake.png")
                await asyncio.sleep(1.5)
                if random.randint(1, 100) < 14:
                    await legendary_fled()
                    await asyncio.sleep(0.5)
                else:
                    await client.send_file(message.channel, "images/shake2.png")
                    await asyncio.sleep(1.5)
                    if random.randint(1, 100) < 15:
                        await legendary_fled()
                        await asyncio.sleep(1.5)
                    else:
                        await client.send_file(message.channel, "images/shake.png")
                        await asyncio.sleep(1.5)
                        await legendary_caught()
                        if leg_iv > 90:
                            await client.send_message(message.channel, leg_highiv)
                            await asyncio.sleep(1)
            else:
                await client.send_message(message.channel, "throwing pokéball...")
                await asyncio.sleep(1)
                await client.send_message(message.channel, "excellent throw!")
                await asyncio.sleep(1.5)
                await client.send_file(message.channel, "images/shake.png")
                await asyncio.sleep(1.5)
                if random.randint(1, 100) < 14:
                    await legendary_shiny_fled()
                    await asyncio.sleep(0.5)
                else:
                    await client.send_file(message.channel, "images/shake2.png")
                    await asyncio.sleep(1.5)
                    if random.randint(1, 100) < 15:
                        await legendary_shiny_fled()
                        await asyncio.sleep(1.5)
                    else:
                        await client.send_file(message.channel, "images/shake.png")
                        await asyncio.sleep(1.5)
                        await legendary_shiny_caught()
                        if leg_iv > 90:
                            await client.send_message(message.channel, leg_highiv)
                            await asyncio.sleep(1)
        async def legendary_normal_spawn():
            embed_legendary_normal_spawn = discord.Embed(
                title= leg_choice,
                description="CP: " + str(raid_boss_cp(find_pokemon_id(leg_choice), 5)) + "\nThe legendary pokemon " + str(leg_choice) + " has appeared\nand is ready for battle! Goodluck, trainer!", color=0x20ef25)
            embed_legendary_normal_spawn.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(leg_choice).lower() + ".gif")
            await client.send_message(message.channel, embed=embed_legendary_normal_spawn)
        async def legendary_shiny_spawn():
            embed_legendary_shiny_spawn = discord.Embed(
                title= "Shiny " + leg_choice,
                description= "CP: " + str(raid_boss_cp(find_pokemon_id(leg_choice), 5)) + "\nThe shiny legendary " + str(leg_choice) + " has appeared\nand is ready for battle! Goodluck, trainer!", color=0x20ef25)
            embed_legendary_shiny_spawn.set_image(url="http://www.pokestadium.com/sprites/xy/shiny" + str(leg_choice).lower() + ".gif")
            await client.send_message(message.channel, embed=embed_legendary_shiny_spawn)
        if shiny_or_not <= 96:
            await legendary_normal_spawn()
            asyncio.sleep(0.3)
        else:
            await legendary_shiny_spawn()
            asyncio.sleep(0.3)
        if client.wait_for_message(author=message.author, content="$raid"):
            await client.send_message(message.channel, "User " + message.author.mention + " has began a battle with the wild " + leg_choice + "!")
            await asyncio.sleep(1)
            await client.send_message(message.channel, "To attack, type `$attack`")
            await asyncio.sleep(0.1)
            #make sure $attack is written before everything else begins
            def check(msg):
                return msg.content.startswith("$attack")
            def leg_catch(msg):
                return msg.content.startswith("$catch")
            if client.wait_for_message(author=message.author, content="$attack"):
                message = await client.wait_for_message(author=message.author, check=check)
                await asyncio.sleep(0.3)
                await client.send_message(message.channel, "The wild " + str(leg_choice) + " has " + str(damage) + " health left! To attack again, type `$attack`")
                await asyncio.sleep(0.1)
                if client.wait_for_message(author=message.author, content="$attack"):
                    message = await client.wait_for_message(author=message.author, check=check)
                    await asyncio.sleep(0.3)
                    await client.send_message(message.channel, "The wild " + str(leg_choice) + " has " + str(damage2) + " health left! To attack again, type `$attack`")
                    await asyncio.sleep(0.1)
                    if client.wait_for_message(author=message.author, content="$attack"):
                        message = await client.wait_for_message(author=message.author, check=check)
                        await asyncio.sleep(0.3)
                        await client.send_message(message.channel, "The wild " + str(leg_choice) + " has " + str(damage3) + " health left! To attack again, type `$attack`")
                        await asyncio.sleep(0.1)
                        if client.wait_for_message(author=message.author, content="$attack"):
                            message = await client.wait_for_message(author=message.author, check=check)
                            await asyncio.sleep(0.3)
                            if damage4 <=0:
                                await client.send_message(message.channel, "The wild " + str(leg_choice) + " has fainted! To catch it, type `$catch`")
                                if client.wait_for_message(author=message.author, content="$catch"):
                                    message = await client.wait_for_message(author=message.author, check=leg_catch)
                                    await leg_capture()
    if message.content.startswith('$mydex 90'):
        owner = message.author.id
        query = 'SELECT * FROM pokemon WHERE iv >= 90 AND owner=? ORDER BY date(added)'
        s = ''
        n = 1
        for p in cursor.execute(query, (owner,)):
            s += '#' + str(n) + ". `" + p[1] + "` Type: `" + p[2] + "` Level: `" + str(p[3]) + "` CP: `" + str(p[4]) + "` IV: `" + str(round(int(p[5]), 1)) + "% (" + str(p[6]) + "/" + str(p[7]) + "/" + str(p[8]) + ")`\n    Caught on: " + p[9] + "\n"
            n += 1
        embed = discord.Embed(
            title='Last 5 90% Pokemon',
            description=s, color=0x20ef25
        )
        await client.send_message(message.channel, embed=embed)
    if message.content.startswith('$mydex all'):
        owner = message.author.id
        query = 'SELECT * FROM pokemon WHERE owner=? ORDER BY date(added)'
        s = ''
        n = 1
        for p in cursor.execute(query, (owner,)):
            s += '#' + str(n)+ ". `" + p[1] + "` Type: `" + p[2] + "` Level: `" + str(p[3]) + "` CP: `" + str(p[4]) + "` IV: `" + str(round(int(p[5]), 1)) + "% (" + str(p[6]) + "/" + str(p[7]) + "/" + str(p[8]) + ")`\n    Caught on: " + p[9]+ "\n"
            n += 1
        embed = discord.Embed(
            title='Last 5 Pokemon',
            description=s, color=0x20ef25
        )
        await client.send_message(message.channel, embed=embed)
    if message.content.startswith('$mydex shiny'):
        owner = message.author.id
        query = 'SELECT * FROM pokemon WHERE type=\'Shiny\' AND owner=? ORDER BY date(added)'
        s = ''
        n = 1
        for p in cursor.execute(query, (owner,)):
            s += '#' + str(n)+ ". `" + p[1] + "` Type: `" + p[2] + "` Level: `" + str(p[3]) + "` CP: `" + str(p[4]) + "` IV: `" + str(round(int(p[5]), 1)) + "% (" + str(p[6]) + "/" + str(p[7]) + "/" + str(p[8]) + ")`\n    Caught on: " + p[9]+ "\n"
            n += 1
        embed = discord.Embed(
            title='Last 5 Shiny Pokemon',
            description=s, color=0x20ef25
        )
        await client.send_message(message.channel, embed=embed)



    if message.content.startswith("$help"):
        if message.author == client.user:
            return
        def help_check(msg):
            return msg.content.startswith("$help")
        message = await client.wait_for_message(author=message.author, check=help_check)
        embed_help = discord.Embed(
            title = "Help",
            description = ("Welcome to PokeBot v3.2.2!\n\nPokemon will randomly appear in chat, to catch them, simply type $throw to throw a pokeball! Alternatively, you can also `$search` for Pokémon!\nIV's and Level follow the style of Pokemon GO!\n\nWant to hatch a pokemon? Simply type $hatch. IV's and Level will also follow Pokemon GO Egg hatch mechanics.\n\nIf you'd like to raid against a legendary, simply type $raid to get started!\n\nWant to test your luck? To see how many encounters it would take before you ran into a 100% Pokemon, type `$100`\n\nWant to report a bug? Message 1447xRK!\n\n*no copyright infringment intended with images, they do not belong to me*"),
            color = 3447003,
        )
        await client.send_message(message.channel, embed=embed_help)

client.run("INSERT BOT TOKEN BETWEEN QUOTES")

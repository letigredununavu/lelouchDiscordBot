import discord
from discord.ext import commands
import os
import random
import sqlite3

token = "NzU0NDU5NzE3NTYwMTcyNjA0.X11DXQ.2VcrWnJkzMadmmR8wM-KQJaEQms"

client = commands.Bot(command_prefix = '>', help_command=None)

mots = open("mots.txt", 'r')
mots = mots.read().split('\n')

def add_users_in_leaderBoard(user, points = 0):
    try:
        #Connect to databse
        connection = sqlite3.connect('hangMan.db')
        cursor = connection.cursor()
        print("cursor connected")

        cursor.execute("select * from scores where name=?", (user,))

        if not cursor.fetchone():
        
            #Create the query command pass it to the cursor with the user argument and initial 0 points
            sql_query = "insert into scores values (?,?)"
            cursor.execute(sql_query, (user, points))

        #Commit the changes
        connection.commit()

        print("modifs enregistrés")

        cursor.close()

    except sqlite3.Error as error:
        print("error dans l'ajout")

    #Close the connection
    finally:
        if (connection):
            connection.close()
            print("connection fini")


def add_points_to_user(user, points_to_add):
    try:
        #Connect to database
        connection = sqlite3.connect('hangMan.db')
        cursor = connection.cursor()
        print("cursor connected")

        #Create the query command and execute it with the cursor
        sql_query = "select * from scores where name=? "
        cursor.execute(sql_query, (user,))

        player = cursor.fetchone()
        if player:
            new_points = player[1] + points_to_add
            print("new points = {}".format(new_points))
            sql_query = "update scores set points=? where name=?"
            cursor.execute(sql_query, (new_points, user))
        else:
            add_users_in_leaderBoard(user, points_to_add)
            print("new player created with {} points".format(points_to_add))
        print("update successful")
        connection.commit()
        cursor.close()

    except expression as identifier:
        print("error dans l'ajout des points")

    finally:
        if (connection):
            connection.close()
            print("connection fini")


def get_database():
    try:
        #Connect to database
        connection = sqlite3.connect('hangMan.db')
        cursor = connection.cursor()
        print("cursor connected")

        #Create the query command and execute it
        sql_query = "select * from scores"
        cursor.execute(sql_query)

        database = cursor.fetchall()

        cursor.close()

    except sqlite3.Error as error:
        print("error dans le show_data")

    finally:
        if (connection):
            connection.close()
            print("connection fini")

        return database


def clean_database():
    try:
        connection = sqlite3.connect('hangMan.db')
        cursor = connection.cursor()
        print("cursor connected")

        sql_query = "delete from scores"
        cursor.execute(sql_query)
        connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("erreur dans la suppresion de la db")

    finally:
        if (connection):
            connection.close()
            print("connection fini")


class Game():
    def __init__(self, mot = "giraffe", start = False, lettres_utilisees = [], lives = 7):
        self.mot = mot
        self.start = start
        self.lettres_utilisees = lettres_utilisees
        self.mot_chiffrer = ['-' for i in range(len(self.mot))]
        self.lives = lives
    
    def new_game(self, mot):
        self.mot = mot
        self.lives = 7
        self.start = True
        self.lettres_utilisees = []
        self.mot_chiffrer = ['-' for i in range(len(self.mot))]


game = Game()


def get__adding_points_with_letter():
    multiplier = 1
    for letter in game.mot_chiffrer:
        if letter != '-':
            multiplier += 1

    return 3 * len(game.mot) - 2 * multiplier


def get_minus_points_with_letter():
    multiplier = 1
    for letter in game.mot_chiffrer:
        if letter != '-':
            multiplier += 1

    return -(len(game.mot) + 2 * multiplier)


def get_adding_points_with_word():
    multiplier = 1
    for letter in game.mot_chiffrer:
        if letter != '-':
            multiplier += 1
    
    return 4 * len(game.mot) - 2 * multiplier

def get_minus_points_with_word():
    multiplier = 1
    for letter in game.mot_chiffrer:
        if letter != '-':
            multiplier += 1
    
    return -(2 * len(game.mot) + 2 * multiplier)


@client.event
async def on_ready():
    print("We have logged in as {}".format(client))

@client.command()
async def start(ctx):
    await ctx.send("game starting")
    game.new_game(mots[random.randrange(len(mots))])
    await ctx.send("Le mot: {}".format(''.join(game.mot_chiffrer)))

@client.command()
async def play(ctx, *, letter):
    if game.start:
        letter = letter.lower()
        if len(letter) > 1 or not letter.isalpha():
            await ctx.send("Pas un caractere valide")
        
        elif letter in game.lettres_utilisees:
            await ctx.send("Vous avez déjà utilisé cette lettre bande de nazes...")
        
        else:
            user = ctx.author.name

            if letter in game.mot:
                await ctx.send("Houuu congrats biatch") 
                points = get__adding_points_with_letter()
                add_points_to_user(user, points)

                for i in range(len(game.mot)):
                    if letter == game.mot[i]:
                        game.mot_chiffrer[i] = letter

            else:
                await ctx.send("Nope.")
                points = get_minus_points_with_letter()
                add_points_to_user(user, points)
                game.lives -= 1

                if game.lives <= 0:
                    await ctx.send("Vous avez perdu pétasses")
                    await ctx.send("-play turn around")
                    await ctx.send("Le mot était: {}".format(game.mot))
                    game.start = False
                    return

            game.lettres_utilisees.append(letter)
            
            await ctx.send("mot: {}".format(''.join(game.mot_chiffrer)))
            await ctx.send("lettres utilisées: {}".format(game.lettres_utilisees))
            await ctx.send("vies restantes: {}".format(game.lives))

            if not '-' in game.mot_chiffrer:
                await ctx.send("Congratulations!!!")
                await ctx.send("-play congratulations")
                game.start = False
    else:
        await ctx.send("Aucun partie est commencé connasse")

@client.command()
async def guess(ctx, *, word):
    user = ctx.author.name
    if word.lower() == game.mot:
        await ctx.send("Bravooo!, le mot était bien: {}".format(game.mot))
        points = get_adding_points_with_word()
        add_points_to_user(user, points)
        game.start = False
    else:
        points = get_minus_points_with_word()
        add_points_to_user(user, points)
        await ctx.send("No, better luck next time")
        game.lives -= 1


@client.command()
async def help(ctx):
    message = "```\nCommandes du bots:\n\n"
    message += ">help pour voir les commandes du bots\n\n"
    message += "Catégorie partie: \n\n"
    message += ">start pour commencer une partie\n"
    message += ">guess _(le mot) pour guess le mot au complet (!Attention, ca donne plus de points, mais en enlève plus aussi!)\n"
    message += ">play _(une lettre de l'alphabet) pour jouer une lettre, pas de symboles spéciaux (-, , ')\n\n"
    message += "Catégorie leaderboard: \n\n"
    message += ">leaderboard pour voir le leaderboard\n"
    message += ">clean_db pour effacer la base de données\n"
    message += ">add_user pour ajouter votre username au leaderboard, vous pouvez aussi juste jouer\n\n```\n"
    await ctx.send(message)



@client.command()
async def add_user(ctx):
    user = ctx.author.name
    add_users_in_leaderBoard(user)

@client.command()
async def leaderboard(ctx):
    database = get_database()
    message = ""
    for i in range(len(database)):
        message += "{} : {} avec {} points\n".format(i+1, database[i][0], database[i][1])
    if message:
        await ctx.send(message)

@client.command()
async def clean_db(ctx):
    if ctx.author.name == 'tonythelion':
        clean_database()
    else:
        await ctx.send("HAHAHAHAHA tu n'as pas ce pouvoir")

client.run(token)
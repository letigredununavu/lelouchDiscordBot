import discord
from discord.ext import commands
import os
import random
import sqlite3
import dbControl as db

client = commands.Bot(command_prefix = '>', help_command=None)

# Formatting the words bank
mots = open("mots.txt", 'r', encoding='utf-8')
mots = mots.read().split('\n')

images = ['images/dead.png', 'images/live6.png', 'images/live5.png', 'images/live4.png',
     'images/live3.png', 'images/live2.png', 'images/live1.png', 'images/live0.png']


# The class that represent our game
class Game():

    def __init__(self, mot = "giraffe", start = False, lettres_utilisees = [], lives = 7):
        self.mot = mot
        self.start = start
        self.lettres_utilisees = lettres_utilisees
        self.mot_chiffrer = ['-' for i in range(len(self.mot))]
        self.lives = lives
    
    # function to create a new game
    def new_game(self, mot):
        self.mot = mot
        self.lives = 7
        self.start = True
        self.lettres_utilisees = []
        self.mot_chiffrer = ['-' for i in range(len(self.mot))]


game = Game()


# Function to get the number of points to add with a guessed letter
def get_adding_points_with_letter():
    multiplier = len(game.mot) - game.mot_chiffrer.count('-')

    return 3 * len(game.mot) - multiplier


# Function to get the number of points to remove with a wronged guessed letter
def get_minus_points_with_letter():
    multiplier = len(game.mot) - game.mot_chiffrer.count('-')

    return -(len(game.mot)/2 + multiplier)


# Function to get the number of points to add with a guessed word
def get_adding_points_with_word():
    multiplier = len(game.mot) - game.mot_chiffrer.count('-')
    
    return 4 * len(game.mot) - 2 * multiplier


# Function to get the number of points to remove with a wronged guessed word
def get_minus_points_with_word():
    multiplier = len(game.mot) - game.mot_chiffrer.count('-')
    
    return -(len(game.mot) + 2 * multiplier)


@client.event
async def on_ready():

    print("We have logged in as {}".format(client))
    await client.change_presence(activity=discord.Game(name='Hang Man | >help'))


# Command to start a new game
@client.command()
async def start(ctx):

    message = ""
    message += "game starting\n"

    game.new_game(mots[random.randrange(len(mots))])

    message += "Le mot: {}".format(''.join(game.mot_chiffrer))

    image = images[game.lives]


    await ctx.send(message, file=discord.File(image))
    #await ctx.send()


# Command to guess a letter
@client.command()
async def play(ctx, *, letter):

    # If a game is started
    if game.start:

        # Format the input to lowercase
        letter = letter.lower()

        # Check that the input is ONE letter and in the alphabet
        if len(letter) > 1 or not letter.isalpha():
            await ctx.send("Pas un caractere valide")
        
        # Check that they did not already used the letter
        elif letter in game.lettres_utilisees:
            await ctx.send("Vous avez déjà utilisé cette lettre bande de nazes...")
        
        else:
            message = ""
            user = ctx.author.name

            # If the letter is in the word
            if letter in game.mot:
                message += "Houuu congrats {}\n".format(user)
                #await ctx.send("Houuu congrats biatch")

                # Get the points to add to the user and adding them
                points = get_adding_points_with_letter()
                db.add_points_to_user(user, points)

                for i in range(len(game.mot)):
                    if letter == game.mot[i]:
                        game.mot_chiffrer[i] = letter
                game.lettres_utilisees.append(letter)
            
                message += "mot: {}\n".format(''.join(game.mot_chiffrer))
                message += "lettres utilisées: {}\n".format(game.lettres_utilisees)
                message += "vies restantes: {}\n".format(game.lives)

                # If the game is won
                if not '-' in game.mot_chiffrer:
                    message += "Congratulations vous avez gagné!!!"
                    #await ctx.send("Congratulations!!!")
                    game.start = False
        
                await ctx.send(message)


            else:

                message += "Nope.\n"
                #await ctx.send("Nope.")

                # Get the points the remove to the user and remove them
                points = get_minus_points_with_letter()
                db.add_points_to_user(user, points)

                game.lives -= 1

                image = images[game.lives]

                # If they have lost
                if game.lives <= 0:
                    message += "Vous avez perdu...\nLe mot était: {}\n".format(game.mot)
                    #await ctx.send("Vous avez perdu pétasses\nLe mot était: {}\n".format(game.mot))

                    game.start = False

                else:
                    game.lettres_utilisees.append(letter)
            
                    message += "mot: {}\n".format(''.join(game.mot_chiffrer))
                    message += "lettres utilisées: {}\n".format(game.lettres_utilisees)
                    message += "vies restantes: {}\n".format(game.lives)
        
                await ctx.send(message, file=discord.File(image))

    else:
        await ctx.send("Aucun partie n'est commencée")


# Command to guess the entire word
@client.command()
async def guess(ctx, *, word):

    # Si une partie est commencé
    if game.start:
        user = ctx.author.name
        # If the guess is correct add the points
        if word.lower() == game.mot:
            await ctx.send("Bravooo! {}, le mot était bien: {}".format(user, game.mot))

            points = get_adding_points_with_word()
            db.add_points_to_user(user, points)

            game.start = False
        
        # Else, remove points and a live
        else:
            message = ""

            points = get_minus_points_with_word()
            db.add_points_to_user(user, points)

            game.lives -= 1

            # If they have lost
            if game.lives <= 0:
                message += "Vous avez perdu pétasses\nLe mot était: {}\n".format(game.mot)

                game.start = False

            else:
                image = images[game.lives]
                message += "No, better luck next time\n"
                message += "mot: {}\n".format(''.join(game.mot_chiffrer))
                message += "lettres utilisées: {}\n".format(game.lettres_utilisees)
                message += "vies restantes: {}".format(game.lives)
            
            await ctx.send(message, file=discord.File(image))
    
    else:
        await ctx.send("Aucun partie n'est commencée")
        


# The help command
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


# The command to add to user to the database
@client.command()
async def add_user(ctx):
    user = ctx.author.name
    db.add_users_in_leaderBoard(user)


# The command to show the database
@client.command()
async def leaderboard(ctx):

    database = db.get_database()
    if database:
        message = ""
        
        for i in range(len(database)):
            message += "{} : {} avec {} points\n".format(i+1, database[i][0], database[i][1])
        
        if message:
            await ctx.send(message)
    else:
        await ctx.send("Database vide")


# Command to clean the database
@client.command()
async def clean_db(ctx):

    if ctx.author.name == 'tonythelion':
        await ctx.send("Database cleané")
        db.clean_database()
    
    else:
        await ctx.send("HAHAHAHAHA tu n'as pas ce pouvoir")

        
token = os.environ['BOT_TOKEN']
client.run(token)

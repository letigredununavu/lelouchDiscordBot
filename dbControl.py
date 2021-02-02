from user import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import desc
import stats

# Fichier qui controle tous les accès et modifications à la base de données


# Ajoute un user du nom 'username' avec 'points' points dans la db 
def add_user(username, points):

    engine = create_engine('sqlite:///HangMan.db', echo=False)

    Base.metadata.create_all(bind=engine)
    

    Session = sessionmaker(bind=engine)

    session = Session()

    user = session.query(User).filter_by(name = username).first()

    # Vérifie que l'user n'existe pas déjà
    if not user:
        user = User(username, points)
        print(user)
        session.add(user)
        session.commit()
        print("\n\nuser added ({})\n\n".format(user))
    else:
        print("user existait déjà")

    session.close()


# Ajoute 'points' points au jouer 'username'
def add_points_to_user(username, points):

    engine = create_engine('sqlite:///HangMan.db', echo=False)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    # Si le joueur existait pas, on le crée
    if not session.query(User).filter_by(name=username).first():
        add_user(username, 0)

    user = session.query(User).filter_by(name = username).first()
    print(user)

    user.points += points

    print("points ajouté a l'user {}".format(user.name))
    session.commit()

    session.close()


# Retourne tous les joueurs dans la db
def get_database():
    engine = create_engine('sqlite:///HangMan.db', echo=False)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    users = session.query(User).order_by(desc(User.points)).all()

    session.close()

    return users


# Efface tous les joueurs de la db
def clear_database():
    engine = create_engine('sqlite:///HangMan.db', echo=False)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    users = session.query(User).all()
    for user in users:
        session.delete(user)

    session.commit()

    session.close()
    print("database cleaner")


# Retourne les data du joueur 'username'
def get_user_data(username):
    engine = create_engine('sqlite:///HangMan.db', echo=False)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    if not session.query(User).filter_by(name=username).first():
        add_user(username, 0)

    user = session.query(User).filter_by(name=username).first()

    session.close()

    return user


# Ajoute une occurence de la lettre 'letter' au joueur 'username'
def add_letter_occurence(username, letter):
    engine = create_engine('sqlite:///HangMan.db', echo=False)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    # Vérification que le joueur existe
    if not session.query(User).filter_by(name=username).first():
        add_user(username, 0)

    user = session.query(User).filter_by(name=username).first()

    user.letters[letter] += 1

    session.commit()
    print("lettre {} ajouté à l'user {}".format(letter, username))

    session.close()


# Ajoute une victoire au joueur 'username'
def add_win_to_player(username):
    engine = create_engine('sqlite:///HangMan.db', echo=False)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    # Vérification que le joueur existe
    if not session.query(User).filter_by(name=username).first():
        add_user(username, 0)

    user = session.query(User).filter_by(name=username).first()

    user.games_won += 1

    session.commit()
    print("victoire ajouté à l'user {}".format(username))

    session.close()


# Ajoute une partie au joueur 'username'
def add_game_to_player(username):
    engine = create_engine('sqlite:///HangMan.db', echo=False)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    # Vérification que le joueur existe
    if not session.query(User).filter_by(name=username).first():
        add_user(username, 0)

    user = session.query(User).filter_by(name=username).first()

    user.games_played += 1

    session.commit()
    print("1 partie jouée ajouté à l'user {}".format(username))

    session.close()


# Ajoute une lettre bien deviné au joueur 'username'
def add_guessed_letters_to_player(username, letter):
    engine = create_engine('sqlite:///HangMan.db', echo=False)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    # Vérification que le joueur existe
    if not session.query(User).filter_by(name=username).first():
        add_user(username, 0)

    user = session.query(User).filter_by(name=username).first()

    user.guessed_letters += 1
    user.total_letters += 1
    user.letters[letter] += 1

    session.commit()
    print("Une lettre de plus de devinée pour l'utilisateur {}".format(username))

    session.close()


# incrémente le nombre de lettres guessed par le joueur 'username'
def add_total_letters(username, letter):
    engine = create_engine('sqlite:///HangMan.db', echo=False)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    # Vérification que le joueur existe
    if not session.query(User).filter_by(name=username).first():
        add_user(username, 0)

    user = session.query(User).filter_by(name=username).first()

    user.total_letters += 1
    user.letters[letter] += 1

    session.commit()
    print("Une lettre de plus pour l'utilisateur {}".format(username))

    session.close()


# Crée l'image des graphique avec les data de 'username'
def create_graphs(username):
    user = get_user_data(username)

    alphabet = [i for i in user.letters.keys()]

    alphabet_values = [i for i in user.letters.values()]

    games_played = user.games_played

    games_won = user.games_won

    good_guessed_letters = user.guessed_letters

    nbr_of_guessed_letters = user.total_letters

    stats.create_graph_as_png(alphabet, alphabet_values, games_played, 
        games_won, good_guessed_letters, nbr_of_guessed_letters, user)



if __name__ == '__main__':
    add_user('even', 100)
    add_points_to_user('even', 100)
    users = get_database()
    for user in users:
        print(user)
    clear_database()
    add_user('antoine',12)
    users = get_database()
    for user in users:
        print(user)
    add_letter_occurence('antoine', 'é')
    add_game_to_player('antoine')
    add_guessed_letters_to_player('antoine','v')
    create_graphs('antoine')

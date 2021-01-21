import sqlite3

# Function to add a user to the database
def add_users_in_leaderBoard(user, points = 0):

    try:
        # Connect to database
        connection = sqlite3.connect('hangMan.db')
        cursor = connection.cursor()
        print("cursor connected")

        # Verify that the user is not already in the database
        cursor.execute("select * from scores where name=?", (user,))

        if not cursor.fetchone():
        
            # Create the query command pass it to the cursor with the user argument and initial 0 points
            sql_query = "insert into scores values (?,?)"
            cursor.execute(sql_query, (user, points))

        # Commit the changes
        connection.commit()

        print("modifs enregistrés")

        cursor.close()

    except sqlite3.Error as error:
        print("error dans l'ajout")

    # Close the connection
    finally:
        if (connection):
            connection.close()
            print("connection fini")


# Function to add points to a user
def add_points_to_user(user, points_to_add):

    try:
        # Connect to the database
        connection = sqlite3.connect('hangMan.db')
        cursor = connection.cursor()
        print("cursor connected")

        # Create the query command and execute it with the cursor
        sql_query = "select * from scores where name=? "
        cursor.execute(sql_query, (user,))

        player = cursor.fetchone()

        # Verify that the player exist
        if player:
            new_points = player[1] + points_to_add
            print("new points = {}".format(new_points))
            sql_query = "update scores set points=? where name=?"
            cursor.execute(sql_query, (new_points, user))
        
        # If the player does not exist, create it
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


# Function to get the entire database
def get_database():

    try:
        # Connect to database
        connection = sqlite3.connect('hangMan.db')
        cursor = connection.cursor()
        print("cursor connected")

        # Create the query command and execute it
        sql_query = "select * from scores order by points desc"
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


# Function to erase all database
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
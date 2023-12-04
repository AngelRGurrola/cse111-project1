import sqlite3
from sqlite3 import Error  

def openConnection(_dbFile):
    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
    except Error as e:
        print(e)

    return conn

def closeConnection(_conn, _dbFile):
    try:
        _conn.close()
    except Error as e:
        print(e)

def start(_conn):
        while True:
            print("\n------------------------------------------")
            print("MOVIE ORGANIZER: ")
            print("1. Login Profile")
            print("2. Create Profile")
            print("3. End Session") 

            num = input("\nEnter desired number here: ")

            if num == "1":
                login(_conn)
            elif num == "2":
                create(_conn)
            elif num == "3":
                break
            
            else:
                print("Invalid Input: Please select a desired action with the appropriate number")

def create(_conn):
    print("\n    Creating User")
    print("-------------------------------")
    user_name = input("Enter User Name: ")
    print("\nFilm Platforms: Amazon Prime / HULU / Netflix / Disney+")
    plat_a = changeAmazon()
    plat_h = changeHulu()
    plat_n = changeNetflix()
    plat_d = changeDisney()

    sql = """SELECT max(userID) + 1 FROM Users"""
    cur = _conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:        #DO I NEED TO ITERATE TO GO INTO THE RESULT
        user_id = row[0]
    print("%d, %s, %d, %d, %d, %d" % (user_id, user_name, plat_a, plat_h, plat_n, plat_d)) #testing the caputer of User Inputs

def changeAmazon():
    while True:
        check = input("\nAmazon Prime Y or N: ")
        check.upper()
        if check == "Y":
            plat_a = 1
            return plat_a
        elif check == "N":
            plat_a == 0
            return plat_a
        else:
            print("Please enter a correct response")

def changeHulu():
    while True:
        check = input("\nHULU Y or N: ")
        check.upper()
        if check == "Y":
            plat_h = 1
            return plat_h
        elif check =="N":
            plat_h = 0
            return plat_h
        else:
            print("Please enter a correct response")

def changeNetflix():
    while True:
        check = input("\nNetflix Y or N: ")
        check.upper()
        if check == "Y":
            plat_n = 1
            return plat_n
        elif check == "N":
            plat_n = 0
            return plat_n
        else:
            print("Please enter a correct response")

def changeDisney():
    while True:
        check = input("\nDisney+ Y or N: ")
        check.upper()
        if check == "Y":
            plat_d = 1
            return plat_d
        elif check == "N":
            plat_d = 0
            return plat_d
        else:
            print("Please enter a correct response")

def login(_conn):
    print("\nChoose an Existing Profile")
    try:   
        sql = """SELECT userName FROM Users"""
        cur = _conn.cursor()
        cur.execute(sql)

        p = '{:>10}'.format("Users")
        print(p)
        print("-------------------------------")

        rows = cur.fetchall()
        for row in rows:
            p = '{:>10}'.format(row[0])
            print(p)
        print("-------------------------------")
        check = True
        while check:
            user = input("Enter User Name: ")
            sql = """SELECT userName, userID FROM Users WHERE userName = ?"""
            args = [user]
            cur = _conn.cursor()
            cur.execute(sql, args)
            rows = cur.fetchall()
            spell_check = 0
            for row in rows:
                if user == row[0]:
                    p = '{:>10} {:>10}'.format(row[0], row[1])
                    user_name = row[0]
                    user_id = row[1]
                    print(p)
                    spell_check = 1
                    check = False
            if spell_check == 0:
                print("Incorrect User OR User does not exist")

        loginInterface(user_name, user_id, _conn)
        
    except Error as e:
        print(e)

def loginInterface(name, id, _conn):
    while True:
        print("\n------------------------------------------")
        print("WELCOME %s TO YOUR FILM ORGANIZER" % (name))
        print("1. Watch Later")
        print("2. Owned Films")
        print("3. Streaming Platform")
        print("4. Log Out")

        num = input("\nEnter desired number here: ")

        if num == "1":
            watchLaterInterface(name, id, _conn)
        elif num == "2":
            ownedFilmsInterface(id, _conn)
        elif num == "3":
            print("hi")
        elif num == "4":
            break
        
        else:
            print("Invalid Input: Please select a desired action with the appropriate number")

def ownedFilmsInterface(id, _conn):
    while True:
        print("\n------------------------------------------")
        print("OWNED FILMS LIST:")
        statement = '''
            SELECT * 
            FROM OwnedFilms
            WHERE userID = ?;
        '''
        arg = [id]
        
        cur = _conn.cursor()
        cur.execute(statement, arg)
        rows = cur.fetchall()
        for row in rows:
            print(row[1])
            
        print("\nOPTIONS:")
        print("1: Add to list") # Still need to be added
        print("2: Delete from list")
        print("3: More details on film")
        print("4: Return back")
        userInput = input("\nEnter option:")
        
        if userInput == "1":
            print("ADD")
        elif userInput == "2":
            print("\nWHICH FILM DO YOU WANT TO DELETE?")
            
            i = 1
            for row in rows:
                print(i, ": ", row[1])
                i += 1
            print("0: Cancel")
            deleteRow = input("\nSelect number ")
            if int(deleteRow) != 0:
                deleteFromOwnedFilms(id, rows[int(deleteRow) - 1][1], _conn) 
        elif userInput == "3":
            print("\nWHICH FILM DO YOU WANT MORE DETAIL?")
            
            i = 1
            for row in rows:
                print(i, ": ", row[1])
                i += 1
            print("0: Cancel")
            deleteRow = input("\nSelect number ")
            if int(deleteRow) != 0:
                filmDetails(rows[int(deleteRow) - 1][1], _conn)
        elif userInput == "4":
            break
        else:
            print("Invalid Option")

def deleteFromOwnedFilms(id, filmName, _conn):
    cur = _conn.cursor()
    args = [id, filmName]
    
    statement = '''
        DELETE FROM OwnedFilms
        WHERE userID = ?
            AND filmName = ?;
    '''
    cur.execute(statement, args)
    print(filmName, "HAS BEEN DELETED FROM YOUR LIST.")
    
    # Uncomment this to save the changes in the database
    # cur.commit()
        
    return 0
                   
def watchLaterInterface(name, id, _conn):
    while True:
        print("\n------------------------------------------")
        print("WATCH LATER LIST:")
        statement = '''
            SELECT * 
            FROM WatchLater w
            WHERE ? = w.userID;
        '''
        arg = [id]
        
        cur = _conn.cursor()
        cur.execute(statement, arg)
        rows = cur.fetchall()
        for row in rows:
            print(row[1])
        
        print("\nOPTIONS:") 
        print("1: Add to list") # Still need to be added
        print("2: Delete from list")
        print("3: More details on film")
        print("4: Return back")
        userInput = input("\nEnter option:")
        
        if userInput == "1":
            print("ADD")
        elif userInput == "2": 
            print("\nWHICH FILM DO YOU WANT TO DELETE?")
            
            i = 1
            for row in rows:
                print(i, ": ", row[1])
                i += 1
            print("0: Cancel")
            deleteRow = input("\nSelect number ")
            if int(deleteRow) != 0:
                deleteFromWatchLater(id, rows[int(deleteRow) - 1][1], _conn)
        elif userInput == "3":
            print("\nWHICH FILM DO YOU WANT MORE DETAIL?")
            
            i = 1
            for row in rows:
                print(i, ": ", row[1])
                i += 1
            print("0: Cancel")
            deleteRow = input("\nSelect number ")
            if int(deleteRow) != 0:
                filmDetails(rows[int(deleteRow) - 1][1], _conn)
        elif userInput == "4":
            break
        else:
            print("Invalid option")
        
def deleteFromWatchLater (id, filmName, _conn):
    cur = _conn.cursor()
    args = [id, filmName]
    
    statement = '''
        DELETE FROM WatchLater
        WHERE userID = ?
            AND filmName = ?;
    '''
    
    cur.execute(statement, args)
    print(filmName, "HAS BEEN DELETED FROM YOUR LIST.")
    
    # Uncomment this to save the changes in the database
    # cur.commit()
    
    return 0
        
def filmDetails (filmName, _conn):
    cur = _conn.cursor()
    arg = [filmName]
    
    statement = '''
    SELECT movieTitle as Title,
        year as Year, 
        genre as Genre,
        summary as Summary,
        imdbRating as Rating,
        director as Director,
        star1 as Stars,
        star2 as Stars,
        star3 as Stars,
        star4 as Stars
    FROM movieDetails
    WHERE movieTitle = ?;
    '''
    
    cur.execute(statement, arg)
    rows = cur.fetchall()
    
    for row in rows:
        print(f"\nMovie Title: {row[0]}")
        print(f"Year: {row[1]}")
        print(f"Genre: {row[2]}")
        print(f"Summary: {row[3]}")
        print(f"imbdRating: {row[4]}")
        print(f"Director: {row[5]}")
        print(f"Stars: {row[6]}, {row[7]}, {row[8]}, {row[9]}")
        
    input("\nPress enter to continue...")
    
    
    return 0

def main():
    database = r"film.sqlite"

    # create a database connection
    conn = openConnection(database)
    
    start(conn)

    closeConnection(conn, database)

if __name__ == "__main__":
    main()
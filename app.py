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
    cur = _conn.cursor()
    
    print("\n    Creating User")
    print("-------------------------------")
    user_name = input("Enter User Name: ")
    print("\nFilm Platforms: Amazon Prime / HULU / Netflix / Disney+")
    plat_a = changeAmazon()
    plat_h = changeHulu()
    plat_n = changeNetflix()
    plat_d = changeDisney()

    sql = """SELECT max(userID) + 1 FROM Users"""
    cur.execute(sql)
    rows = cur.fetchall()
    
    statement = '''
        INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?)
    '''
    args = [rows[0][0], user_name, plat_a, plat_h, plat_n, plat_d]
    cur.execute(statement, args)
    
    # Uncomment to commit changes to database
    # cur.commit()

def changeAmazon():
    while True:
        check = (input("\nAmazon Prime Y or N: ")).upper()

        if check == "Y":
            plat_a = 1
            return plat_a
        elif check == "N":
            plat_a = 0
            return plat_a
        else:
            print("Please enter a correct response")

def changeHulu():
    while True:
        check = (input("HULU Y or N: ")).upper()
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
        check = (input("Netflix Y or N: ")).upper()
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
        check = (input("Disney+ Y or N: ")).upper()
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
            user = input("Enter User Name or 0 to cancel Login: ")
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
            if user == "0":
                print("Returning to previous...")
                return 0
            elif spell_check == 0:
                print("Incorrect User OR User does not exist")

        loginInterface(user_name, user_id, _conn)
        
    except Error as e:
        print(e)

def loginInterface(name, id, _conn):
    while True:
        print("\n------------------------------------------")
        print("WELCOME %s TO YOUR FILM ORGANIZER" % (name))
        print("0. Log Out")
        print("1. Watch Later")
        print("2. Owned Films")
        print("3. Streaming Platform")

        num = input("\nEnter desired number here: ")
        if num == "0":
            break
        elif num == "1":
            watchLaterInterface(name, id, _conn)
        elif num == "2":
            ownedFilmsInterface(id, _conn)
        elif num == "3":
            streamPlat(id, _conn)
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
        print("0: Return back")
        print("1: Add to list") # Still need to be added
        print("2: Delete from list")
        print("3: More details on film")
        userInput = input("\nEnter option:")
        
        if userInput == "0":
            break
        elif userInput == "1":
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
        print("0: Return back")
        print("1: Add to list") # Still need to be added
        print("2: Delete from list")
        print("3: More details on film")
        userInput = input("\nEnter option:")
        if userInput == "0":
            break
        elif userInput == "1":
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

def searchFilm(id, _conn):
    while True:
        print("\033[1m" + "\nSelect film type" + "\033[0m")
        filmType = (input("TV Show or Movie? ")).upper()
        
        if filmType == "TV SHOW":
            return 0
        elif filmType == "MOVIE":
            searchMovie(id, _conn)
        else:
            print("Invalid Film Type!")

def searchMovie(id, _conn):
    while True:
        print("\033[1m" + "\nWelcome to the Movie database\nTo return back enter 0" + "\033[0m" )

        userFilter = input("Select how you want to search by: Title, director, genre, year, runtime, stars: ")
        if userFilter != "0":  
            #userFilter = userFilter.split(", ")
            userFilter = re.split(r'[, ]', userFilter)
            userFilter = [word for word in userFilter if word]
            userInput = []
            i = 0
            for filters in userFilter:
                match (userFilter[i]).upper:
                    case "TITLE":
                        userInput.append(input("Enter Title: "))
                        userFilter[i] = "movieTitle"
                    case "DIRECTOR":
                        userInput.append(input("Enter director: "))
                        userFilter[i] = "director"
                    case "GENRE":
                        userInput.append(input("Enter genre: "))
                        userFilter[i] = "genre"
                    case "YEAR":
                        userInput.append(input("Enter year:"))
                        userFilter[i] = "year"
                    case "RUNTIME":
                        userInput.append(input("Enter runtime(minutes): "))
                        userFilter[i] = "runtime"
                    case "STARS":
                        userInput.append(input("Enter star's full name: "))
                        userFilter[i] = "star1"
                
        else:
            return 0

def filterMovie(id, userFitler, userInput, _conn):
    return 0

def streamPlat(id, _conn):
    while True:
        print("------------------------------------------")
        print("\nPLATFORM MANAGER")
        print("0. Return back")
        print("1. Update Platforms")
        print("2. View current Platforms")
        print("3. Search Films in Platforms")
        choice = input("Enter option: ")
        if choice == "0":
            return 0
        elif choice == "1":
            updatePlat(id, _conn)
        elif choice == "2":
            viewPlat(id, _conn)
        elif choice == "3":
            searchPlat(id, _conn)

def searchPlat(id, _conn):
    print("------------------------------------------")


def viewPlat(id, _conn):
    sql = """SELECT amazonPrime, hulu, netflix, disney FROM Users WHERE userID = ?"""
    args = [id]
    cur = _conn.cursor()
    cur.execute(sql, args)
    rows = cur.fetchall()
    list_p = []
    for row in rows:
        plat_a = row[0]
        plat_h = row[1]
        plat_n = row[2]
        plat_d = row[3]
    if plat_a == 1:
        list_p.append("Amazon Prime")
    if plat_h == 1:
        list_p.append("Hulu")
    if plat_n == 1:
        list_p.append("Netflix")
    if plat_d == 1:
        list_p.append("Disney")

    print("\n------------------------------------------")
    if plat_a + plat_h + plat_n + plat_d == 0:
        print("You are currently not subscribed to any Platforms")
    else:
        print(*list_p, sep= ", ", end=" ")
        print("are your current platforms")

def updatePlat(id, _conn):         
    print("\nFilm Platforms: Amazon Prime / HULU / Netflix / Disney+")
    plat_a = changeAmazon()
    plat_h = changeHulu()
    plat_n = changeNetflix()
    plat_d = changeDisney()
    statement = """UPDATE Users
                    SET amazonPrime = ?, hulu = ?, netflix = ?, disney = ?
                    WHERE userID = ?"""
    args = [plat_a, plat_h, plat_n, plat_d, id]
    cur = _conn.cursor()
    cur.execute(statement, args) 

def main():
    database = r"film.sqlite"

    # create a database connection
    conn = openConnection(database)
    
    start(conn)

    closeConnection(conn, database)

if __name__ == "__main__":
    main()

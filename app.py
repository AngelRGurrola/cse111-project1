import sqlite3
import re
from sqlite3 import Error  
import os
import platform

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

def clearTerminal():
    # Comment the line below if running on windows or change it to cls
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Darwin":
        os.system("clear")
    return 0

def start(_conn):
    clearTerminal()
    while True:
        clearTerminal()
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
    clearTerminal()
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
    clearTerminal()
    while True:
        clearTerminal()
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
    clearTerminal()
    while True:
        clearTerminal()
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
        print("1: Add to list")
        print("2: Delete from list")
        print("3: More details on film")
        userInput = input("\033[1m" + "\nEnter option:" + "\033[0m")
        
        if userInput == "0":
            clearTerminal()
            return 0
        elif userInput == "1":
            searchFilm(id, True, False, True, _conn)
        elif userInput == "2":
            clearTerminal()
            print("\nWHICH FILM DO YOU WANT TO DELETE FROM YOUR OWNED FILMS?")
            
            i = 1
            for row in rows:
                print(i, ": ", row[1])
                i += 1
            print("0: Cancel")
            deleteRow = input("\nSelect number ")
            if int(deleteRow) != 0:
                deleteFromOwnedFilms(id, rows[int(deleteRow) - 1][1], _conn)
        elif userInput == "3":
            clearTerminal()
            print("\nWHICH FILM DO YOU WANT MORE DETAIL?")
            
            i = 1
            for row in rows:
                print(i, ": ", row[1])
                i += 1
            print("0: Cancel")
            deleteRow = input("\nSelect number ")
            if int(deleteRow) != 0:
                filmDetails(rows[int(deleteRow) - 1][1], _conn, 0,  id, True)
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
    clearTerminal()
    print(filmName, "HAS BEEN DELETED FROM YOUR LIST.")
    input("Press enter to continue...")
    
    # Uncomment this to save the changes in the database
    # cur.commit()
        
    return 0
                   
def watchLaterInterface(name, id, _conn):
    while True:
        clearTerminal()
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
        userInput = input("\033[1m" + "\nEnter option: " + "\033[0m")
        if userInput == "0":
            break
        elif userInput == "1":
            searchFilm(id, True, True, False, _conn)
        elif userInput == "2": 
            clearTerminal()
            print("\nWHICH FILM DO YOU WANT TO DELETE FROM YOUR WATCH LATER?")
            
            i = 1
            for row in rows:
                print(i, ": ", row[1])
                i += 1
            print("0: Cancel")
            deleteRow = input("\nSelect number ")
            if int(deleteRow) != 0:
                deleteFromWatchLater(id, rows[int(deleteRow) - 1][1], _conn)
        elif userInput == "3":
            clearTerminal()
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
    clearTerminal()
    print(filmName, "HAS BEEN DELETED FROM YOUR LIST.")
    input("Press enter to continue...")
    
    # Uncomment this to save the changes in the database
    # cur.commit()
    
    return 0

def filmDetails (filmName, _conn, year = 0, id = 0, ownedFilms = False):
    clearTerminal()
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
    if year != 0:
        testStatement = """
            SELECT * FROM (
                SELECT movieTitle as title, 
                    genre as genre, 
                    year as year, 
                    summary as summary, 
                    director as director, 
                    NULL as creator, 
                    runtime as runtime, 
                    null as seasons,
                    null as episodes 
                FROM movieDetails 
                WHERE movieTitle = ?
                    and year = ?
                UNION
                SELECT tvTitle as title, 
                    genre as genre, 
                    airDate as year, 
                    summary as summary, 
                    NULL as director, 
                    creator as creator, 
                    null as runtime, 
                    seasons as seasons, 
                    episodes as episodes 
                FROM tvDetails 
                WHERE tvTitle = ? 
                    and strftime('%Y', airDate) = ?)
                    """
        testArgs = [filmName, year, filmName, year]
    else:
        testStatement = """
            SELECT * FROM (
                SELECT movieTitle as title, 
                    genre as genre, 
                    year as year, 
                    summary as summary, 
                    director as director, 
                    NULL as creator, 
                    runtime as runtime, 
                    null as seasons,
                    null as episodes 
                FROM movieDetails 
                WHERE movieTitle = ?
                UNION
                SELECT tvTitle as title, 
                    genre as genre, 
                    airDate as year, 
                    summary as summary, 
                    NULL as director, 
                    creator as creator, 
                    null as runtime, 
                    seasons as seasons, 
                    episodes as episodes 
                FROM tvDetails 
                WHERE tvTitle = ? )
                    """
        testArgs = [filmName, filmName]
    cur.execute(testStatement, testArgs)
    rows = cur.fetchall()
    for row in rows:
        print(f"\nFilm Title: {row[0]}")
        print(f"Genre: {row[1]}")
        print(f"Release Year: {row[2]}")
        print(f"Summary: {row[3]}")
        if row[4] is None:
            print(f"Creator: {row[5]}")
        else:
            print(f"Director: {row[4]}")
        if row[6] is None:
            print(f"Seasons: {row[7]}")
            print(f"Episodes: {row[8]}")
        else:
            print(f"Runtime: {row[6]}")

    if ownedFilms: 
        statement = """select subLanguage, resolution 
            from Subtitles,
                OwnedFilms
            where OwnedFilms.userID = ?
                and Subtitles.filmName = ?
                and OwnedFilms.filmName = Subtitles.filmName;
                """
        subArgs =[id, filmName]
        cur.execute(statement, subArgs)
        subs = cur.fetchall()
        print("Subtiles: ", end="")
        for row in subs:
            print(row[0], end=" ")
        print("\nResolution: ", end="")
        for row in subs:
            print(row[1], end="p ")    
        print()
    
    availInPlat(id, _conn, filmName)
    
    input("\nPress enter to continue...")

    return 0

def availInPlat(id, _conn, filmName):
    cur = _conn.cursor()

    
    moviePlat = """
        select filmNetflix,
            filmHulu,
            filmPrime,
            filmDisney
        from streamingPlat,
            Users
        where Users.userID = ?
            and streamingPlat.filmTitle = ?;
    """
    args = [id, filmName]
    cur.execute(moviePlat, args)
    filmPlat = cur.fetchall()
    
    userPlat = """
        select netflix,
            hulu,
            amazonPrime,
            disney
        from Users
        where userID = ?"""
    args = [id]
    cur.execute(userPlat, args)
    avPlat = cur.fetchall()

    print(f"{filmName} is", end=" ")
    notFound = True
    if len(filmPlat) == 1:
        if avPlat[0][0] == 1 and filmPlat[0][0] == 1:
            if notFound:
                print("Netflix")
                notFound = False
            else:
                print("and Netflix")
        elif avPlat[0][1] == 1 and filmPlat[0][1] == 1:
            if notFound:
                print("Hulu")
                notFound = False
            else:
                print("and Hulu")
        elif avPlat[0][2] == 1 and filmPlat[0][2] == 1:
            if notFound:
                print("Amazon Prime")
                notFound = False
            else:
                print("and Amazon Prime")
        elif avPlat[0][3] == 1 and filmPlat[0][3] == 1:
            if notFound:
                print("Disney Plus")
                notFound = False
            else:
                print("and Disney Plus")
        else:
            print("not available in your current subscriptions")
    else:
       print("not available in your current subscriptions") 
    
    return 0


def searchFilm(id, add, toWatchList, toOwnedFilms, _conn):
    while True:
        clearTerminal()
        print("\033[1m" + "\nSelect film type\n0 to cancel" + "\033[0m")
        filmType = (input("TV Show or Movie? ")).upper()
        
        if filmType == "TV SHOW":
            searchTV(id, add, toWatchList, toOwnedFilms, _conn)
            return 0
        elif filmType == "MOVIE":
            searchMovie(id, add, toWatchList, toOwnedFilms, _conn)
            return 0
        elif filmType == "0":
            return 0
        else:
            print("Invalid Film Type!")

def searchTV(id, add, toWatchList, toOwnedFilms, _conn):
    while True:
        clearTerminal()
        print("\033[1m" + "\nWelcome to the TV Show database\nTo return back enter 0" + "\033[0m" )
        userFilter = input("Select how you want to search by (limit 4): \ntitle, seasons, episodes, showStatus, year, genre: ")
        if userFilter != "0":
            userFilter = re.split(r'[, ]', userFilter)
            userFilter = [word for word in userFilter if word]
            userInput = []
            i = 0
            for filters in userFilter:
                match filters.upper():
                    case 'TITLE':
                        userInput.append(input("Enter title: "))
                        userFilter[i] = "tvTitle"
                    case "SEASONS":
                        userInput.append(input("Enter how many seasons (least than and to): "))
                        userFilter[i] = "seasons"
                    case "EPISODES":
                        userInput.append(input("Enter how many episodes (least than and to): "))
                        userFilter[i] = "episodes"
                    case "SHOWSTATUS":
                        userInputTemp = input("Enter show status (returning or finished): ")
                        if userInputTemp.upper() == "RETURNING":
                            userInput.append("Returning Series")
                        elif userInputTemp.upper() == "FINISHED":
                            userInput.append("Ended") 
                        userFilter[i] = "showStatus"
                    case "YEAR":
                        userInput.append(input("Enter year: "))
                        userFilter[i] = "airDate"
                    case "GENRE":
                        userInput.append(input("Enter genre:"))
                        userFilter[i] = "genre"
                i += 1
            filterTV(id, userFilter, userInput, add, toWatchList, toOwnedFilms, _conn)
            return 0
        else:
            return 0


def searchMovie(id, add, toWatchList, toOwnedFilms, _conn):
    while True:
        clearTerminal()
        print("\033[1m" + "\nWelcome to the Movie database\nTo return back enter 0" + "\033[0m" )

        userFilter = input("Select how you want to search by: Title, director, genre, year, runtime, stars: ")
        if userFilter != "0":  
            #userFilter = userFilter.split(", ")
            userFilter = re.split(r'[, ]', userFilter)
            userFilter = [word for word in userFilter if word]
            userInput = []
            i = 0
            for filters in userFilter:
                match filters.upper():
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
                i = i + 1
            filterMovie(id, userFilter, userInput, add, toWatchList, toOwnedFilms, _conn)
            return 0
                
        else:
            return 0

def filterTV(id, userFilter, userInput, add, toWatchList, toOwnedFilms, _conn):
    cur = _conn.cursor()
    year = False
    like = False
    lessThan = False
    yearIndex = -1
    
    i = 0
    likeIndex = []
    lessThanIndex = []
    for attribute in userFilter:
        match attribute:
            case "airDate":
                year = True
                yearIndex = i
            case "tvTitle" | "showStatus" | "genre":
                like = True
                likeIndex.append(i)
            case "seasons" | "episodes":
                lessThan = True
                lessThanIndex.append(i)
        i += 1
        
    match len(userInput):
        case 1:
            if year:
                statement = f"""
                    select tvTitle from tvDetails
                    where strftime('%Y', {userFilter[yearIndex]}) = ?;
                """
                args = [userInput[yearIndex]]
            elif like:
                statement = f"""
                    select tvTitle from tvDetails
                    where {userFilter[0]} like ?;
                """
                args = [("%") + userInput[0] + ("%")]
            elif lessThan:
                statement = f"""
                    select tvTitle from tvDetails
                    where {userFilter[0]} <= ?;
                """
                args = [userInput[0]]
        case 2:
            if year:
                if like:
                    statement = f"""
                        select tvTitle from tvDetails
                        where strftime('%Y', {userFilter[yearIndex]}) = ?
                            and {userFilter[likeIndex[0]]} like ?;
                    """
                    args = [userInput[yearIndex], ("%") + userInput[likeIndex[0]] + ("%")]
                elif lessThan:
                    statement = f"""
                        select tvTitle from tvDetails
                        where strftime('%Y', {userFilter[yearIndex]}) = ?
                            and {userFilter[lessThanIndex[0]]} <= ?;
                    """
                    args = [userInput[yearIndex], userInput[lessThanIndex[0]]]
            else:
                if like and lessThan:
                    statement = f"""
                        select tvTitle from tvDetails
                        where {userFilter[likeIndex[0]]} like ?
                            and {userFilter[lessThanIndex[0]]} <= ?;
                    """
                    args = [ ("%") + userInput[likeIndex[0]] + ("%"), userInput[lessThanIndex[0]]]
                elif like and not lessThan:
                    statement = f"""
                        select tvTitle from tvDetails
                        where {userFilter[likeIndex[0]]} like ?
                            and {userFilter[likeIndex[1]]} like ?;
                    """
                    args = [ ("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%")]
                else:
                    statement = f"""select tvTitle from tvDetails
                        where {userFilter[lessThanIndex[0]]} <= ?
                            and {userFilter[lessThanIndex[1]]} <= ?;
                    """
                    args = [userInput[lessThanIndex[0]], userInput[lessThanIndex[1]]]                        
        case 3:
            if year:
                if like:
                    if lessThan:
                        statement = f"""
                        select tvTitle from tvDetails
                        where strftime('%Y', {userFilter[yearIndex]}) = ?
                            and {userFilter[likeIndex[0]]} like ?
                            and {userFilter[lessThanIndex[0]]} <= ?;
                        """
                        args = [userInput[yearIndex], ("%") + userInput[likeIndex[0]] + ("%"), userInput[lessThanIndex[0]]]
                    else:
                        statement = f"""
                        select tvTitle from tvDetails
                        where strftime('%Y', {userFilter[yearIndex]}) = ?
                            and {userFilter[likeIndex[0]]} like ?
                            and {userFilter[likeIndex[1]]} like ?;
                        """
                        args = [userInput[yearIndex], ("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%")]
                elif lessThan:
                    statement = f"""
                    select tvTitle from tvDetails
                    where strftime('%Y', {userFilter[yearIndex]}) = ?
                        and {userFilter[lessThanIndex[0]]} <= ?
                        and {userFilter[lessThanIndex[1]]} <= ?;
                    """
                    args = [userInput[yearIndex], userInput[lessThanIndex[0]], userInput[lessThanIndex[1]]]
            else:
                if like and len(likeIndex) == 2:
                    statement = f"""
                    select tvTitle from tvDetails
                    where {userFilter[lessThanIndex[0]]} <= ?
                        and {userFilter[likeIndex[0]]} like ?
                        and {userFilter[likeIndex[1]]} like ?;
                    """
                    args = [userInput[lessThanIndex[0]], ("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%")]
                else:
                    statement = f"""
                    select tvTitle from tvDetails
                    where {userFilter[lessThanIndex[0]]} <= ?
                        and {userFilter[lessThanIndex[1]]} <= ?
                        and {userFilter[likeIndex[0]]} like ?;
                    """
                    args = [userInput[lessThanIndex[0]], userInput[lessThanIndex[1]], ("%") + userInput[likeIndex[0]] + ("%")]                                   
        case 4:
            if year:
                if like:
                    if lessThan and len(lessThanIndex) == 2:
                        statement = f"""
                        select tvTitle from tvDetails
                        where {userFilter[lessThanIndex[0]]} <= ?
                            and {userFilter[lessThanIndex[1]]} <= ?
                            and {userFilter[likeIndex[0]]} like ?
                            and strftime('%Y', {userFilter[yearIndex]}) = ?;
                        """
                        args = [userInput[lessThanIndex[0]], userInput[lessThanIndex[1]], ("%") + userInput[likeIndex[0]] + ("%"), userInput[yearIndex]]
                    elif lessThan and len(likeIndex) == 2:
                        statement = f"""
                        select tvTitle from tvDetails
                        where {userFilter[lessThanIndex[0]]} <= ?
                            and {userFilter[likeIndex[0]]} like ?
                            and {userFilter[likeIndex[1]]} like ?
                            and strftime('%Y', {userFilter[yearIndex]}) = ?;
                        """
                        args = [userInput[lessThanIndex[0]], ("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%"), userInput[yearIndex]]
                    elif len(likeIndex) == 3:
                        statement = f"""
                        select tvTitle from tvDetails
                        where {userFilter[likeIndex[0]]} like ?
                            and {userFilter[likeIndex[1]]} like ?
                            and {userFilter[likeIndex[2]]} like ?
                            and strftime('%Y', {userFilter[yearIndex]}) = ?;
                        """
                        args = [("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%"), ("%") + userInput[likeIndex[2]] + ("%"), userInput[yearIndex]]
                else:
                    if len(lessThanIndex) == 2 and len(likeIndex) == 2:
                        statement = f"""
                        select tvTitle from tvDetails
                        where {userFilter[lessThanIndex[0]]} <= ?
                            and {userFilter[likeIndex[0]]} like ?
                            and {userFilter[likeIndex[1]]} like ?
                            and {userFilter[lessThanIndex[1]]} <= ?
                        """
                        args = [userInput[lessThanIndex[0]], ("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%"), userInput[lessThanIndex[1]]]
                    elif len(lessThanIndex) == 1 and len(likeIndex) == 3:
                        statement = f"""
                        select tvTitle from tvDetails
                        where {userFilter[likeIndex[0]]} like ?
                            and {userFilter[likeIndex[1]]} like ?
                            and {userFilter[likeIndex[2]]} like ?
                            and {userFilter[lessThanIndex[0]]} <= ?
                        """
                        args = [("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%"), ("%") + userInput[likeIndex[2]] + ("%"), userInput[lessThanIndex[0]]]                                  
        case 5:
            if year:
                if like:
                    if len(lessThanIndex) == 2 and len(likeIndex) == 2:
                        statement = f"""
                        select tvTitle from tvDetails
                        where {userFilter[likeIndex[0]]} like ?
                            and {userFilter[likeIndex[1]]} like ?
                            and {userFilter[lessThanIndex[0]]} <= ?
                            and {userFilter[lessThanIndex[1]]} <= ?
                            and strftime('%Y', {userFilter[yearIndex]}) = ?;
                        """
                        args = [("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%"), userInput[lessThanIndex[0]], userInput[lessThanIndex[1]], userInput[yearIndex]]     
                    elif len(lessThanIndex) == 1 and len(likeIndex) == 3:
                        statement = f"""
                        select tvTitle from tvDetails
                        where {userFilter[likeIndex[0]]} like ?
                            and {userFilter[likeIndex[1]]} like ?
                            and {userFilter[likeIndex[2]]} like ?
                            and {userFilter[lessThanIndex[0]]} <= ?
                            and strftime('%Y', {userFilter[yearIndex]}) = ?;
                        """
                        args = [("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%"), ("%") + userInput[likeIndex[2]] + ("%"), userInput[lessThanIndex[0]], userInput[yearIndex]] 
            else:
                if len(lessThanIndex) == 2 and len(likeIndex) == 3:
                        statement = f"""
                        select tvTitle from tvDetails
                        where {userFilter[likeIndex[0]]} like ?
                            and {userFilter[likeIndex[1]]} like ?
                            and {userFilter[likeIndex[2]]} like ?
                            and {userFilter[lessThanIndex[0]]} <= ?
                            and {userFilter[lessThanIndex[1]]} <= ?;
                        """
                        args = [("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%"), ("%") + userInput[likeIndex[2]] + ("%"), userInput[lessThanIndex[0]], userInput[lessThanIndex[1]]]                                 
        case 6: 
            statement = f"""
                select tvTitle from tvDetails
                where {userFilter[likeIndex[0]]} like ?
                    and {userFilter[likeIndex[1]]} like ?
                    and {userFilter[likeIndex[2]]} like ?
                    and {userFilter[lessThanIndex[0]]} <= ?
                    and {userFilter[lessThanIndex[1]]} <= ?
                    and strftime('%Y', {userFilter[yearIndex]}) = ?;
                """
            args = [("%") + userInput[likeIndex[0]] + ("%"), ("%") + userInput[likeIndex[1]] + ("%"), ("%") + userInput[likeIndex[2]] + ("%"), userInput[lessThanIndex[0]], userInput[lessThanIndex[1]], userInput[yearIndex]] 
    cur.execute(statement, args)
    rows = cur.fetchall()
    while True:     
        clearTerminal()               
        print("\033[1m" + "\nResults:" "\033[0m")
        i = 1
        for row in rows:
            print(f"{row[0]}")
            i += 1
        
        print("\n\033[1m" + "Options:" + "\033[0m")
        userInput = input("1. More detail on film\n2. Add film\n3: Search Again\n0: Cancel Search\n Enter option: ")
        if userInput == "1":
            clearTerminal()               
            print("\033[1m" + "\nResults:" + "\033[0m")
            i = 1
            for row in rows:
                print(f"{i}: {row[0]}")
                i += 1
            numFilm = input("\nWhich film # do you want see more detail about (0 to cancel): ")
            if int(numFilm) > 0 and int(numFilm) < i:
                getYear = """select strftime('%Y', airDate) from tvDetails
                    where tvTitle = ?;"""
                args = [rows[int(numFilm) - 1][0]]
                cur.execute(getYear, args)
                yearResult = cur.fetchall()
                filmDetails(rows[int(numFilm) - 1][0], _conn, yearResult[0][0])
        elif userInput == "2":
            if add:
                clearTerminal()               
                print("\033[1m" + "\nResults:" + "\033[0m")
                i = 1
                for row in rows:
                    print(f"{i}: {row[0]}")
                    i += 1
                addFilm = input("\nWhich film # do you want to add (0 to cancel): ")
                if toWatchList: 
                        if int(addFilm) > 0 and int(addFilm) < i:
                            addToWatchLater(id, rows[int(addFilm) - 1][0], _conn)
                            return 0
                if toOwnedFilms:
                    if int(addFilm) >  0 and int(addFilm) < i:
                        resolution = input("Enter resolution of film (0 for none): ")
                        subtitles = input("Enter subtitle language (0 for none): ")
                        addToOwnedFilm(id, rows[int(addFilm) - 1][0], resolution, subtitles, _conn)
                        return 0
        elif userInput == "3":
            searchTV(id, add, toWatchList, toOwnedFilms, _conn)
            return 0
        elif userInput == "0":
            return 0  
    return 0

def filterMovie(id, userFilter, userInput, add, toWatchList, toOwnedFilms, _conn):
    cur = _conn.cursor()
    runtime = False
    runtimeIndex = -1
    match len(userInput):
        case 1:
            i = 0
            for attribute in userFilter:
                if attribute == "runtime":
                    runtime = True
                    runtimeIndex = i
                i += 1
            if runtime:
                statement = f"select movieTitle, year from movieDetails where {userFilter[runtimeIndex]} < ?;"
                args = [userInput[runtimeIndex]]
            else:  
                statement = f"select movieTitle, year from movieDetails where {userFilter[0]} like ?;"
                args = [("%") + userInput[0] + ("%")]
        case 2:
            i = 0
            for attribute in userFilter:
                if attribute == "runtime":
                    runtime = True
                    runtimeIndex = i
                i += 1
            if runtime:
                index = []
                for x in range(len(userFilter) + 1):
                    if x != runtimeIndex:
                        index.append(x)
                statement = f"select movieTitle, year from movieDetails where {userFilter[runtimeIndex]} < ? and {userFilter[index[0]]} like ?;"
                args = [userInput[runtimeIndex], ("%") + userInput[index[0]] + ("%")]
            else:
                statement = f"select movieTitle, year from movieDetails where {userFilter[0]} like ? and {userFilter[1]} like ?;"
                args = [("%") + userInput[0] + ("%"), ("%") + userInput[1] + ("%")]
        case 3: 
            i = 0
            for attribute in userFilter:
                if attribute == "runtime":
                    runtime = True
                    runtimeIndex = i
                i += 1
            if runtime:
                index = []
                for x in range(len(userFilter) + 1):
                    if x != runtimeIndex:
                        index.append(x)
                statement = f"""select movieTitle, year from movieDetails where {userFilter[runtimeIndex]} < ?
                    and {userFilter[index[0]]} like ?
                    and {userFilter[index[1]]} like ?;"""
                args = [userInput[runtimeIndex], ("%") + userInput[index[0]] + ("%"), ("%") + userInput[index[1]] + ("%")]
            else:
                statement = f"""select movieTitle, year from movieDetails where {userFilter[0]} like ?
                and {userFilter[1]} like ?
                and {userFilter[2]} like ?;"""
                args = [("%") + userInput[0] + ("%"), ("%") + userInput[1] + ("%"), ("%") + userInput[2] + ("%")]
        case 4:
            i = 0
            for attribute in userFilter:
                if attribute == "runtime":
                    runtime = True
                    runtimeIndex = i
                i += 1
            if runtime:
                index = []
                for x in range(len(userFilter) + 1):
                    if x != runtimeIndex:
                        index.append(x)
                statement = f"""select movieTitle, year from movieDetails where {userFilter[runtimeIndex]} < ?
                    and {userFilter[index[0]]} like ?
                    and {userFilter[index[1]]} like ?
                    and {userFilter[index[2]]} like ?;"""
                args = [userInput[runtimeIndex], ("%") + userInput[index[0]] + ("%"), ("%") + userInput[index[1]] + ("%"), ("%") + userInput[index[2]] + ("%")]
            else:
                statement = f"""select movieTitle, year from movieDetails where {userFilter[0]} like ?
                    and {userFilter[1]} like ?
                    and {userFilter[2]} like ?
                    and {userFilter[3]} like ?;"""
                args = [("%") + userInput[0] + ("%"), ("%") + userInput[1] + ("%"), ("%") + userInput[2] + ("%"), ("%") + userInput[3] + ("%")]      
        case 5:
            i = 0
            for attribute in userFilter:
                if attribute == "runtime":
                    runtime = True
                    runtimeIndex = i
                i += 1
            if runtime:
                index = []
                for x in range(len(userFilter) + 1):
                    if x != runtimeIndex:
                        index.append(x)
                statement = f"""select movieTitle, year from movieDetails where {userFilter[runtimeIndex]} like ?
                    and {userFilter[index[0]]} like ?
                    and {userFilter[index[1]]} like ?
                    and {userFilter[index[2]]} like ?
                    and {userFilter[index[3]]} like ?;"""
                args = [userInput[runtimeIndex], ("%") + userInput[index[0]] + ("%"), ("%") + userInput[index[1]] + ("%"), ("%") + userInput[index[2]] + ("%"), ("%") + userInput[index[3]] + ("%")]
            else:
                statement = f"""select movieTitle, year from movieDetails where {userFilter[0]} like ?
                    and {userFilter[1]} like ?
                    and {userFilter[2]} like ?
                    and {userFilter[3]} like ?
                    and {userFilter[4]} like ?;"""
                args = [("%") + userInput[0] + ("%"), ("%") + userInput[1] + ("%"), ("%") + userInput[2] + ("%"), ("%") + userInput[3] + ("%"), ("%") + userInput[4] + ("%")]
        case 6:
            i = 0
            for attribute in userFilter:
                if attribute == "runtime":
                    runtime = True
                    runtimeIndex = i
                i += 1
            if runtime:
                index = []
                for x in range(len(userFilter) + 1):
                    if x != runtimeIndex:
                        index.append(x)
                statement = f"""select movieTitle, year from movieDetails where {userFilter[runtimeIndex]} < ?
                    and {userFilter[index[0]]} like ?
                    and {userFilter[index[1]]} like ?
                    and {userFilter[index[2]]} like ?
                    and {userFilter[index[3]]} like ?
                    and {userFilter[index[4]]} like ?;"""
                args = [userInput[runtimeIndex], ("%") + userInput[index[0]] + ("%"), ("%") + userInput[index[1]] + ("%"), ("%") + userInput[index[2]] + ("%"), ("%") + userInput[index[3]] + ("%"), ("%") + userInput[index[4]] + ("%")]
            else:
                tatement = f"""select movieTitle, year from movieDetails where {userFilter[0]} like ?
                    and {userFilter[1]} like ?
                    and {userFilter[2]} like ?
                    and {userFilter[3]} like ?
                    and {userFilter[4]} like ?
                    and {userFilter[5]} like ?;"""
                args = [("%") + userInput[0] + ("%"), ("%") + userInput[1] + ("%"), ("%") + userInput[2] + ("%"), ("%") + userInput[3] + ("%"), ("%") + userInput[4] + ("%"), ("%") + userInput[5] + ("%")]
        
    cur.execute(statement, args)
    rows = cur.fetchall()
    while True:       
        clearTerminal()             
        print("\033[1m" + "\nResults:" + "\033[0m" )
        i = 1
        for row in rows:
            print(f"{row[0]}")
            i += 1
        
        print("\n\033[1m" + "Options:" + "\033[0m")
        userInput = input("1. More detail on film\n2. Add film\n3: Search Again\n0: Cancel Search\n Enter option: ")
        if userInput == "1":
                clearTerminal()
                i = 1
                print("\033[1m" + "\nResults:" + "\033[0m" )
                for row in rows:
                    print(f"{i}: {row[0]}")
                    i += 1
                numFilm = input("\nWhich film # do you want see more detail about: ")
                if int(numFilm) > 0 and int(numFilm) < i:
                    getYear = """select year from movieDetails
                            where movieTitle = ?;"""
                    args = [rows[int(numFilm) - 1][0]]
                    cur.execute(getYear, args)
                    yearResult = cur.fetchall()
                    filmDetails(rows[int(numFilm) - 1][0], _conn, yearResult[0][0])
        elif userInput == "2":
            if add:
                clearTerminal()
                i = 1
                print("\033[1m" + "\nResults:" + "\033[0m" )
                for row in rows:
                    print(f"{i}: {row[0]}")
                    i += 1
                addFilm = input("\nWhich film # do you want to add (0 to cancel): ")
                if toWatchList: 
                        if int(addFilm) > 0 and int(addFilm) < i:
                            addToWatchLater(id, rows[int(addFilm) - 1][0], _conn)
                            return 0
                if toOwnedFilms:
                    if int(addFilm) >  0 and int(addFilm) < i:
                        resolution = input("Enter resolution of film (0 for none): ")
                        subtitles = input("Enter subtitle language (0 for none): ")
                        addToOwnedFilm(id, rows[int(addFilm) - 1][0], resolution, subtitles, _conn)
                        return 0
        elif userInput == "3":
            searchMovie(id, add, toWatchList, toOwnedFilms, _conn)
            return 0
        elif userInput == "0":
            return 0  
    
    return 0

def addToOwnedFilm(id, filmTitle, resolution, subtitles, _conn):
    cur = _conn.cursor()
    statement = "insert into OwnedFilms values (?, ? , ?)"
    args = [id, filmTitle, resolution]
    cur.execute(statement, args)
    
    if subtitles != "0":
        statement = "insert into Subtitles values (?, ?)"
        args = [filmTitle, subtitles]
        cur.execute(statement, args)
    clearTerminal()
    print(filmTitle, "HAS BEEN ADDED TO OWNED FILMS")
    input("Press enter to continue...")
    
    # Uncomment to commit
    # cur.commit()
    
    return 0

def addToWatchLater(id, filmTitle, _conn):
    cur = _conn.cursor()
    statement = """
        insert into WatchLater values (?, ?)
    """
    args = [id, filmTitle]
    cur.execute(statement, args)
    clearTerminal()
    print(filmTitle, " HAS BEEN ADDED TO WATCH LATER")
    input("Press enter to continue...")
    
    # Uncomment to commit
    # cur.commit()
    
    return 0

def streamPlat(id, _conn):
    while True:
        clearTerminal()
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
    clearTerminal()
    print("------------------------------------------")
    print("SEARCH ACROSS OWNED PLATFORMS:")
    while True:
        print("\033[1m" + "\nSelect film type" + "\033[0m")
        print("\033[1m" + "Enter 0 to cancel" + "\033[0m")
        filmType = (input("1. TV show \n2. Movie \nEnter option: ")).upper()
        
        if filmType == "1":
            searchPlatFilm(id, filmType, _conn)
        elif filmType == "2":
            searchPlatFilm(id, filmType, _conn)
        elif filmType == "0":
            return
        else:
            print("Invalid Input")

def searchPlatFilm(id, type, _conn):
    if type == "1":
        filmType = "Tv Show"
        fType = 1
        while True:
            choice = input("\nSearch by %s's \n1. Title \n2. Year \n3. Genre \n0. return \nEnter option: " % (filmType))
            if choice == "0":
                return 0
            if choice == "1":
                title = input("0 to return or Enter %s's Title: " % (filmType)).upper()
                if title == "0":
                    continue
                else:
                    searchPlatFilmTitle(id, fType, title, _conn)
            if choice == "2":
                title = input("0 to return or Enter %s's Year: " % (filmType)).upper()
                if title == "0":
                    continue
                else:
                    searchPlatFilmYear(id, fType, title, _conn)
            if choice == "3":
                title = input("0 to return or Enter %s's Genre: " % (filmType)).upper()
                if title == "0":
                    continue
                else:
                    searchPlatFilmGenre(id, fType, title, _conn)
    if type == "2":
        filmType = "Movie"
        fType = 0
        while True:
            choice = input("\nSearch by %s's \n1. Title \n2. Year \n3. Genre \n0. return \nEnter option: " % (filmType))
            if choice == "0":
                return 0
            if choice == "1":
                title = input("0 to return or Enter %s's Title: " % (filmType)).upper()
                if title == "0":
                    continue
                else:
                    searchPlatFilmTitle(id, fType, title, _conn)
            if choice == "2":
                title = input("0 to return or Enter %s's Year: " % (filmType)).upper()
                if title == "0":
                    continue
                else:
                    searchPlatFilmYear(id, fType, title, _conn)
            if choice == "3":
                title = input("0 to return or Enter %s's Genre: " % (filmType)).upper()
                if title == "0":
                    continue
                else:
                    searchPlatFilmGenre(id, fType, title, _conn)

def searchPlatFilmGenre(id, ftype, title, _conn):
    p_list = {}
    if ftype == "0":
        filmTable = "movieDetails"
        filmTitle = "movieTitle"
    elif ftype == "1":
        filmTable = "tvDetails"
        filmTitle = "tvTitle"
    genres = title.split()
    count = 0
    for genre in genres:
        new_genre = "%" + genre + "%"
        genres[count] = "f.genre like " + new_genre
        count += 1
    print(genres)
    if len(genres) == 1 and ftype == 0:
        statement = f"""SELECT u.filmTitle, f.genre
                        FROM Users u, streamingPlat p, ? f
                        WHERE u.filmTitle = f.?
                            AND u.ID = ?
                            AND 
                            AND {genre[0]}""" # making the search through the genre and joins the 3 tables using platform and titles


def searchPlatFilmYear(id, ftype, title, _conn):
    print("2")

def searchPlatFilmTitle(id, fType, title, _conn):
    p_list = {}
    title = '%' + title + '%'
    statement = """SELECT filmTitle
                    FROM streamingPlat, Users
                    WHERE UPPER(filmTitle) like ? 
                        AND filmPrime = amazonPrime
                        AND amazonPrime = 1
                        AND userID = ?
                        AND filmType = ?"""
    args = [title, id, fType]
    cur = _conn.cursor()
    cur.execute(statement, args)
    rows = cur.fetchall()
    if rows:
        for row in rows:
            p_list[row[0]] = []
            p_list[row[0]].append("in Amazon Prime")
    
    statement = """SELECT filmTitle
                    FROM streamingPlat, Users
                    WHERE UPPER(filmTitle) like ? 
                        AND filmHulu = hulu
                        AND hulu = 1
                        AND userID = ?
                        AND filmType = ?"""
    args = [title, id, fType]
    cur = _conn.cursor()
    cur.execute(statement, args)
    rows = cur.fetchall()
    if rows:
        for row in rows:
            if row[0] in p_list:
                p_list[row[0]].append("in Hulu")
            else:
                p_list[row[0]] = []
                p_list[row[0]].append("in Hulu")

    statement = """SELECT filmTitle
                    FROM streamingPlat, Users
                    WHERE UPPER(filmTitle) like ? 
                        AND filmNetflix = netflix
                        AND netflix = 1
                        AND userID = ?
                        AND filmType = ?"""
    args = [title, id, fType]
    cur = _conn.cursor()
    cur.execute(statement, args)
    rows = cur.fetchall()
    if rows:
        for row in rows:
            if row[0] in p_list:
                p_list[row[0]].append("in Netflix")
            else:
                p_list[row[0]] = []
                p_list[row[0]].append("in Netflix")

    statement = """SELECT filmTitle
                    FROM streamingPlat, Users
                    WHERE UPPER(filmTitle) like ? 
                        AND filmDisney = disney
                        AND disney = 1
                        AND userID = ?
                        AND filmType = ?"""
    args = [title, id, fType]
    cur = _conn.cursor()
    cur.execute(statement, args)
    rows = cur.fetchall()
    if rows:
        for row in rows:
            if row[0] in p_list:
                p_list[row[0]].append("in Disney+")
            else:
                p_list[row[0]] = []
                p_list[row[0]].append("in Disney+")

    for key, values in p_list.items():
        print("\n------------------------------------------")
        print(f"{key} {' '.join(values)}")


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
.mode list

-- Delete
DELETE FROM Users;
DELETE FROM OwnedFilms;
DELETE FROM Subtitles;
DELETE FROM WatchLater;


-- Add User 
INSERT INTO Users VALUES(1001, 'Jose Cano', 1, 0, 1, 1);

-- Add films owned by user
INSERT INTO OwnedFilms VALUES(1001, 'The Dark Knight', 1080);
INSERT INTO OwnedFilms VALUES(1001, 'The Dark Knight Rises', 1080);
INSERT INTO OwnedFilms VALUES(1001, 'Terminator 2: Judgment Day', 2160);
INSERT INTO OwnedFilms VALUES(1001, 'Guardians of the Galaxy Vol. 3', 720);

-- Add to watch later based on user
INSERT INTO WatchLater VALUES(1001, 'Scott Pilgrim vs. the World');
INSERT INTO WatchLater VALUES(1001, 'Kill Bill: Vol. 2');
INSERT INTO WatchLater VALUES(1001, 'Avatar');


-- Add subtitles from user 
INSERT INTO Subtitles VALUES('The Dark Knight', 'english');
INSERT INTO Subtitles VALUES('The Dark Knight', 'spanish');
INSERT INTO Subtitles VALUES('The Dark Knight', 'french');
INSERT INTO Subtitles VALUES('The Dark Knight Rises', 'english');
INSERT INTO Subtitles VALUES('Terminator 2: Judgment Day', 'russian');

-- Displaying films that is offered by Hulu, Prime, and Disney+
SELECT filmTitle 
FROM streamingPlat 
WHERE filmHulu = 1 
    and filmPrime = 1 
    and filmDisney = 1;

--Display TV Shows that stared and ended in the year 2021
SELECT tvTitle
FROM tvDetails
WHERE showStatus = 'Ended'
    AND airDate like '2021-%'
    AND lastDate like '2021-%';
-- Retrieve ratings, genre, and summary from Owned Films along with the film name
SELECT filmName, rating, genre, summary
FROM OwnedFilms, movieDetails
WHERE filmName = movieTitle;

--Searching up all film details available from a specified movie in the watch later list
SELECT *
FROM movieDetails
WHERE movieTitle = (SELECT filmName
                    FROM WatchLater
                    WHERE filmName = 'Avatar');

-- Display Movies That are only on Hulu
SELECT filmTitle
FROM streamingPlat
WHERE filmType = 0
    AND filmHulu = 1
    AND filmDisney = 0
    AND filmPrime= 0
    AND filmNetflix = 0;

---- Display TvShows That are only on Hulu and Prime along with their genre
SELECT filmTitle, genre
FROM streamingPlat, tvDetails
WHERE filmType = 1
    AND filmHulu = 1
    AND filmDisney = 0
    AND filmPrime= 1
    AND filmNetflix = 0
    AND tvTitle = filmTitle;


-- Update streaming platform from user
UPDATE Users
SET disney = 0
WHERE userID = 1001;

-- Remove film from watch later
DELETE FROM WatchLater 
WHERE userID = 1001 AND
    filmName LIKE "Kill%";

-- Remove subtitle 
DELETE FROM Subtitles
WHERE filmName = 'The Dark Knight' AND
    subLanguage = 'french';

-- Display Users
SELECT *
FROM Users;

-- Display Watch Later
SELECT *
FROM WatchLater;

-- Display OwnedFilms
SELECT * 
FROM OwnedFilms;

-- Display Subtitles
SELECT * 
FROM Subtitles;

-- Find directors that made a film in 2008 that Jose Cano own
SELECT director
FROM movieDetails m,
    OwnedFilms o,
    Users u
WHERE
    u.userName = 'Jose Cano' AND
    u.userID = o.userID AND
    o.filmName = m.movieTitle AND
    year = 2008;

-- Add Movie from movieDetails 
INSERT INTO WatchLater (userID, filmName)
SELECT 1001, movieTitle
FROM movieDetails
WHERE movieTitle LIKE 'Fight Club';

-- Display Watch Later
SELECT *
FROM WatchLater;

-- Select tv shows that are on netflix, completed, and scripted
SELECT tv.tvTitle
FROM tvDetails tv,
    streamingPlat s
WHERE
    tv.tvTitle = s.filmTitle AND
    s.filmNetflix = 1 AND
    tv.showStatus = 'Ended' AND
    tv.showType = 'Scripted'
LIMIT 10;

SELECT o.filmName, m.imdbRating
FROM OwnedFilms o,
    movieDetails m,
    Users u
WHERE u.userID = o.userID AND
    u.userName = 'Jose Cano' AND
    o.filmName = m.movieTitle AND
    m.director LIKE 'Christopher%';
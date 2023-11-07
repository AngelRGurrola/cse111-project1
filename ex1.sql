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
----
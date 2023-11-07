.header ON
.mode csv

--SQLite
DROP TABLE IF EXISTS Subtitles;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS OwnedFilms;
DROP TABLE IF EXISTS WatchLater;
DROP TABLE IF EXISTS movieDetails;
DROP Table IF EXISTS tvDetails;
DROP TABLE IF EXISTS streamingPlat;

CREATE TABLE streamingPlat (
    u_ID INTEGER not null,
    filmID INTEGER not null,
    filmTitle varchar(152) not null,
    filmYear INTEGER not null,
    filmAge varchar(5),
    filmRottenTomatoe varchar(10) not null,
    filmNetflix INTEGER not null,
    filmHulu INTEGER not null,
    filmPrime INTEGER not null,
    filmDisney INTEGER not null,
    filmType INTEGER not null
);

.import "films.csv" streamingPlat

CREATE TABLE Subtitles (
    filmName VARCHAR(152) NOT NULL,
    subLanguage CHAR(25) NOT NULL
);

CREATE TABLE Users (
    userID INTEGER PRIMARY KEY,
    userName VARCHAR(25) NOT NULL,
    amazonPrime INTEGER,
    hulu INTEGER,
    netflix INTEGER,
    disney INTEGER
);

CREATE TABLE OwnedFilms (
    userID INTEGER,
    filmName VARCHAR(152) NOT NULL,
    resolution INTEGER
);

CREATE TABLE WatchLater (
    userID INTEGER,
    filmName VARCHAR(152) NOT NULL
);

CREATE TABLE movieDetails (
    posterLink VARCHAR(200) NOT NULL,
    movieTitle VARCHAR(152) NOT NULL,
    year INTEGER NOT NULL,
    rating CHAR(2) NOT NULL,
    runtime VARCHAR(10) NOT NULL,
    genre CHAR(10) NOT NULL,
    imdbRating FLOAT NOT NULL,
    summary VARCHAR(500) NOT NULL,
    metaScore INTEGER NOT NULL,
    director VARCHAR(50) NOT NULL,
    star1 VARCHAR(50) NOT NULL,
    star2 VARCHAR(50) NOT NULL,
    star3 VARCHAR(50) NOT NULL,
    star4 VARCHAR(50) NOT NULL,
    noVotes INTEGER NOT NULL,
    gross VARCHAR(50) NOT NULL
);
.import "imdb_top_1000.csv" movieDetails

CREATE TABLE tvDetail(
    id INTEGER NOT NULL,
    tvTitle VARCHAR(152) NOT NULL,
    seasons INTEGER NOT NULL,
    episodes INTEGER NOT NULL,
    oriLang CHAR(10) NOT NULL,
    voteCount INTEGER NOT NULL,
    voteAvg FLOAT NOT NULL, 
    summary VARCHAR(500) NOT NULL,
    rating CHAR(5) NOT NULL,
    backdropLink VARCHAR(50) NOT NULL,
    airDate CHAR(10) NOT NULL,
    lastDate CHAR(10) NOT NULL,
    homepage CHAR(50),
    inProduction CHAR(5) NOT NULL,
    orgTitle VARCHAR(152) NOT NULL,
    populatity FLOAT NOT NULL,
    posterLink VARCHAR(152),
    showType VARCHAR(50) NOT NULL,
    showStatus VARCHAR(50) NOT NULL,
    tagline VARCHAR(500),
    genre VARCHAR(150),
    creator VARCHAR(100),
    lang VARCHAR(50),
    networks VARCHAR(50),
    origin CHAR(5),
    spokenLang VARCHAR(50),
    prodCompany VARCHAR(100),
    prodCountry VARCHAR(50),
    epiRuntime INTEGER
);

.import "TMDB_tv_dataset_v3.csv" tvDetail

CREATE TABLE IF NOT EXISTS album 
(
	album_id INT PRIMARY KEY,
	name varchar(40) NOT NULL,
	year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS track 
(
	track_id INT PRIMARY KEY,
	name varchar(40) NOT NULL,
	duration INT NOT NULL,
	fk_album_id INT REFERENCES album(album_id)
);

CREATE TABLE IF NOT EXISTS collection
(
	collection_id INT PRIMARY KEY,
	name varchar(40) NOT NULL,
	year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS artist
(
	artist_id INT PRIMARY KEY,
	name varchar(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS genre
(
	genre_id INT PRIMARY KEY,
	name varchar(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS track_collection
(
	track_id INT REFERENCES track(track_id),
	collection_id INT REFERENCES collection(collection_id),
	CONSTRAINT track_collection_id_pkey PRIMARY KEY (track_id, collection_id)
);

CREATE TABLE IF NOT EXISTS album_artist
(
	album_id INT REFERENCES album(album_id),
	artist_id INT REFERENCES artist(artist_id),
	CONSTRAINT album_artist_id_pkey PRIMARY KEY (album_id, artist_id)
);

CREATE TABLE IF NOT EXISTS artist_genre
(
	artist_id INT REFERENCES artist(artist_id),
	genre_id INT REFERENCES genre(genre_id),
	CONSTRAINT album_genre_id_pkey PRIMARY KEY (artist_id, genre_id)
);

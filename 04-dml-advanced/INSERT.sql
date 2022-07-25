-- genre
INSERT INTO genre
VALUES 
(1, 'pop'),
(2, 'alternative'),
(3, 'jazz'),
(4, 'classical'),
(5, 'electronic');

-- artist
INSERT INTO artist
VALUES 
(1, 'artist1'),
(2, 'artist2'),
(3, 'artist3'),
(4, 'artist4'),
(5, 'artist 5'),
(6, 'artist 6'),
(7, 'artist 7'),
(8, 'artist 8');

-- album
INSERT INTO album
VALUES 
(1, 'album1', 1994),
(2, 'album2', 2000),
(3, 'album3', 2018),
(4, 'album4', 2022),
(5, 'album5', 2002),
(6, 'album6', 2019),
(7, 'album7', 2019),
(8, 'album8', 1997);

-- track
INSERT INTO track
VALUES 
(1, 'track1', 2, 1),
(2, 'track2', 3, 1),
(3, 'track3', 4, 2),
(4, 'track4', 4, 2),
(5, 'track5', 3, 3),
(6, 'track6', 5, 3),
(7, 'my track7', 7, 4),
(8, 'мой track8', 2, 4),
(9, 'track9', 3, 5),
(10, 'мой track10', 4, 5),
(11, 'track11', 6, 6),
(12, 'track12', 5, 6),
(13, 'track13', 3, 7),
(14, 'track14', 4, 7),
(15, 'track15', 2, 8),
(16, 'track16', 3, 1);

-- collection
INSERT INTO collection
VALUES 
(1, 'collecton1', 2020),
(2, 'collecton2', 2020),
(3, 'collecton3', 2021),
(4, 'collecton4', 2021),
(5, 'collecton5', 2021),
(6, 'collecton6', 2022),
(7, 'collecton7', 2022),
(8, 'collecton8', 2022);

-- artist_genre
INSERT INTO artist_genre
VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 1),
(7, 2),
(8, 3);

-- album_artist
INSERT INTO album_artist
VALUES 
(1, 1),
(1, 2),
(2, 2),
(3, 3),
(4, 4),
(4, 5),
(5, 5),
(6, 6),
(7, 7),
(8, 7);

-- track_collection
INSERT INTO track_collection
VALUES 
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 2),
(6, 2),
(7, 3),
(8, 3),
(9, 4),
(10, 4),
(11, 5),
(12, 5),
(13, 6),
(14, 6),
(15, 7),
(1, 7),
(2, 7),
(3, 7),
(4, 8),
(5, 8);




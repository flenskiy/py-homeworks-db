-- название и год выхода альбомов, вышедших в 2018 году;
SELECT name, year FROM album
WHERE year = 2018;

-- название и продолжительность самого длительного трека;
SELECT name, duration FROM track
WHERE duration = (SELECT MAX(duration) FROM track);

-- название и продолжительность самого длительного трека;
SELECT name FROM track
WHERE duration >= 3.5;

-- исполнители, чье имя состоит из 1 слова;
SELECT name FROM artist
WHERE name NOT LIKE '% %';

-- название треков, которые содержат слово "мой"/"my".
SELECT name FROM track
WHERE name LIKE '%my%' OR name LIKE '%мой%';
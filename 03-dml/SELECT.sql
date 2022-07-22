-- 1. название и год выхода альбомов, вышедших в 2018 году;
SELECT name, year FROM album
WHERE year = 2018;

-- 2. название и продолжительность самого длительного трека;
SELECT name, duration FROM track
WHERE duration = (SELECT MAX(duration) FROM track);

-- 3. название треков, продолжительность которых не менее 3,5 минуты;
SELECT name FROM track
WHERE duration >= 3.5;

-- 4. названия сборников, вышедших в период с 2018 по 2020 год включительно;
SELECT name FROM collection
WHERE year >= 2018 AND year <= 2020;

-- 5. исполнители, чье имя состоит из 1 слова;
SELECT name FROM artist
WHERE name NOT LIKE '% %';

-- 6. название треков, которые содержат слово "мой"/"my".
SELECT name FROM track
WHERE name LIKE '%my%' OR name ILIKE '%мой%';
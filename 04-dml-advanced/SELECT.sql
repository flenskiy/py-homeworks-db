-- 1. количество исполнителей в каждом жанре;
SELECT name, COUNT(artist_id) FROM genre g
JOIN artist_genre ag ON g.genre_id = ag.genre_id
GROUP BY g.name;

-- 2. количество треков, вошедших в альбомы 2019-2020 годов;
SELECT COUNT(*) FROM track t
JOIN track_collection tc ON t.track_id = tc.track_id
JOIN collection c ON tc.collection_id = c.collection_id
WHERE c.year >= 2019 AND c.year <= 2020;

-- 3. средняя продолжительность треков по каждому альбому;
SELECT fk_album_id, AVG(duration) FROM track t
JOIN album a ON t.fk_album_id = a.album_id
GROUP BY fk_album_id
ORDER BY AVG(duration) DESC;

-- 4. все исполнители, которые не выпустили альбомы в 2020 году;
SELECT DISTINCT ar.name FROM artist ar
JOIN album_artist aa ON ar.artist_id = aa.artist_id
JOIN album al ON aa.album_id = al.album_id
WHERE NOT al.year = 2020
ORDER BY ar.name;

-- 5.названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
SELECT c.name FROM collection c
JOIN track_collection tc ON c.collection_id = tc.collection_id
JOIN track t ON tc.track_id = t.track_id
JOIN album al ON t.fk_album_id = al.album_id
JOIN album_artist aa ON al.album_id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.artist_id
WHERE ar.name LIKE 'artist2'
GROUP BY c.name;

-- 6.название альбомов, в которых присутствуют исполнители более 1 жанра;
SELECT al.name FROM album al
JOIN album_artist aa ON al.album_id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.artist_id
JOIN artist_genre ag ON ar.artist_id = ag.artist_id
JOIN genre g ON ag.genre_id = g.genre_id
GROUP BY al.name
HAVING COUNT(g.name) > 1;

-- 7.наименование треков, которые не входят в сборники;
SELECT t.name FROM track t
LEFT JOIN track_collection tc ON t.track_id = tc.track_id
WHERE tc.collection_id IS NULL;

-- 8. исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
SELECT ar.name FROM artist ar
JOIN album_artist aa ON ar.artist_id = aa.artist_id
JOIN album al ON aa.album_id = al.album_id
JOIN track t ON al.album_id = t.fk_album_id
WHERE t.duration = (SELECT MIN(duration) FROM track);

-- 9. название альбомов, содержащих наименьшее количество треков
SELECT DISTINCT al.name FROM album al
LEFT JOIN track t ON t.fk_album_id = al.album_id
WHERE t.fk_album_id IN (
	SELECT fk_album_id FROM track
	GROUP BY fk_album_id
	HAVING COUNT(track_id) = (
		SELECT COUNT(track_id) FROM track
		GROUP BY fk_album_id
		ORDER BY COUNT
		LIMIT 1
	)
);
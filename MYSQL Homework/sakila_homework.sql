USE sakila;

#1a
SELECT first_name, last_name 
FROM actor;

#1b
SELECT CONCAT(first_name, " ", last_name, " ") AS `Actor Name`
FROM actor;

#2a
SELECT actor_id, first_name, last_name
FROM actor 
WHERE first_name LIKE 'Joe%';

#2b
SELECT first_name, last_name 
FROM actor
WHERE last_name LIKE '%GEN%';

#2c
SELECT first_name, last_name 
FROM actor
WHERE last_name LIKE '%LI%'
ORDER BY last_name ASC, first_name ASC;

#2d
SELECT country_id, country 
FROM country
WHERE country IN ('Afghanistan', 'Bangladesh', 'China');

#3a
ALTER TABLE actor
ADD COLUMN middle_name VARCHAR(45) AFTER first_name;

#3b
ALTER TABLE actor
MODIFY COLUMN middle_name BLOB;

#3c
ALTER TABLE actor
DROP COLUMN middle_name;

#4a
SELECT last_name, COUNT(last_name) AS `last_name_count`
FROM actor
GROUP BY last_name;

#4b
SELECT last_name, COUNT(last_name) AS `last_name_count`
FROM actor
GROUP BY last_name
HAVING COUNT(last_name) >= 2;

#4c
UPDATE actor
SET first_name = 'HARPO' 
WHERE actor_id = 172;

#4d
UPDATE actor
SET first_name = 'GROUCHO' 
WHERE actor_id = 172;

#5a
SHOW CREATE TABLE address;

#6a
SELECT first_name, last_name, address
FROM staff AS s
LEFT JOIN address AS a ON s.address_id = a.address_id;

#6b
SELECT s.staff_id, s.first_name, s.last_name, SUM(p.amount) AS total_sold
FROM staff AS s
JOIN payment AS p ON s.staff_id = p.staff_id
AND p.payment_date BETWEEN '2005-08-01 00:00:00' AND '2005-08-31 11:59:59'
GROUP BY s.staff_id;

#6c
SELECT f.title, COUNT(a.actor_id) AS total_actors
FROM film AS f
INNER JOIN film_actor AS a ON f.film_id = a.film_id
GROUP BY f.film_id;

#6d
SELECT f.title, COUNT(i.inventory_id) AS total_copies
FROM film AS f
JOIN inventory AS i ON f.film_id = i.film_id
AND title = "Hunchback Impossible"
GROUP BY f.film_id;

#6e
SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount) AS total_paid
FROM customer AS c
JOIN payment AS p ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY last_name ASC;

#7a
SELECT title
FROM film
WHERE language_id IN
(
  SELECT language_id
  FROM language l
  WHERE language_id =1
  AND title LIKE 'K%' OR title LIKE 'Q%'
);

#7b
SELECT first_name, last_name
FROM actor
WHERE actor_id IN
(
  SELECT actor_id
  FROM film_actor
  WHERE film_id IN
  (
    SELECT film_id
    FROM film 
    WHERE title IN ('Alone Trip')
  )
);

#7c
SELECT cu.first_name, cu.last_name, cu.email, a.district, co.country
FROM customer AS cu
JOIN address AS a ON cu.address_id = a.address_id
JOIN city AS c ON a.city_id = c.city_id
JOIN country AS co ON c.country_id = co.country_id
HAVING co.country = 'Canada';

#7d 
SELECT f.title, c.name AS 'genre'
FROM film AS f
JOIN  film_category AS fc ON f.film_id = fc.film_id
JOIN  category AS c ON fc.category_id = c.category_id
HAVING c.name = 'Family';

#7e
SELECT f.title, COUNT(r.rental_id) AS 'total rented'
FROM film AS f
JOIN inventory AS i ON f.film_id = i.film_id
JOIN rental AS r ON i.inventory_id = r.inventory_id
JOIN payment AS p ON r.rental_id = p.rental_id
GROUP BY f.film_id
ORDER BY COUNT(r.rental_id) DESC;

#7f
SELECT s.store_id, a.address, a.district, SUM(p.amount) AS 'total sold'
FROM address AS a
JOIN store AS s ON a.address_id = s.address_id
JOIN staff AS st ON s.store_id = st.store_id
JOIN payment AS p ON st.staff_id = p.staff_id
GROUP BY s.store_id;

#7g
SELECT  s.store_id, c.city, co.country
FROM store AS s
JOIN address AS a ON  a.address_id = s.address_id
JOIN city AS c ON a.city_id = c.city_id
JOIN country AS co ON c.country_id = co.country_id;

#7h
SELECT c.name AS 'Genre', SUM(p.amount) AS 'Gross Revenue'
FROM category AS c
JOIN film_category AS fc ON c.category_id = fc.category_id
JOIN inventory AS i ON fc.film_id = i.film_id
JOIN rental AS r ON i.inventory_id = r.inventory_id
JOIN payment AS p ON r.rental_id = p.rental_id
GROUP BY c.name
ORDER BY SUM(p.amount) DESC LIMIT 5;

#8a
CREATE VIEW top_five_genres AS
SELECT c.name AS 'Genre', SUM(p.amount) AS 'Gross Revenue'
FROM category AS c
JOIN film_category AS fc ON c.category_id = fc.category_id
JOIN inventory AS i ON fc.film_id = i.film_id
JOIN rental AS r ON i.inventory_id = r.inventory_id
JOIN payment AS p ON r.rental_id = p.rental_id
GROUP BY c.name
ORDER BY SUM(p.amount) DESC LIMIT 5;

#8b
SELECT * 
FROM top_five_genres;

#8c
DROP VIEW top_five_genres;



-- SELECT * FROM film;
-- SELECT district,phone,postal_code FROM address;
-- SELECT address || ' ' || district || ' ' || postal_code AS full_address FROM address;
-- SELECT * FROM customer WHERE first_name LIKE 'J%';
-- SELECT * FROM payment WHERE amount BETWEEN 3 AND 5;
-- SELECT * FROM payment WHERE payment_date BETWEEN '2007-02-15' and '2007-02-20';
-- SELECT title FROM film WHERE film_id IN (SELECT film_id FROM inventory);
-- SELECT * FROM payment WHERE amount BETWEEN 4 AND 6 ORDER BY payment_date DESC;
-- SELECT * FROM customer ORDER BY last_name DESC LIMIT 5;
-- SELECT * FROM customer ORDER BY last_name ASC LIMIT 5 OFFSET 10;

-- INSERT INTO 
-- 	customer(store_id,first_name,last_name, email, address_id) 
-- 	VALUES
-- 		(1,'John','Smith','js@yahoo.com',2),
-- 		(31,'Johny','Smith','jys@yahoo.com',6),
-- 		(11,'Johne','Smith','jes@yahoo.com',13),
-- 		(5,'Jhohn','Smith','jhs@yahoo.com',3),
-- 		(99,'Johnnie','Smith','jnies@yahoo.com',51)
-- 	RETURNING *;

-- UPDATE customer
-- 	SET first_name = 'ZZZZZZ', last_name = 'QQQQQ'
-- 	WHERE customer_id = 2 RETURNING *;


-- SELECT * FROM customer ORDER BY customer_id DESC;
-- DELETE FROM customer WHERE customer_id = 605;
-- SELECT * FROM customer ORDER BY customer_id DESC;

DELETE FROM customer WHERE customer_id = 
	(SELECT customer_id FROM customer ORDER BY customer_id DESC LIMIT 1);

BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS engines (engine text PRIMARY KEY, power integer, type integer);
CREATE TABLE IF NOT EXISTS hulls (hull text PRIMARY KEY, armor integer, type integer, capacity integer);
CREATE TABLE IF NOT EXISTS ships (ship text PRIMARY KEY, weapon text, hull text, engine text);
CREATE TABLE IF NOT EXISTS weapons
(weapon text PRIMARY KEY, "reload speed" integer, "rotational speed" integer, diameter integer, "power volley" integer, count integer);
COMMIT;

-- a bunch of random queries for testing

use ufo_sightings;

-- what are the movies releast closest to the date with most ufo sightings
drop temporary table sightings_counted_by_country_date;
create temporary table sightings_counted_by_country_date as
select event_dates.date_full, country_id, row_number() over(partition by event_dates.date, country_id) as sightings_by_date_by_country from ufo_sightings
LEFT JOIN event_dates
USING (date_id)
WHERE year(date_full) > 2017
ORDER BY sightings_by_date_by_country DESC;

-- most sightings in a country on a certain MMYYYY
WITH date_most_sightings AS (
    SELECT date_full
    FROM sightings_counted_by_country_date
    GROUP BY date_full, country_id
    LIMIT 1
)
SELECT title, date
FROM movies m
JOIN event_dates ed USING (date_id)
CROSS JOIN date_most_sightings
WHERE YEAR(ed.date_full) = YEAR(date_most_sightings.date_full)
  AND m.ufo_theme = 1
  AND MONTH(ed.date_full) = MONTH(date_most_sightings.date_full);
  
  
-- month with highest amount of ufo sightings
with total_sightings as (
select count(*) as total from ufo_sightings)

select count(id) as sightings, month(date_full) as month, count(id) / (select total from total_sightings) as sightings_share
from ufo_sightings
JOIN event_dates using(date_id)
group by month(date_full)
ORDER BY sightings DESC;



-- only include years which have more than the average amount of ufo sightings per year
with sightings_per_year as (
select year(date_full) as year, count(id) as sightings from ufo_sightings
JOIN event_dates using (date_id)
GROUP BY year(date_full)),
average_sightings_per_year as (select avg(sightings) as avg_sightings from sightings_per_year)
select * from ufo_sightings 
JOIN event_dates using (date_id)
WHERE year(date_full) IN (SELECT year from sightings_per_year where sightings > (SELECT avg_sightings FROM average_sightings_per_year));

-- countries with ufo in name
create view countries_with_ufo_in_name as (
select * from countries
WHERE country LIKE "%U%" AND country LIKE "%F%" AND country LIKE "%O%");
select * from countries_with_ufo_in_name;

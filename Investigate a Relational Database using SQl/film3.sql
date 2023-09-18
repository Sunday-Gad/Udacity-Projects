with t1 as (select f.title, c."name", f.rental_duration
from film f 
join film_category fc 
on f.film_id = fc.film_id 
join category c 
on c.category_id = fc.category_id
), 
	t2 as (select f.title, avg(rental_duration) ave
		from film f 
		join film_category fc 
		on f.film_id = fc.film_id 
		join category c 
		on c.category_id = fc.category_id
		group by 1
		) 
		
select t4.name, t4.standard_quartile, count(standard_quartile) 
from 		
(select t1.title, t1.name, t1.rental_duration, ntile(4) over (order by t2.ave) standard_quartile
from t1
join t2
on t1.title = t2.title
where t1."name" in ('Children', 'Music', 'Family', 'Animation', 'Classics', 'Comedy')
order by 2,3) t4
group by 1, 2
order by 1, 2

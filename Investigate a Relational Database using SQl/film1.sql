select f.title, c."name", count(f.title) 
from category c 
join film_category fc 
on fc.category_id = c.category_id 
join film f 
on f.film_id = fc.film_id 
join inventory i 
on i.film_id = f.film_id 
join rental r 
on r.inventory_id = i.inventory_id
where c."name"  in ('Children', 'Music', 'Family', 'Animation', 'Classics', 'Comedy')
group by 1, 2
order by 2, 1
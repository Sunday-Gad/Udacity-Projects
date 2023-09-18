select date_part('month', r.rental_date) Rental_month, date_part('year', r.rental_date) Rental_year, i.store_id Store_ID, count(*) Count_rental
from rental r 
join inventory i 
on i.inventory_id = r.inventory_id 
group by 1, 2, 3
order  by 4 desc
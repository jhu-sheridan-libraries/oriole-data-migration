SELECT subcat_2_db.database_id as database_id
, cat.name AS catname
, subcat.name AS subname
FROM xerxes_user_categories cat
INNER JOIN xerxes_user_subcategories subcat 
    ON cat.id = subcat.category_id
INNER JOIN xerxes_user_subcategory_databases subcat_2_db
    ON subcat.id = subcat_2_db.subcategory_id
WHERE cat.username = 'global_user'
ORDER BY 2, 3, 1

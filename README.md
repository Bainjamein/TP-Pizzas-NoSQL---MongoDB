# TP Pizza - NoSQL : MongoDB
## MAALSI23
### Benjamin Perchepied - Quentin Savéan

Commande pour run : __docker-compose up --build__

**Etape 3 :**

a. Quel est le montant total des commandes de pizzas (tous formats confondus) ?

> 2540 €

b. Combien de pizzas ont été commandées (toutes recettes et format confondus) ?

> 155 pizzas

c. Combien de pizzas "Vegan" ont été commandées ?

> 20 pizzas

d. Combien de pizzas ont été commandées en format "large" ?

> 40 pizzas

e. Quelle recette de pizza a été la plus vendue ?

> Cheese

f. Quel format de pizza a été le plus vendu ?

> Small

g. Quelle recette de pizza a rapporté le plus de revenus ?

> Pepperoni

**Etape 4 :**

a. Calcul de la quantité de pizzas commandées par format "medium" pour chaque recette de pizza : 

> db.orders.aggregate([{ $group: { _id:{name:"$name", size:"medium" }, total_quantity: { $sum:"$quantity"}}}])

> Pepperoni : 20
> Cheese : 50
> Vegan : 10

b. Calcul du nombre moyen de pizzas commandées :

> db.orders.aggregate([{$group: {_id: null,average_quantity: { $avg: "$quantity" }}}])

> 19.375

**Etape 5 :**

a. Liste du menu des pizzas :

> [{'name': 'Pepperoni', 'size': 'small', 'price': 19}, {'name': 'Pepperoni', 'size': 'medium', 'price': 20}, {'name': 'Pepperoni', 'size': 'large', 'price': 21}, {'name': 'Cheese', 'size': 'small', 'price': 12}, {'name': 'Cheese', 'size': 'medium', 'price': 13}, {'name': 'Cheese', 'size': 'large', 'price': 14}, {'name': 'Vegan', 'size': 'small', 'price': 17}, {'name': 'Vegan', 'size': 'medium', 'price': 18}]
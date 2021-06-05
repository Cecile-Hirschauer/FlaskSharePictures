# Projet réalisé du 22/02/2021 au 05/03/2021

## Projet en équipe: 4 personnes - Méthodologie: SCRUM


###### Création back-end et front-end d'un site de partage d'image avec Python/Flask

Fonctionnalités de base:

* Une page d'accueil, où toutes les images sont affichées. Les images seront classées par date de création par ordre décroissant (l'image la plus récente est affichée en premier). La page d'accueil peut être filtrée par catégorie, via des paramètres de requête.

* Une page pour afficher une image donnée et son titre/description (quand on clique sur une image de la page d'accueil)

* Une page pour télécharger une nouvelle image, avec un titre, une catégorie (à choisir parmi une liste de catégories disponibles) et une description. Les images téléchargées doivent ensuite être enregistrées dans votre système de fichiers. Cela signifie que vous devrez gérer certains cas particuliers. (Que se passe-t-il lorsque deux images ont le même nom… ?)

* Validations correctes. Assurez-vous que le fichier téléchargé est une image (jpeg, png, gif...) avant de l'ajouter à votre base de données !

* Un système de commentaires. Il doit être possible de visualiser/ajouter des commentaires sur la page qui montre une image donnée


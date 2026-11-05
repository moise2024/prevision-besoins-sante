# Prévision exploratoire des besoins en santé

Prototype académique : prévision mensuelle de fréquentation, comparaison de modèles de régression, visualisation territoriale et documentation des limites.

## Avertissement sur les données

Les données incluses sont entièrement **simulées**. Les établissements, leurs coordonnées et leurs volumes ne décrivent aucun centre réel ni aucun besoin sanitaire réel. Elles permettent de reproduire le pipeline et de vérifier le fonctionnement des livrables, mais ne permettent aucune conclusion sur la Côte d'Ivoire. Aucun dossier patient ni donnée personnelle n'est utilisé.

La recherche a identifié le portail national BDMS comme dispositif de mutualisation sécurisée des données sanitaires, ainsi que des jeux géographiques ouverts d'établissements (Healthsites/HDX). Ces sources ne fournissent pas, dans ce projet, un historique mensuel public de fréquentation apparié aux établissements. Pour un usage réel, il faut obtenir une extraction autorisée et documentée du système d'information sanitaire, puis vérifier les droits, la qualité et la couverture avant modélisation.

## Reproduire

Python 3.10+ :

```bash
pip install -r requirements.txt
python src/run_analysis.py
```

Le script produit les métriques dans `outputs/model_comparison.csv`, une prévision de démonstration par centre dans `outputs/forecasts.csv`, une carte HTML consultable dans un navigateur (`outputs/carte_besoins.html`) et un GeoJSON (`outputs/centres_previsions.geojson`) ouvrable dans QGIS. Les données simulées reproductibles sont dans `data/`.

## Méthode

Un modèle naïf saisonnier (valeur du même mois l'année précédente) est comparé à deux régressions : régression linéaire avec tendance et termes sinusoïdaux annuels, et Ridge avec les mêmes variables. Les 12 derniers mois sont réservés au test chronologique. Les scores sont MAE, RMSE et MAPE; MAPE est omis lorsque les valeurs observées sont nulles. Le modèle ayant le plus faible MAE est réentraîné sur l'historique complet pour produire les 12 mois suivants. Cette règle choisit un modèle pour le prototype uniquement : une validation roulante et un choix distinct par centre seraient préférables avant déploiement.

Le nombre de visites simulées est un indicateur de charge de service, pas une mesure directe de besoins non satisfaits, de prévalence ou de qualité des soins. Les visites peuvent évoluer avec l'offre, l'accessibilité, les pratiques d'enregistrement et les ruptures de stock.

## Sources consultées

- [Portail de la Base de données mutualisée de la santé (BDMS), Côte d'Ivoire](https://portail.bdm-sante.ci/) — description de la plateforme nationale de mutualisation sécurisée.
- [Healthsites.io](https://maps.healthsites.io/map) — référentiel cartographique ouvert d'établissements de santé, alimenté notamment par OpenStreetMap.
- [Plan national de développement sanitaire 2021–2025, OMS](https://extranet.who.int/cpcd/sites/default/files/public_file_repository/CIV_Cote-dIvoire_Plan-National-de-Developpement-Sanitaire_2021-2025.pdf) — contexte de planification sanitaire et indicateurs d'utilisation.

Les coordonnées de ce prototype restent fictives malgré ces références et ne sont pas extraites de ces sources.

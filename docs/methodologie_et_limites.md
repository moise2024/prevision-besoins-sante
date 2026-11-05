# Note méthodologique et limites

## Question et unité d'analyse

Le prototype estime le volume mensuel de visites pour chacun de six centres **fictifs**, à partir de 48 mois simulés (janvier 2022–décembre 2025). La sortie est une prévision de charge de fréquentation. Elle ne mesure pas la demande latente, les besoins non couverts, la morbidité ni les ressources requises.

## Données et préparation

Les séries sont générées avec une graine fixe, un niveau propre à chaque centre, une faible tendance, une saisonnalité annuelle et du bruit aléatoire. Le fichier des coordonnées place des points de démonstration autour d'Abidjan; ces points ne sont pas des établissements existants. Les données réelles devraient inclure un dictionnaire d'indicateurs, la définition de visite, le calendrier, les corrections et agrégations, les valeurs manquantes, les changements de périmètre et la provenance.

## Modèles et évaluation

La séparation chronologique conserve les 12 derniers mois pour le test. Les candidats sont : (1) naïf saisonnier, (2) régression linéaire avec tendance et sinus/cosinus annuels, (3) Ridge avec ces variables. Les métriques sont MAE et RMSE en visites, ainsi que MAPE en pourcentage si aucune observation test n'est nulle. La sélection par MAE sert uniquement à produire l'exemple de prévision; les métriques sont rapportées centre par centre.

Une évaluation opérationnelle devrait utiliser une validation à origine glissante, des intervalles d'incertitude, des comparaisons à des références pertinentes, et analyser la performance selon centre, milieu, saison et qualité de rapportage. Les séries de fréquentation sont des comptes; des modèles de Poisson/nég binomiale ou des approches adaptées aux zéros peuvent être évalués si les propriétés des données le justifient.

## Hypothèses et biais potentiels

- La définition et le processus d'enregistrement des visites restent constants.
- L'historique est représentatif du futur; les ruptures, épidémies, campagnes, grèves, changements d'offre ou événements climatiques ne sont pas modélisés.
- Une faible fréquentation peut signifier accès difficile ou sous-déclaration, plutôt qu'un faible besoin.
- Les différences de population, d'accessibilité, d'offre, de qualité et de couverture des rapports peuvent rendre les comparaisons territoriales trompeuses.
- La saisonnalité simulée est artificielle et ne doit pas être interprétée comme une saisonnalité sanitaire ivoirienne.
- Les coordonnées sont fictives; la carte n'est pas une carte de couverture ou d'accès aux soins.

## Précautions avant toute utilisation

Ne pas allouer des médicaments, du personnel ou des budgets sur la base de cette démonstration. Toute utilisation réelle exige l'autorisation du détenteur des données, une revue de confidentialité et de gouvernance, des contrôles de qualité, une validation avec les équipes sanitaires, des analyses d'équité et une surveillance des erreurs. Les sorties doivent éclairer une discussion humaine et ne pas remplacer le jugement clinique ou la planification publique.

## Sources contextuelles

- La [BDMS de Côte d'Ivoire](https://portail.bdm-sante.ci/) est présentée comme une plateforme nationale de mutualisation sécurisée des données sanitaires.
- [Healthsites.io](https://maps.healthsites.io/map) propose des données cartographiques d'établissements de santé ouvertes, notamment issues d'OpenStreetMap; complétude et actualité doivent être vérifiées localement.
- Le [PNDS 2021–2025](https://extranet.who.int/cpcd/sites/default/files/public_file_repository/CIV_Cote-dIvoire_Plan-National-de-Developpement-Sanitaire_2021-2025.pdf) fournit du contexte de planification et d'utilisation des services, mais ne constitue pas l'historique mensuel désagrégé employé ici.

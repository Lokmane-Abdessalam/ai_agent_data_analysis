# Cahier de Test Concret - Executive AI Agent

Ce fichier contient les questions exactes à copier-coller dans l'interface, ainsi que les réponses factuelles que l'agent DOIT retourner d'après les bases de données et documents fournis.

## Test 1 : Base de Données Ventes (Quantitatif Pur)
* **Question à poser :** 
  > "Quel est le montant total des ventes générées par les clients situés en France ?"
* **Outils déclenchés :** `outil_chiffres_ventes`
* **Réponse concrète attendue :** 
  L'agent doit répondre exactement **195.5** (Alice a fait une commande de 150.5 et une de 45.0, Charlie n'a pas de commande).

## Test 2 : RAG Stratégie (Qualitatif Pur)
* **Question à poser :** 
  > "Quelle a été la décision de la direction face à la baisse de prix agressive de TechDiscount ce trimestre ?"
* **Outils déclenchés :** `recherche_documentaire`
* **Réponse concrète attendue :** 
  L'agent doit expliquer que la direction a refusé de s'aligner sur cette baisse de 15% afin de **préserver l'image de marque "Premium"** et les marges de l'entreprise.

## Test 3 : Analyse Croisée Ventes + RAG (Le test principal)
* **Question à poser :** 
  > "Donne-moi le montant exact des ventes réalisées en Belgique, et explique-moi pourquoi nous avons ces résultats sur ce marché."
* **Outils déclenchés :** `outil_chiffres_ventes` PUIS `recherche_documentaire`
* **Réponse concrète attendue :** 
  - **Chiffres :** L'agent doit indiquer un total de **300.0** (la commande de Bob).
  - **Analyse :** L'agent doit expliquer que cette performance est due à la signature d'un partenariat exclusif de distribution avec le réseau **"Bruxelles Retail"**.

## Test 4 : Base de Données RH (Quantitatif Pur)
* **Question à poser :** 
  > "Combien avons-nous d'employés dans le département IT et quel est leur salaire moyen ?"
* **Outils déclenchés :** `outil_ressources_humaines`
* **Réponse concrète attendue :** 
  L'agent doit répondre qu'il y a **2 employés** (Alice et Charlie) et que leur salaire moyen est de **48 500** (la moyenne entre 45000 et 52000).

## Test 5 : Analyse Croisée RH + RAG
* **Question à poser :** 
  > "Je dois budgéter la masse salariale totale de l'entreprise. Donne-moi la somme exacte de tous les salaires actuels. Ensuite, rappelle-moi quel budget exceptionnel a été débloqué pour la formation."
* **Outils déclenchés :** `outil_ressources_humaines` PUIS `recherche_documentaire`
* **Réponse concrète attendue :** 
  - **Chiffres :** La masse salariale totale est de **135 000** (45000 + 38000 + 52000).
  - **Analyse :** Le budget exceptionnel débloqué pour la formation ("Upskilling") est de **500 000 €**, mis en place pour pallier le gel des embauches externes.

## Test 6 : Synthèse Multi-Départements (Limites et Règles strictes)
* **Question à poser :** 
  > "Combien d'employés avons-nous dans le département Ventes, et quelles sont leurs nouvelles règles de télétravail ?"
* **Outils déclenchés :** `outil_ressources_humaines` PUIS `recherche_documentaire`
* **Réponse concrète attendue :** 
  - **Chiffres :** L'agent doit identifier **1 seul employé** (Bob) dans le département Ventes.
  - **Analyse :** L'agent doit préciser que les employés des ventes ont droit à **2 jours de télétravail** par semaine (contrairement à l'IT/Support qui en ont 3).
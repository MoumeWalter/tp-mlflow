# Réponses théoriques

## Fonctionnalités principales de MLflow
- **Tracking** : enregistre paramètres, métriques, tags et artefacts de chaque run.
- **Projects** : package le code pour des exécutions reproductibles.
- **Models** : format standard (flavors, signature) pour charger un modèle quel que soit le framework.
- **Model Registry** : versionne les modèles, gère des alias (staging, production) et l'historique.
- **Serving** : sert un modèle via une API HTTP (`mlflow models serve`).
- Interface web pour parcourir et comparer les runs, SDK Python et API REST.

## Ce que permet le tracking d'expériences
- Logger les hyperparamètres (`log_params`) et les métriques (`log_metric`, avec historique par étape).
- Logger des tags, des fichiers et graphiques (artefacts) et le modèle lui-même (avec signature).
- Regrouper les runs par expérience, les rechercher, les filtrer, les trier et les comparer dans l'UI.
- Retrouver le code et l'environnement d'un run pour le reproduire.
- Recharger un modèle depuis un run ou le registry.

## Canary deployment
On déploie la nouvelle version à côté de l'ancienne et on lui envoie un petit pourcentage du trafic. On surveille erreurs et métriques, on augmente progressivement, puis on généralise ou on revient en arrière.
Dans ce TP : `current` reçoit le trafic avec la probabilité p, `next` avec 1 - p. `/accept-next-model` généralise la nouvelle version.

## Blue/green deployment
Deux environnements identiques : un seul (« blue ») sert la production. On déploie et teste la nouvelle version sur l'autre (« green »), puis on bascule tout le trafic d'un coup. Le rollback consiste à rebasculer sur l'ancien.

## Similarités et différences
- Points communs : deux versions coexistent, le trafic est routé entre elles, le rollback est rapide, le risque est réduit.
- Canary : montée progressive, test sur du vrai trafic, pas besoin de dupliquer toute l'infrastructure.
- Blue/green : bascule totale et instantanée, test complet avant la bascule, coût de deux environnements complets.

## Sécuriser un MLflow public
MLflow propose :
- une authentification basic auth (`mlflow server --app-name basic-auth`) avec des permissions par expérience et par modèle ;
- des identifiants côté client (`MLFLOW_TRACKING_USERNAME`, `MLFLOW_TRACKING_PASSWORD`) ou un jeton ;
- du SSO via plugin ou reverse proxy ;
- des protections de hôtes autorisés et CORS dans les versions récentes.

Cela ne suffit pas : les identifiants circulent à chaque requête, et la couverture des permissions n'est pas totale.
Mesures complémentaires :
- reverse proxy (nginx, Caddy) avec HTTPS et authentification ;
- accès restreint par pare-feu, VPN ou tunnel SSH ;
- ne jamais exposer le port 5000 en clair sur Internet.

# Serverles simple blog

Ce blog en serverless utilise les technologies suivantes:
- AWS Lambda
- DynamoDB
- S3
- CloudFront
- API Gateway
- Python
- Nuxt.js

Le site est disponible à l'adresse suivante: [serverless-blog.tgarcin.fr](https://serverless-blog.tgarcin.fr)

## Instuctions de déploiement

### Back-end

Requis :
- Serverless framework
- Compte AWS

Dans un terminal

```bash
npm install
export DEPLOYMENT_BUCKET={votre nom de bucket S3}
export DYNAMO_TABLE={Le nom de la table dynamodb}
serverless deploy
```

Récupérer dans le résultat de la commande l'URL de base de l'API et remplacer la variable `env.apiUrl` dans le fichier `front/nuxt.config.js`

### Front-end

Dans un terminal
```bash
cd front
npm install
npm run dev # pour lancer la version de dev avec hotreaload
npx nuxt build --spa # pour build une version Single Page Application
```

## Format des données en base

Un post est représenté dans la table par un document.

Il est identifié de manière unique par son champ `post_id`.

Ci dessous un exemple de post tel qu'il est stocké en base :

```json5
{
  "author": "aerazer", // string
  "comments": [ // liste de commentaires
    {
      "content": "😎😎😎😎😎😎😎", // string
      "create_date": "2019-06-09T16:46:34.847174" // date au format iso
    }
  ],
  "content": "pojra$eorâêr", // string
  "create_date": "2019-06-09T16:46:18.926188", // date au format iso
  "post_id": "60bef326-9692-4db9-939f-6cb5cc2c7c0b", // uuid4
  "title": "arezrae", // string
  "type": "post" // string (constante requise pour l'index secondaire)
}
```

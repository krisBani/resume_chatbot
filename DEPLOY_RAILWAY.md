# 🚀 Guide de Déploiement sur Railway

Ce guide vous accompagne pas à pas pour déployer votre chatbot de CV sur Railway.

---

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :

- ✅ Un compte GitHub (gratuit)
- ✅ Git installé sur votre machine
- ✅ Votre chatbot testé localement (✅ Vous l'avez fait !)
- ✅ Vos 3 clés API (Groq, Cohere, Pinecone) (✅ Vous les avez !)

---

## 🎯 Étapes du déploiement

### ÉTAPE 1 : Préparer le dépôt GitHub (5 min)

#### 1.1 Vérifier le .gitignore

Assurez-vous que votre fichier `.gitignore` contient :

```
.env
__pycache__/
*.pyc
.venv/
venv/
data/*.pdf
data/*.docx
```

Ceci empêche de pousser vos clés API et CV sur GitHub (sécurité).

#### 1.2 Pousser votre code sur GitHub

Si ce n'est pas déjà fait :

```bash
# Vérifier l'état du dépôt
git status

# Ajouter tous les fichiers modifiés
git add .

# Créer un commit
git commit -m "Prepare for Railway deployment"

# Pousser sur GitHub
git push origin main
```

Si vous n'avez pas encore de dépôt GitHub :

```bash
# Aller sur github.com et créer un nouveau dépôt nommé "resume_chatbot"
# Puis :
git remote add origin https://github.com/VOTRE-USERNAME/resume_chatbot.git
git branch -M main
git push -u origin main
```

---

### ÉTAPE 2 : Créer un compte Railway (2 min)

1. **Allez sur** : https://railway.app
2. **Cliquez** sur "Start a New Project" ou "Login"
3. **Connectez-vous** avec votre compte GitHub
4. **Autorisez** Railway à accéder à vos dépôts

Railway vous donne **$5 de crédit gratuit par mois** 🎁

---

### ÉTAPE 3 : Déployer le projet (5 min)

#### 3.1 Créer un nouveau projet

1. Sur le dashboard Railway, cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Choisissez votre dépôt **`resume_chatbot`**
4. Railway va automatiquement détecter que c'est une app Python

#### 3.2 Attendre le build initial

Railway va :

- ✅ Installer Python
- ✅ Installer les dépendances (`requirements.txt`)
- ✅ Construire l'application

**Durée** : 2-3 minutes

⚠️ **Le premier déploiement va échouer** - c'est normal ! Il manque les variables d'environnement.

---

### ÉTAPE 4 : Configurer les variables d'environnement (3 min)

#### 4.1 Accéder aux variables

1. Dans votre projet Railway, cliquez sur l'onglet **"Variables"**
2. Cliquez sur **"+ New Variable"**

#### 4.2 Ajouter TOUTES les variables

Ajoutez une par une (copiez depuis votre `.env` local) :

```env
LLM_PROVIDER=groq
LLM_API_KEY=votre_cle_groq_ici
EMBEDDING_PROVIDER=cohere
EMBEDDING_API_KEY=votre_cle_cohere_ici
PINECONE_API_KEY=votre_cle_pinecone_ici
PINECONE_INDEX_NAME=resumechatbot
RESUME_OWNER_NAME=Kris Bani Nguinano
CANDIDATE_GENDER=male
PORT=8000
```

**🔒 Important** :

- Remplacez les valeurs par vos vraies clés API
- Ces variables sont privées et sécurisées sur Railway
- Ne partagez jamais vos clés API publiquement

#### 4.3 Sauvegarder

Une fois toutes les variables ajoutées, Railway va **automatiquement redéployer** votre application.

---

### ÉTAPE 5 : Obtenir votre URL publique (1 min)

#### 5.1 Générer un domaine

1. Dans votre projet Railway, cliquez sur **"Settings"**
2. Scrollez jusqu'à **"Domains"**
3. Cliquez sur **"Generate Domain"**

Railway va créer une URL comme :

```
https://resume-chatbot-production-xxxx.up.railway.app
```

#### 5.2 Tester l'API

Ouvrez votre navigateur et allez sur :

```
https://votre-app.up.railway.app/
```

Vous devriez voir :

```json
{
  "status": "ok",
  "message": "Resume Chatbot API for Kris Bani Nguinano",
  "version": "2.0-simplified"
}
```

🎉 **Félicitations ! Votre API est en ligne !**

---

### ÉTAPE 6 : Tester avec Postman (2 min)

Testez le endpoint `/ask` avec votre nouvelle URL :

```
POST https://votre-app.up.railway.app/ask
Content-Type: application/json

{
  "question": "What is your experience?"
}
```

Si vous obtenez une réponse, **c'est bon !** 🎉

---

## 🔧 Dépannage

### Problème 1 : "Application Error"

**Cause** : Variables d'environnement manquantes ou incorrectes

**Solution** :

1. Vérifiez que TOUTES les variables sont ajoutées
2. Vérifiez qu'il n'y a pas de fautes de frappe dans les noms
3. Vérifiez que les clés API sont valides

### Problème 2 : "Build Failed"

**Cause** : Problème avec `requirements.txt` ou Python

**Solution** :

1. Vérifiez que `requirements.txt` est à jour
2. Dans Railway Settings, vérifiez la version de Python
3. Consultez les logs de build pour voir l'erreur exacte

### Problème 3 : "Timeout" ou lenteur

**Cause** : Première requête après un moment d'inactivité

**Solution** : C'est normal, attendez quelques secondes. Railway "réveille" l'app.

### Problème 4 : Dépassement du crédit gratuit

**Symptôme** : Railway arrête votre app après quelques jours

**Solution** :

1. Vérifiez votre usage dans le dashboard Railway
2. Si nécessaire, optimisez ou passez à Render (gratuit à vie)
3. Ou ajoutez une carte bancaire pour continuer ($5/mois)

---

## 📊 Surveillance de l'usage

### Vérifier votre consommation

1. Dans Railway, allez dans **"Usage"**
2. Vous verrez :
   - Crédits utilisés ce mois
   - Crédits restants
   - Graphique d'utilisation

### Conseils pour économiser

- Le chatbot consomme très peu au repos
- Seules les requêtes actives consomment
- Votre usage sera probablement < $1/mois

---

## 🎯 Prochaines étapes

Une fois déployé sur Railway :

1. ✅ **Notez votre URL Railway** : `https://votre-app.up.railway.app`
2. 🔗 **Intégrez dans Next.js** : Remplacez l'URL locale par l'URL Railway
3. 📄 **Ajoutez à votre CV** : Mettez un lien vers le chatbot
4. 🚀 **Partagez** : Envoyez le lien aux recruteurs !

---

## 📝 Mise à jour du code

Pour mettre à jour votre chatbot après déploiement :

```bash
# Faites vos modifications localement
# Testez avec : python app.py

# Une fois satisfait :
git add .
git commit -m "Update feature X"
git push origin main

# Railway redéploie automatiquement ! 🎉
```

---

## 💰 Estimation des coûts

Pour un chatbot CV typique :

- **Mois 1-3** : $0 (bien sous les $5 de crédit gratuit)
- **Utilisation intensive** : $1-3/mois
- **Très haute utilisation** : Max $5/mois

**Si vous trouvez un emploi grâce à ce chatbot, $5/mois est un excellent investissement !** 💼

---

## 🆘 Besoin d'aide ?

- **Documentation Railway** : https://docs.railway.app
- **Community Railway** : https://discord.gg/railway
- **Logs Railway** : Consultez l'onglet "Deployments" → "View Logs"

---

**Prêt à déployer ?** Suivez les étapes ci-dessus ! 🚀

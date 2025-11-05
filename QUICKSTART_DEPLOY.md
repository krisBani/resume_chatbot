# 🚀 Déploiement Railway - Quick Start

Guide ultra-rapide pour déployer votre chatbot en 15 minutes.

---

## ✅ Checklist Prédéploiement

Avant de déployer, vérifiez que vous avez :

- [x] ✅ Chatbot testé localement (Postman OK)
- [x] ✅ Clés API prêtes (Groq, Cohere, Pinecone)
- [x] ✅ CV indexé dans Pinecone
- [x] ✅ Fichiers Railway créés (Procfile, runtime.txt)
- [x] ✅ .gitignore configuré

**Tout est prêt ! Vous pouvez commencer. ⬇️**

---

## 📝 Étapes Rapides

### 1️⃣ Pousser sur GitHub (2 min)

```bash
# Vérifier l'état
git status

# Ajouter tous les fichiers
git add .

# Créer un commit
git commit -m "Ready for Railway deployment"

# Pousser
git push origin main
```

---

### 2️⃣ Créer compte Railway (2 min)

1. Aller sur : **https://railway.app**
2. Cliquer **"Login with GitHub"**
3. Autoriser Railway

---

### 3️⃣ Déployer (5 min)

1. **New Project** → **Deploy from GitHub repo**
2. Sélectionner : **`resume_chatbot`**
3. Attendre le build (2-3 min)

⚠️ Le premier build va **échouer** - c'est normal !

---

### 4️⃣ Ajouter variables d'environnement (3 min)

Dans Railway, onglet **"Variables"** → **"+ New Variable"** :

```env
LLM_PROVIDER=groq
LLM_API_KEY=<votre_clé_groq>
EMBEDDING_PROVIDER=cohere
EMBEDDING_API_KEY=<votre_clé_cohere>
PINECONE_API_KEY=<votre_clé_pinecone>
PINECONE_INDEX_NAME=resumechatbot
RESUME_OWNER_NAME=Kris Bani Nguinano
CANDIDATE_GENDER=male
PORT=8000
```

💾 Sauvegarder → Railway redéploie automatiquement

---

### 5️⃣ Générer un domaine (1 min)

1. **Settings** → **Domains**
2. **Generate Domain**

Vous obtenez : `https://resume-chatbot-production-xxxx.up.railway.app`

---

### 6️⃣ Tester (2 min)

**Browser** :

```
https://votre-app.up.railway.app/
```

**Postman** :

```
POST https://votre-app.up.railway.app/ask
{
  "question": "What is your experience?"
}
```

🎉 **Si ça marche, c'est déployé !**

---

## 🔧 En cas de problème

### Build échoue ?

- Vérifiez les logs dans Railway
- Vérifiez `requirements.txt`

### Application Error ?

- **Cause #1** : Variables manquantes
  - Vérifiez que TOUTES les 9 variables sont ajoutées
- **Cause #2** : Clés API invalides
  - Testez vos clés localement d'abord

### Timeout ?

- Première requête = Normal (cold start)
- Attendez 5-10 secondes

---

## 📊 Après le déploiement

### Notez votre URL

```
https://votre-app.up.railway.app
```

### Surveillez l'usage

Railway Dashboard → **Usage**

- Vous verrez les crédits consommés
- Probablement < $1/mois pour un CV

---

## 🎯 Prochaines étapes

1. ✅ **Intégrez dans Next.js** :

   ```javascript
   const API_URL = "https://votre-app.up.railway.app";
   ```

2. 📱 **Testez sur mobile**

3. 📄 **Ajoutez à votre CV** :

   ```
   💬 Interactive Resume Chatbot: [lien]
   ```

4. 🚀 **Partagez avec les recruteurs !**

---

## 💰 Budget

**Estimation pour 3 mois** :

- Mois 1 : $0 (crédit gratuit)
- Mois 2 : $0 (très faible usage)
- Mois 3 : $0-1 (si utilisation normale)

**Total réaliste** : Gratuit pendant toute votre recherche d'emploi !

---

## 📚 Documentation complète

Pour plus de détails, consultez :

- **`DEPLOY_RAILWAY.md`** : Guide détaillé
- **`README_SIMPLIFIED.md`** : Vue d'ensemble du projet
- **`TEST_API.md`** : Tests locaux

---

**Prêt ? Commencez par l'étape 1 ! 🚀**

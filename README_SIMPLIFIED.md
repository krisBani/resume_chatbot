# Resume Chatbot - Version Simplifiée (100% Gratuite)

Ce projet est un chatbot de CV qui permet aux recruteurs d'interagir avec votre CV via une API simple. Cette version a été simplifiée et adaptée pour utiliser des services **100% gratuits**.

## 🎯 Ce qui a changé par rapport à la version originale

- ❌ **Supprimé** : Azure AI Search, Azure SQL, Streamlit, authentification
- ✅ **Ajouté** : Pinecone (gratuit), Groq/LLMs gratuits, API Flask simple
- 💰 **Coût** : 0$ (avec quotas gratuits)
- ⚡ **Complexité** : Réduite de 70%

## 🚀 Technologies utilisées

- **Backend** : Flask (Python)
- **LLM** : Groq (recommandé, gratuit) ou autres providers
- **Embeddings** : Cohere (gratuit) ou OpenAI
- **Vector Database** : Pinecone (tier gratuit)
- **Document Processing** : LangChain

## 📋 Prérequis

1. Python 3.10 ou supérieur
2. Un compte Groq (gratuit) : https://console.groq.com
3. Un compte Cohere (gratuit) : https://dashboard.cohere.com
4. Un compte Pinecone (gratuit) : https://www.pinecone.io
5. Votre CV en format PDF, DOCX ou TXT

## 🛠️ Installation

### 1. Cloner le projet

```bash
git clone <repository_url>
cd resume_chatbot
```

### 2. Créer un environnement virtuel

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Créer les comptes gratuits

#### a) Groq (LLM - Gratuit & Rapide)

1. Créer un compte : https://console.groq.com
2. Générer une clé API depuis le Dashboard
3. Quotas gratuits : ~14,000 requêtes/jour

#### b) Cohere (Embeddings - Gratuit)

1. Créer un compte : https://dashboard.cohere.com
2. Générer une clé API depuis le Dashboard
3. Tier gratuit généreux

#### c) Pinecone (Vector Database - Gratuit)

1. Créer un compte : https://www.pinecone.io
2. Créer un nouvel index :
   - **Nom** : `resume-chatbot`
   - **Dimension** : `1024` (pour Cohere) ou `1536` (pour OpenAI)
   - **Metric** : `cosine`
   - **Cloud** : `AWS`
   - **Region** : `us-east-1`
3. Copier votre clé API

### 5. Configuration (.env)

Copier le fichier `.env.example` vers `.env` :

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Éditer le fichier `.env` avec vos clés :

```env
# LLM Configuration
LLM_PROVIDER=groq
LLM_API_KEY=gsk_votre_cle_groq_ici

# Embedding Configuration
EMBEDDING_PROVIDER=cohere
EMBEDDING_API_KEY=votre_cle_cohere_ici

# Pinecone Configuration
PINECONE_API_KEY=votre_cle_pinecone_ici
PINECONE_INDEX_NAME=resume-chatbot

# Application
RESUME_OWNER_NAME=Votre Nom
```

## 📄 Indexer votre CV

Avant de lancer l'API, vous devez indexer votre CV dans Pinecone.

### Option 1 : Indexer un seul fichier

```bash
python index_resume.py --file chemin/vers/votre_cv.pdf
```

### Option 2 : Indexer un dossier complet

Si vous avez divisé votre CV en sections (recommandé pour de meilleurs résultats) :

```bash
python index_resume.py --directory chemin/vers/dossier_sections/
```

### Option 3 : Réinitialiser l'index

Pour supprimer l'ancien contenu avant l'indexation :

```bash
python index_resume.py --file votre_cv.pdf --clear
```

## 🏃 Lancer l'API

```bash
python app.py
```

L'API démarre sur `http://localhost:8000`

## 🧪 Tester l'API

### Test simple (curl)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is the candidate's experience?\"}"
```

### Test depuis Next.js

```javascript
async function askChatbot(question) {
  const response = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  const data = await response.json();
  return data.answer;
}
```

## 📡 Endpoints disponibles

### `GET /`

Health check de l'API

**Response:**

```json
{
  "status": "ok",
  "message": "Resume Chatbot API for John Doe",
  "version": "2.0-simplified"
}
```

### `POST /ask`

Poser une question au chatbot

**Request:**

```json
{
  "question": "What programming languages does the candidate know?"
}
```

**Response:**

```json
{
  "answer": "According to the resume, the candidate is proficient in Python, JavaScript, and Java...",
  "status": "success"
}
```

## 🌐 Déploiement

### Option 1 : Railway (Recommandé)

1. Créer un compte : https://railway.app
2. Créer un nouveau projet
3. Connecter votre repo GitHub
4. Ajouter les variables d'environnement depuis `.env`
5. Railway détecte automatiquement Flask et déploie

**Crédit gratuit** : 5$/mois

### Option 2 : Render

1. Créer un compte : https://render.com
2. Créer un nouveau "Web Service"
3. Connecter votre repo GitHub
4. Configurer :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`
5. Ajouter les variables d'environnement

**Tier gratuit** disponible (avec limitations)

### Option 3 : Fly.io

```bash
# Installer Fly CLI
curl -L https://fly.io/install.sh | sh

# Se connecter
fly auth login

# Déployer
fly launch
```

## 🔧 Configuration avancée

### Utiliser un autre LLM

Dans votre `.env`, changez simplement le provider :

```env
# OpenAI (payant)
LLM_PROVIDER=openai
LLM_API_KEY=sk-...

# Together AI (crédits gratuits)
LLM_PROVIDER=together
LLM_API_KEY=...

# Mistral AI
LLM_PROVIDER=mistral
LLM_API_KEY=...

# Kimi (Moonshot)
LLM_PROVIDER=kimi
LLM_API_KEY=...

# Custom (n'importe quelle API compatible OpenAI)
LLM_PROVIDER=custom
LLM_BASE_URL=https://votre-api.com/v1
LLM_API_KEY=...
```

### Ajuster les paramètres

```env
# Température (0 = déterministe, 1 = créatif)
LLM_TEMPERATURE=0

# Modèle spécifique
LLM_MODEL=llama-3.1-70b-versatile

# Modèle d'embeddings
EMBEDDING_MODEL=embed-english-light-v3.0
```

## 📊 Structure du projet

```
resume_chatbot/
├── app.py                    # API Flask principale
├── index_resume.py           # Script d'indexation
├── requirements.txt          # Dépendances Python
├── .env                      # Configuration (ne pas commit!)
├── .env.example             # Template de configuration
├── config/
│   └── configuration.py     # Chargement de la config
└── backend/
    ├── chatbot.py           # Logique du chatbot
    └── retriever.py         # Interface Pinecone
```

## 🐛 Dépannage

### Erreur : "Missing required environment variables"

→ Vérifiez que votre `.env` contient toutes les clés requises

### Erreur : "Index does not exist"

→ Créez l'index dans Pinecone avec les bonnes dimensions

### Erreur : "Invalid API key"

→ Vérifiez vos clés API dans le `.env`

### L'API ne démarre pas

→ Assurez-vous d'avoir activé l'environnement virtuel et installé les dépendances

### Les réponses ne sont pas pertinentes

→ Vérifiez que votre CV a été correctement indexé avec `index_resume.py`

## 💡 Conseils pour de meilleurs résultats

1. **Divisez votre CV** en sections (expérience, formation, compétences, etc.)
2. **Nommez les fichiers clairement** (ex: `experience.pdf`, `skills.pdf`)
3. **Utilisez un format texte propre** (évitez les images, tableaux complexes)
4. **Testez différentes questions** pour améliorer les réponses

## 📈 Quotas gratuits (estimation)

| Service  | Quota gratuit          | Suffisant pour        |
| -------- | ---------------------- | --------------------- |
| Groq     | ~14,000 req/jour       | ~500 questions/jour   |
| Cohere   | Généreux               | Milliers d'embeddings |
| Pinecone | 1 index, 100K vecteurs | CV complet            |
| Railway  | 5$/mois crédit         | Hébergement léger     |

## 🔒 Sécurité

- Ne commitez **JAMAIS** votre fichier `.env`
- Le `.gitignore` est configuré pour l'ignorer
- Utilisez des variables d'environnement en production
- Ajoutez un rate limiting si besoin (pas inclus par défaut)

## 📞 Support

Pour toute question ou problème, consultez le `.env.example` ou les commentaires dans le code.

## 📝 Licence

Voir le fichier LICENSE dans le projet.

---

**Développé avec ❤️ pour aider les développeurs à créer leur propre chatbot de CV gratuitement**

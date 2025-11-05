# 🧪 Guide de Test de l'API

Ce guide vous montre comment tester votre API de chatbot localement.

## Prérequis

1. L'API doit être en cours d'exécution :
   ```bash
   python app.py
   ```
   L'API démarre sur `http://127.0.0.1:8000`

---

## Méthode 1 : Avec votre Navigateur (Le plus simple) 🌐

### Test 1 : Health Check

Ouvrez votre navigateur et allez sur :

```
http://127.0.0.1:8000/
```

Vous devriez voir :

```json
{
  "status": "ok",
  "message": "Resume Chatbot API for Your Name",
  "version": "2.0-simplified"
}
```

### Test 2 : Poser une question

Pour poser des questions, vous devez utiliser une des méthodes ci-dessous (navigateur seul ne suffit pas pour POST).

---

## Méthode 2 : Avec PowerShell (Recommandé sur Windows) 💻

Ouvrez PowerShell et utilisez `Invoke-RestMethod` :

```powershell
# Question 1 : Expérience
$body = @{
    question = "What is the candidate's experience?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/ask" -Method POST -Body $body -ContentType "application/json"
```

```powershell
# Question 2 : Compétences
$body = @{
    question = "What programming languages does the candidate know?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/ask" -Method POST -Body $body -ContentType "application/json"
```

```powershell
# Question 3 : Formation
$body = @{
    question = "Tell me about the candidate's education"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/ask" -Method POST -Body $body -ContentType "application/json"
```

---

## Méthode 3 : Avec curl (Si installé) 🔧

```bash
# Question 1
curl -X POST http://127.0.0.1:8000/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"What is the candidate's experience?\"}"

# Question 2
curl -X POST http://127.0.0.1:8000/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"What skills does the candidate have?\"}"
```

---

## Méthode 4 : Avec Postman (Application GUI) 📮

1. **Téléchargez Postman** : https://www.postman.com/downloads/
2. **Créez une nouvelle requête** :
   - Méthode : `POST`
   - URL : `http://127.0.0.1:8000/ask`
   - Headers : `Content-Type: application/json`
   - Body (raw, JSON) :
     ```json
     {
       "question": "What is the candidate's experience?"
     }
     ```
3. **Cliquez sur Send**

---

## Méthode 5 : Avec un script Python 🐍

Créez un fichier `test_api.py` :

```python
import requests

def test_chatbot(question):
    url = "http://127.0.0.1:8000/ask"
    data = {"question": question}

    print(f"\n📝 Question: {question}")
    print("⏳ Envoi de la requête...")

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Réponse: {result['answer']}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)

# Tests
if __name__ == "__main__":
    questions = [
        "What is the candidate's experience?",
        "What programming languages does the candidate know?",
        "Tell me about the candidate's education",
        "What are the candidate's main skills?"
    ]

    for q in questions:
        test_chatbot(q)
        print("-" * 80)
```

Lancez-le :

```bash
python test_api.py
```

---

## Méthode 6 : Depuis votre Next.js 🚀

Dans votre code Next.js :

```javascript
// api/chatbot.ts ou components/ChatBot.tsx

async function askChatbot(question) {
  try {
    const response = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();
    console.log("Réponse:", data.answer);
    return data.answer;
  } catch (error) {
    console.error("Erreur:", error);
  }
}

// Utilisation
askChatbot("What is the candidate's experience?");
```

---

## 📊 Résultat attendu

Pour une question valide, vous devriez recevoir :

```json
{
  "answer": "Based on the resume, [réponse générée par le chatbot]...",
  "status": "success"
}
```

---

## ❌ Dépannage

### Problème 1 : "Connection refused"

➡️ L'API n'est pas lancée. Lancez `python app.py` d'abord.

### Problème 2 : "Missing required environment variables"

➡️ Vérifiez votre fichier `.env` avec toutes les clés API.

### Problème 3 : Réponses vides ou erreurs

➡️ Vérifiez que votre CV est bien indexé :

```bash
python index_resume.py --file data/Resume.docx.pdf
```

### Problème 4 : CORS errors (depuis Next.js)

➡️ Normal en local. Une fois déployé sur Railway/Render, ça fonctionnera.
Pour résoudre en local, lancez Next.js avec un proxy ou utilisez l'extension CORS du navigateur.

---

## 🎯 Prochaines étapes

Une fois que les tests locaux fonctionnent :

1. ✅ Déployer l'API sur Railway ou Render
2. ✅ Obtenir l'URL publique (ex: `https://votre-app.railway.app`)
3. ✅ Mettre à jour votre Next.js pour utiliser cette URL
4. ✅ Partager le lien du chatbot dans votre CV !

---

**Besoin d'aide ?** Consultez `README_SIMPLIFIED.md` pour plus de détails.

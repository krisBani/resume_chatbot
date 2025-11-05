"""
Script de test simple pour l'API du chatbot
Utilisation : python test_api.py
"""

import requests
import sys

def test_health():
    """Test le endpoint de health check"""
    print("\n" + "="*80)
    print("🏥 Test 1: Health Check")
    print("="*80)
    
    try:
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            print("✅ L'API est en ligne !")
            print(f"   Réponse : {response.json()}")
            return True
        else:
            print(f"❌ Erreur {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API")
        print("   Assurez-vous que l'API est lancée avec : python app.py")
        return False
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

def test_question(question):
    """Test une question au chatbot"""
    url = "http://127.0.0.1:8000/ask"
    data = {"question": question}
    
    print(f"\n📝 Question : {question}")
    print("⏳ Envoi de la requête...")
    
    try:
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Statut : {result.get('status', 'N/A')}")
            print(f"💬 Réponse :\n{result.get('answer', 'Pas de réponse')}")
            return True
        else:
            print(f"❌ Erreur {response.status_code}")
            print(f"   {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ La requête a pris trop de temps (timeout)")
        return False
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

def main():
    print("\n" + "🤖 TEST DU CHATBOT DE CV ".center(80, "="))
    print("\nCe script va tester votre API de chatbot localement.")
    print("Assurez-vous que l'API est lancée : python app.py\n")
    
    # Test 1: Health check
    if not test_health():
        print("\n⚠️  L'API ne répond pas. Arrêt des tests.")
        sys.exit(1)
    
    # Test 2-5: Questions variées
    questions = [
        "What is the candidate's experience?",
        "What programming languages does the candidate know?",
        "Tell me about the candidate's education",
        "What are the candidate's main skills?"
    ]
    
    print("\n" + "="*80)
    print("💬 Test 2-5: Questions au chatbot")
    print("="*80)
    
    success_count = 0
    for i, question in enumerate(questions, 2):
        print(f"\n--- Test {i} ---")
        if test_question(question):
            success_count += 1
        print("-" * 80)
    
    # Résumé
    print("\n" + "📊 RÉSUMÉ ".center(80, "="))
    total_tests = len(questions) + 1  # +1 pour health check
    print(f"✅ Tests réussis : {success_count + 1}/{total_tests}")
    
    if success_count == len(questions):
        print("\n🎉 Tous les tests sont passés ! Votre chatbot fonctionne parfaitement.")
        print("\n📋 Prochaines étapes :")
        print("   1. Déployer sur Railway ou Render (voir README_SIMPLIFIED.md)")
        print("   2. Connecter votre Next.js à l'URL publique")
        print("   3. Partager le lien dans votre CV !")
    else:
        print("\n⚠️  Certains tests ont échoué.")
        print("   Vérifiez que :")
        print("   - Le fichier .env contient toutes les clés API")
        print("   - Votre CV a été indexé : python index_resume.py --file data/Resume.docx.pdf")
        print("   - Les services (Groq, Pinecone, Cohere) sont accessibles")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()

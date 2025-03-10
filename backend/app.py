from flask import Flask, request, jsonify
import sqlite3
from sentiment_analysis import analyze_sentiment  # Importer la fonction d'analyse

app = Flask(__name__)



# Vérifier si Flask tourne bien
@app.route('/')
def home():
    return "🚀 Flask fonctionne correctement !"

# Route pour analyser le sentiment et enregistrer dans la base de données
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    print("📩 Requête reçue :", data)  # Debug : Afficher les données reçues

    if not data or "text" not in data:
        return jsonify({"error": "Aucun texte fourni"}), 400

    text = data["text"]
    sentiment = analyze_sentiment(text)

    # Sauvegarder le texte et le sentiment dans la base de données
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (text, sentiment) VALUES (?, ?)", (text, sentiment))
    conn.commit()
    conn.close()

    # Retourner la réponse avec le texte et le sentiment
    return jsonify({"text": text, "sentiment": sentiment})

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000, debug=True)  # Exécuter sur toutes les interfaces

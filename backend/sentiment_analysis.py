from transformers import pipeline

# Charger le modèle de Hugging Face
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(text):
    
    result = sentiment_model(text)[0]
    print(f"Debug Model: {result}")  # Voir la sortie brute

    # Transformer le score en Positif, Neutre, Négatif
    if result["label"] in ["5 stars", "4 stars"] :
        return "Positif"
    elif result["label"] == "3 stars":
        return "Neutre"
    else:
        return "Négatif"

# Test rapide
if __name__ == "__main__":
    test_text = "J'adore cet événement, c'était génial !"
    print(f"Texte : {test_text} → Sentiment : {analyze_sentiment(test_text)}")      

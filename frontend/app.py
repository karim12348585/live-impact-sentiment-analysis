import streamlit as st
import sqlite3
import plotly.express as px
import pandas as pd
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Fonction pour extraire les données depuis la base de données SQLite
def fetch_feedback_data():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text, sentiment, date FROM feedback")
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=["Avis", "Sentiment", "Date"])

# Fonction pour stocker une suggestion d'amélioration
def store_suggestion(suggestion):
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS suggestions (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)")
    cursor.execute("INSERT INTO suggestions (text) VALUES (?)", (suggestion,))
    conn.commit()
    conn.close()

# Fonction pour récupérer les suggestions d'amélioration
def fetch_suggestions():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text, date FROM suggestions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=["Suggestion", "Date"])

# Fonction pour télécharger les données
def download_csv(dataframe, filename="data.csv"):
    csv = dataframe.to_csv(index=False)
    st.download_button(
        label="📥 Télécharger les données",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

# Interface Streamlit
st.set_page_config(page_title="Analyse des avis du événement TWISE NIGHT", page_icon="💬", layout="wide")
st.title("💬 Analyse des avis du événement Nuit des Chercheurs en Temps Réel")
st.markdown("**Entrez un avis et voyez instantanément son analyse !**")

# Diviser l'écran en 2 colonnes
col1, col2 = st.columns([2, 3])

# Colonne 1: Avis et Suggestions
with col1:
    st.subheader("📥 Votre Avis et Suggestions")
    
    # Saisie utilisateur pour avis
    user_input = st.text_area("📝 Votre avis ici :", "")

    # URL de l'API Flask
    API_URL = "http://127.0.0.1:5000/analyze"

    # Bouton pour analyser
    if st.button("🔍 Analyser Sentiment"):
        if user_input.strip():
            response = requests.post(API_URL, json={"text": user_input})

            if response.status_code == 200:
                result = response.json()
                sentiment = result["sentiment"]

                st.subheader("📊 Résultat de l'analyse :")
                if sentiment == "Positif":
                    st.success(f"😊 Sentiment détecté : **{sentiment}**")
                elif sentiment == "Négatif":
                    st.error(f"😠 Sentiment détecté : **{sentiment}**")
                else:
                    st.warning(f"😐 Sentiment détecté : **{sentiment}**")

                # Sauvegarde du sentiment dans la base de données
                conn = sqlite3.connect('feedback.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO feedback (text, sentiment, date) VALUES (?, ?, datetime('now'))", (user_input, sentiment))
                conn.commit()
                conn.close()
            else:
                st.error("❌ Erreur lors de l'analyse. Vérifiez l'API Flask.")
        else:
            st.warning("⚠️ Veuillez entrer un texte.")
    
    # Barre de suggestion
    st.subheader("💡 Suggestions pour Améliorer les Futurs Événements")
    suggestion_input = st.text_area("📝 Partagez vos idées pour améliorer les prochains événements :", "")
    
    if st.button("📩 Soumettre la Suggestion"):
        if suggestion_input.strip():
            store_suggestion(suggestion_input)
            st.success("✅ Suggestion enregistrée avec succès !")
        else:
            st.warning("⚠️ Veuillez entrer une suggestion valide.")

# Colonne 2: Graphiques et Statistiques
with col2:
    st.subheader("📊 Statistiques et Graphiques")
    
    # Option de filtrage des sentiments
    sentiment_filter = st.selectbox("🔎 Filtrer les avis par sentiment", ["Tous", "Positif", "Négatif", "Neutre"])

    # Récupérer les données filtrées
    df = fetch_feedback_data()

    if sentiment_filter != "Tous":
        df = df[df["Sentiment"] == sentiment_filter]

    # Affichage des graphiques et des statistiques
    if not df.empty:
        # Distribution des sentiments
        sentiment_counts = df["Sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Nombre"]
        fig = px.bar(sentiment_counts, x="Sentiment", y="Nombre", color="Sentiment", title="📊 Distribution des Sentiments", text_auto=True)
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig)

        sentiment_pie = df["Sentiment"].value_counts().reset_index()
        sentiment_pie.columns = ["Sentiment", "Nombre"]
        fig_pie = px.pie(sentiment_pie, names="Sentiment", values="Nombre", title="🗨️ Répartition des Sentiments")
        st.plotly_chart(fig_pie)

        all_text = " ".join(df["Avis"])
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)
        st.subheader("🌟 Nuage de Mots des Avis")
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        # Global sentiment trend over time
        df["Date"] = pd.to_datetime(df["Date"])
        df['Date'] = df['Date'].dt.date  # On ne garde que la date, pas l'heure
        
        # Sentiment trend calculation
        sentiment_map = {"Positif": 1, "Neutre": 0, "Négatif": -1}
        df['Sentiment_Score'] = df['Sentiment'].map(sentiment_map)
        
        sentiment_trend = df.groupby("Date")["Sentiment_Score"].mean().reset_index()
        sentiment_trend.columns = ["Date", "Sentiment_Moyen"]
        
        # Plotting the global sentiment curve
        fig_trend = px.line(sentiment_trend, x="Date", y="Sentiment_Moyen", title="📈 Évolution du Sentiment Global", 
                            labels={"Sentiment_Moyen": "Sentiment Moyen", "Date": "Date"})
        st.plotly_chart(fig_trend)

        # Affichage du résumé des statistiques
        st.subheader("📈 Résumé des Statistiques")
        st.write(f"Nombre total d'avis : {len(df)}")
        st.write(f"Nombre d'avis positifs : {len(df[df['Sentiment'] == 'Positif'])}")
        st.write(f"Nombre d'avis négatifs : {len(df[df['Sentiment'] == 'Négatif'])}")
        st.write(f"Nombre d'avis neutres : {len(df[df['Sentiment'] == 'Neutre'])}")

        # Option de téléchargement des données
        download_csv(df)

    else:
        st.warning("⚠️ Aucun avis analysé pour l'instant.")

    # Affichage des suggestions après les graphiques
    suggestions_df = fetch_suggestions()
    if not suggestions_df.empty:
        st.subheader("📌 Suggestions Soumises")
        st.dataframe(suggestions_df)

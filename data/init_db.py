import sqlite3

# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('feedback.db')

# Create a cursor object
cursor = conn.cursor()


# Fonction pour créer la base de données et les tables si elles n'existent pas
def create_tables():

    cursor = conn.cursor()
    
    # Création de la table 'feedback' si elle n'existe pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            sentiment TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Création de la table 'suggestions' si elle n'existe pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Exécuter la fonction au démarrage
create_tables()

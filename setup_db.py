import sqlite3

# Crée un fichier de base de données local
conn = sqlite3.connect('ventes.db')
cursor = conn.cursor()

# Création des tables
cursor.execute('''CREATE TABLE utilisateurs (id INTEGER PRIMARY KEY, nom TEXT, pays TEXT)''')
cursor.execute('''CREATE TABLE commandes (id INTEGER PRIMARY KEY, utilisateur_id INTEGER, montant REAL, date TEXT)''')

# Insertion de quelques fausses données
utilisateurs = [("Alice", "France"), ("Bob", "Belgique"), ("Charlie", "France")]
cursor.executemany("INSERT INTO utilisateurs (nom, pays) VALUES (?, ?)", utilisateurs)

commandes = [(1, 150.5, "2026-09-01"), (1, 45.0, "2026-09-15"), (2, 300.0, "2026-09-10")]
cursor.executemany("INSERT INTO commandes (utilisateur_id, montant, date) VALUES (?, ?, ?)", commandes)

conn.commit()
conn.close()
print("Base de données 'ventes.db' créée avec succès !")